"""Pandas filter engine + stable cap-K ordering."""

from __future__ import annotations

from typing import List, Optional

import pandas as pd

from milestone_zomato.config import get_settings
from milestone_zomato.models.preferences import UserPreferences
from milestone_zomato.models.restaurant import RESTAURANT_DF_COLUMNS, Restaurant
from milestone_zomato_filter.matching import city_matches, coerce_cuisine_list, cuisine_matches
from milestone_zomato_filter.validate import effective_prefs, validate_preferences_for_filter


def _optional_str(val: object) -> Optional[str]:
    if val is None or (isinstance(val, float) and pd.isna(val)):
        return None
    s = str(val).strip()
    return s or None


def _row_to_restaurant(row: pd.Series) -> Restaurant:
    cuisines = coerce_cuisine_list(row.get("cuisines"))
    cb = row.get("cost_bucket")
    cost_bucket = None
    if cb is not None and not (isinstance(cb, float) and pd.isna(cb)):
        raw = str(cb).strip().lower()
        if raw in {"low", "medium", "high"}:
            cost_bucket = raw  # type: ignore[assignment]
    rating_f: Optional[float]
    rating = row.get("rating")
    if rating is not None and not (isinstance(rating, float) and pd.isna(rating)):
        rating_f = float(rating)
    else:
        rating_f = None
    return Restaurant(
        id=str(row["id"]),
        name=str(row["name"]),
        city=_optional_str(row.get("city")),
        area=_optional_str(row.get("area")),
        cuisines=cuisines,
        cost_bucket=cost_bucket,
        rating=rating_f,
    )


def filter_candidates_from_frame(prefs: UserPreferences, df: pd.DataFrame) -> List[Restaurant]:
    """Apply hard filters and cap-K to an in-memory canonical frame (test hook)."""
    validate_preferences_for_filter(prefs)
    ep = effective_prefs(prefs)

    if df.empty:
        return []

    missing = [c for c in RESTAURANT_DF_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"DataFrame missing columns {missing}; expected {RESTAURANT_DF_COLUMNS}")

    work = df.loc[:, RESTAURANT_DF_COLUMNS].copy()
    mask = pd.Series(True, index=work.index)

    if ep.location:
        mask &= work["city"].apply(lambda v: city_matches(v, ep.location)) | \
                work["area"].apply(lambda v: city_matches(v, ep.location))

    if ep.cuisine:
        mask &= work["cuisines"].apply(lambda v: cuisine_matches(v, ep.cuisine))

    if ep.budget is not None:
        mask &= work["cost_bucket"].notna() & (
            work["cost_bucket"].astype(str).str.strip().str.lower() == ep.budget
        )

    if ep.min_rating is not None:
        mask &= work["rating"].notna() & (work["rating"].astype(float) >= float(ep.min_rating))

    filtered = work.loc[mask]
    if filtered.empty:
        return []

    k = max(1, int(get_settings().filter_top_k))
    tmp = filtered.copy()
    tmp["_sort_rating"] = tmp["rating"].astype(float).fillna(-1.0)
    tmp["_sort_name"] = tmp["name"].map(lambda x: str(x).strip().casefold())
    tmp["_sort_id"] = tmp["id"].astype(str)
    tmp = tmp.sort_values(
        by=["_sort_rating", "_sort_name", "_sort_id"],
        ascending=[False, True, True],
    )
    capped = tmp.head(k).drop(columns=["_sort_rating", "_sort_name", "_sort_id"])
    return [_row_to_restaurant(capped.iloc[i]) for i in range(len(capped))]


def filter_candidates(prefs: UserPreferences) -> List[Restaurant]:
    """Load the store via :func:`~milestone_zomato.data.store.list_restaurants` and filter."""
    from milestone_zomato.data.store import list_restaurants

    df = list_restaurants()
    return filter_candidates_from_frame(prefs, df)
