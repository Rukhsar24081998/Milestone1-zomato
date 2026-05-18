"""Smoke entrypoint: ensures Phase 0 contracts import and run."""

from __future__ import annotations

from .config import get_settings
from .data.store import list_restaurants
from .filter.engine import filter_candidates
from .llm.recommend import recommend
from .models import UserPreferences


def main() -> None:
    settings = get_settings()
    print(
        f"milestone-zomato settings: dataset={settings.hf_dataset_id!r}, "
        f"llm_model={settings.llm_model!r}, cache={settings.restaurant_cache_path!r}",
    )

    df = list_restaurants()
    print(f"list_restaurants: rows={len(df)}, columns={list(df.columns)}")

    prefs = UserPreferences(location="Delhi", cuisine="Chinese", budget="medium", min_rating=3.5)
    candidates = filter_candidates(prefs)
    print(f"filter_candidates: n={len(candidates)}")

    recs = recommend(prefs, candidates)
    print(f"recommend: n={len(recs)}")


if __name__ == "__main__":
    main()
