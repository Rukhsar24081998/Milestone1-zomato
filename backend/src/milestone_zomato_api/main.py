"""FastAPI application serving the UI and API for Phase 4."""

import os
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from milestone_zomato.data.store import list_restaurants
from milestone_zomato.filter.engine import filter_candidates
from milestone_zomato.llm.recommend import recommend
from milestone_zomato.models.preferences import UserPreferences
from milestone_zomato_filter.matching import city_matches, cuisine_matches
from milestone_zomato_api.dto import PresentationResponse, PresentationResult
from milestone_zomato_api.summary import generate_summary_blurb
from milestone_zomato_ops.middleware import OperationalMiddleware
from milestone_zomato_ops.logging import Timer, MetricsLogger
from milestone_zomato_ops.cache import cached_recommendation

app = FastAPI(title="Zomato Recommender", version="1.0.0")

# Phase 5: Operational Middleware
app.add_middleware(OperationalMiddleware)

# CORS configuration
# Allow localhost (dev), any *.streamlit.app (Streamlit Cloud),
# any *.onrender.com (Render preview URLs), plus any custom domain
# set via the ALLOWED_ORIGINS env var (comma-separated).
_extra_origins = [
    o.strip()
    for o in os.getenv("ALLOWED_ORIGINS", "").split(",")
    if o.strip()
]
_default_origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=_default_origins + _extra_origins,
    allow_origin_regex=r"https://(.*\.streamlit\.app|.*\.onrender\.com|.*\.vercel\.app)",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setup static files for UI
UI_DIR = Path(__file__).parent.parent.parent.parent / "frontend"
app.mount("/static", StaticFiles(directory=UI_DIR), name="static")


@app.get("/")
def read_root():
    """Serve the main UI index.html."""
    return FileResponse(UI_DIR / "index.html")


@app.get("/health")
def health_check():
    """Liveness probe: check if the API is up."""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "features": ["search", "caching", "metrics"]
    }


@app.get("/ready")
def readiness_check():
    """Readiness probe: check if data is loaded."""
    df = list_restaurants()
    if df.empty:
        return {"status": "not_ready", "reason": "Database is empty or missing."}, 503
    return {"status": "ready"}


# Wrap the internal recommendation logic to allow caching
@cached_recommendation
def _get_recommendations_pipeline(prefs: UserPreferences):
    # Ensure data is loaded (Phase 1)
    df = list_restaurants()
    if df.empty:
        return None

    # Phase 2: Deterministic Filtering
    with Timer("filter_candidates"):
        candidates = filter_candidates(prefs)

        if not candidates and (prefs.location or prefs.cuisine):
            if prefs.location:
                location_mask = (
                    df["city"].apply(lambda v: city_matches(v, prefs.location)) |
                    df["area"].apply(lambda v: city_matches(v, prefs.location))
                )
                if not location_mask.any():
                    relaxed = prefs.model_copy(update={"location": None})
                    candidates = filter_candidates(relaxed)

            if not candidates and prefs.cuisine:
                cuisine_mask = df["cuisines"].apply(lambda v: cuisine_matches(v, prefs.cuisine))
                if not cuisine_mask.any():
                    relaxed = prefs.model_copy(update={"cuisine": None})
                    candidates = filter_candidates(relaxed)

    MetricsLogger.log_metrics("filter_stats", candidate_count=len(candidates))

    # Phase 3: LLM Recommendations (Combined with summary blurb)
    with Timer("llm_recommend"):
        recommendations, summary_blurb = recommend(prefs, candidates)

    return recommendations, candidates, summary_blurb


@app.post("/api/recommend", response_model=PresentationResponse)
def get_recommendations(prefs: UserPreferences) -> PresentationResponse:
    """End-to-end recommendation pipeline."""
    pipeline_result = _get_recommendations_pipeline(prefs)
    
    if pipeline_result is None:
        return PresentationResponse(results=[], summary_blurb="Database is empty or missing.")

    recommendations, candidates, summary_blurb = pipeline_result

    # Map candidate data back to the recommendations to form PresentationResults
    candidate_dict = {c.id: c for c in candidates}
    
    results = []
    for rec in sorted(recommendations, key=lambda x: x.rank):
        restaurant = candidate_dict.get(rec.restaurant_id)
        if restaurant:
            # Clean up cuisines if they are in list/numpy format
            cuisine_list = restaurant.cuisines
            if isinstance(cuisine_list, (list, tuple)):
                cuisine_str = ", ".join(cuisine_list)
            elif isinstance(cuisine_list, str):
                # Handle cases where it might be a string representation of a list
                cuisine_str = cuisine_list.strip("[]").replace("'", "").replace('"', "").replace("\n", ", ")
            else:
                cuisine_str = str(cuisine_list)

            results.append(
                PresentationResult(
                    name=restaurant.name,
                    cuisines=cuisine_str,
                    rating=restaurant.rating,
                    cost=restaurant.cost_bucket,
                    explanation=rec.explanation,
                )
            )

    # If we have no results, but the pipeline returned a generic error blurb
    if not results and "expert" in summary_blurb.lower():
        return PresentationResponse(results=[], summary_blurb=summary_blurb)

    return PresentationResponse(results=results, summary_blurb=summary_blurb)

