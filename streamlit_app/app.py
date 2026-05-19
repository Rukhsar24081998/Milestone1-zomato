"""Phase 7 — Streamlit frontend for Zomato AI Recommendations.

Calls the FastAPI backend (local or Render) via POST /api/recommend.
Set BACKEND_URL in Streamlit secrets or as an environment variable.
"""

import os

import requests
import streamlit as st

# ── Config ────────────────────────────────────────────────────────────────────
BACKEND_URL = (
    st.secrets.get("BACKEND_URL", None)
    if hasattr(st, "secrets")
    else None
) or os.getenv("BACKEND_URL", "http://localhost:8000")

BACKEND_URL = BACKEND_URL.rstrip("/")

# ── Page setup ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Zomato AI Recommendations",
    page_icon="🍽️",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

        /* Brand colours */
        :root {
            --zomato-red: #b7122a;
            --zomato-light: #fdf3f4;
            --zomato-muted: #5b403f;
            --zomato-dark: #1b1c1c;
        }

        body, .css-1d391kg, .stTextInput, .stSelectbox, .stNumberInput {
            font-family: 'Inter', 'Segoe UI', -apple-system, BlinkMacSystemFont, sans-serif;
        }

        /* Header strip */
        .zomato-header {
            background: var(--zomato-red);
            color: white;
            padding: 1rem 1.5rem;
            border-radius: 12px;
            margin-bottom: 1.5rem;
            display: flex;
            align-items: center;
            gap: 0.6rem;
        }
        .zomato-header h1 {
            margin: 0;
            font-size: 1.6rem;
            font-weight: 800;
            letter-spacing: -0.5px;
        }
        .zomato-header p {
            margin: 0;
            font-size: 0.85rem;
            opacity: 0.85;
        }

        /* Summary blurb */
        .summary-box {
            background: var(--zomato-light);
            border-left: 4px solid var(--zomato-red);
            padding: 0.9rem 1.1rem;
            border-radius: 8px;
            margin-bottom: 1.2rem;
            font-size: 0.95rem;
            color: var(--zomato-muted);
        }

        .stButton>button {
            background: var(--zomato-red) !important;
            color: white !important;
            border-radius: 10px !important;
            padding: 0.8rem 1.2rem !important;
        }
        .stButton>button:hover {
            background: #a51124 !important;
        }

        .stTextInput>div>div>input,
        .stNumberInput>div>div>input,
        .stSelectbox>div>div>div>div>div>select {
            border-radius: 10px !important;
        }

        /* Restaurant card */
        .restaurant-card {
            background: white;
            border: 1px solid #f0e0e0;
            border-radius: 14px;
            padding: 1.1rem 1.3rem;
            margin-bottom: 0.9rem;
            box-shadow: 0 2px 8px rgba(183,18,42,0.06);
        }
        .restaurant-card h3 {
            margin: 0 0 0.3rem 0;
            font-size: 1.05rem;
            font-weight: 700;
            color: #1b1c1c;
        }
        .restaurant-card .meta {
            display: flex;
            gap: 0.7rem;
            flex-wrap: wrap;
            margin-bottom: 0.55rem;
        }
        .badge {
            font-size: 0.75rem;
            font-weight: 600;
            padding: 2px 9px;
            border-radius: 20px;
        }
        .badge-rating  { background: #e8f5e9; color: #2e7d32; }
        .badge-cost    { background: #fff3e0; color: #e65100; }
        .badge-cuisine { background: #f3e5f5; color: #6a1b9a; }
        .explanation {
            font-size: 0.85rem;
            color: var(--zomato-muted);
            line-height: 1.5;
            margin: 0;
        }

        /* Status pill */
        .status-pill {
            display: inline-block;
            font-size: 0.72rem;
            font-weight: 700;
            padding: 2px 10px;
            border-radius: 20px;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        .status-live   { background: #e8f5e9; color: #2e7d32; }
        .status-down   { background: #fce4ec; color: #b71c1c; }
        .status-check  { background: #fff8e1; color: #f57f17; }

        /* Hide Streamlit default footer */
        footer { visibility: hidden; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown(
    """
    <div class="zomato-header">
        <span style="font-size:2rem">🍽️</span>
        <div>
            <h1>ZOMATO AI</h1>
            <p>AI-powered restaurant recommendations in India</p>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ── API health indicator ───────────────────────────────────────────────────────
@st.cache_data(ttl=30, show_spinner=False)
def check_health(url: str) -> str:
    try:
        r = requests.get(f"{url}/health", timeout=5)
        if r.status_code == 200 and r.json().get("status") == "healthy":
            return "live"
        return "down"
    except Exception:
        return "down"


health = check_health(BACKEND_URL)
pill_class = "status-live" if health == "live" else "status-down"
pill_label = "API LIVE" if health == "live" else "API DOWN"
st.markdown(
    f'<span class="status-pill {pill_class}">{pill_label}</span>',
    unsafe_allow_html=True,
)

if health == "down":
    st.error(
        f"Cannot reach the backend at **{BACKEND_URL}**. "
        "Make sure the FastAPI server is running or check your `BACKEND_URL` secret."
    )

st.markdown("---")

# ── Search form ───────────────────────────────────────────────────────────────
st.subheader("🔍 Find your next favourite meal")

city_options = [
    "Bangalore",
    "Mumbai",
    "Delhi",
    "Chennai",
    "Hyderabad",
    "Kolkata",
    "Pune",
    "Ahmedabad",
    "Jaipur",
    "Lucknow",
    "Goa",
]
col1, col2 = st.columns([3, 1])
with col1:
    location = st.selectbox(
        "City",
        options=city_options,
        index=0,
        help="Select the city for which you want restaurant recommendations.",
    )
    cuisine = st.text_input(
        "Cuisine",
        placeholder="North Indian, Italian, Biryani…",
    )
with col2:
    budget_inr = st.number_input(
        "Budget (₹ per person)",
        min_value=0,
        max_value=10000,
        value=800,
        step=100,
        help="≤ ₹500 = low · ₹501–1500 = medium · > ₹1500 = high",
    )
    min_rating = st.select_slider(
        "Minimum rating ⭐",
        options=[1.0, 2.0, 3.0, 4.0, 5.0],
        value=4.0,
        format_func=lambda x: f"{x:.0f} & above" if x < 5 else "5 only",
    )

# Map INR amount → budget band
def inr_to_band(amount: int) -> str:
    if amount <= 500:
        return "low"
    if amount <= 1500:
        return "medium"
    return "high"


budget_band = inr_to_band(int(budget_inr))
st.caption(f"Budget band: **{budget_band}** (₹{int(budget_inr):,})")

search_clicked = st.button(
    "⚡ Find Flavors",
    type="primary",
    disabled=(health == "down"),
    use_container_width=True,
)

# ── Results ───────────────────────────────────────────────────────────────────
if search_clicked:
    payload = {
        "location": location,
        "budget": budget_band,
        "cuisine": cuisine.strip() or None,
        "min_rating": min_rating,
    }

    with st.spinner("Asking Zomato AI…"):
        try:
            resp = requests.post(
                f"{BACKEND_URL}/api/recommend",
                json=payload,
                timeout=60,
            )
            resp.raise_for_status()
            data = resp.json()
        except requests.exceptions.Timeout:
            st.error("The request timed out. The backend may be waking up (Render free tier). Try again in 30 seconds.")
            st.stop()
        except requests.exceptions.RequestException as exc:
            st.error(f"Request failed: {exc}")
            st.stop()

    results = data.get("results", [])
    summary = data.get("summary_blurb", "")

    if not results:
        st.warning(
            "No restaurants found. Try a different city, lower your minimum rating, or broaden your cuisine."
        )
    else:
        # Summary blurb
        if summary and summary.lower() not in ("no candidates found.", "database is empty or missing."):
            st.markdown(
                f'<div class="summary-box">💡 {summary}</div>',
                unsafe_allow_html=True,
            )

        st.success(f"Found **{len(results)}** restaurant{'s' if len(results) != 1 else ''}")

        # Cost bucket → display label
        cost_labels = {"low": "₹", "medium": "₹₹", "high": "₹₹₹"}

        for r in results:
            name      = r.get("name", "Unknown")
            cuisines  = r.get("cuisines", "")
            rating    = r.get("rating")
            cost      = r.get("cost", "")
            expl      = r.get("explanation", "")

            # Clean numpy-style cuisine strings: ['North Indian' 'Chinese'] → North Indian, Chinese
            cuisines = (
                cuisines.strip("[]")
                .replace("'", "")
                .replace('"', "")
                .replace("\n", " ")
            )
            # numpy arrays use spaces between tokens — normalise to comma-separated
            import re
            cuisines = re.sub(r"\s{2,}", ", ", cuisines).strip(", ")

            rating_badge  = f'<span class="badge badge-rating">⭐ {rating:.1f}</span>' if rating else ""
            cost_badge    = f'<span class="badge badge-cost">{cost_labels.get(cost, cost)}</span>' if cost else ""
            cuisine_badge = f'<span class="badge badge-cuisine">🍴 {cuisines}</span>' if cuisines else ""

            st.markdown(
                f"""
                <div class="restaurant-card">
                    <h3>{name}</h3>
                    <div class="meta">
                        {rating_badge}
                        {cost_badge}
                        {cuisine_badge}
                    </div>
                    <p class="explanation">{expl}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.caption(
    "🍽️ **Zomato AI Recommendations** · Phase 7 · "
    "Powered by FastAPI + OpenAI · Deployed on Streamlit Community Cloud & Render"
)
