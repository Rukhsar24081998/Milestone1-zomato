"""Row-level matching helpers (city, cuisine lists)."""

from __future__ import annotations

from typing import Any, List

import pandas as pd


def coerce_cuisine_list(value: Any) -> List[str]:
    """Normalize ``cuisines`` cell from Parquet/DataFrame to a list of strings."""
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return []
    if isinstance(value, list):
        return [str(x).strip() for x in value if str(x).strip()]
    if isinstance(value, str):
        return [p.strip() for p in value.split(",") if p.strip()]
    return [str(value).strip()] if str(value).strip() else []


def city_matches(city_val: Any, user_location: str) -> bool:
    """Symmetric substring / equality match on normalized city labels with fuzzy matching."""
    if not user_location:
        return True
    u = user_location.strip().casefold()
    if not u:
        return True
    if city_val is None or (isinstance(city_val, float) and pd.isna(city_val)):
        return False
    c = str(city_val).strip().casefold()
    if not c:
        return False
    
    # Exact match or substring match
    if c == u or u in c or c in u:
        return True
    
    # Common typo corrections for Indian cities
    typo_map = {
        "banglore": "bangalore",
        "bangaluru": "bangalore",
        "bombay": "mumbai",
        "calcutta": "kolkata",
        "madras": "chennai",
        "dilli": "delhi",
        "new delhi": "delhi",
        "gurgaon": "gurugram",
    }
    
    # Check if user input is a known typo
    corrected_u = typo_map.get(u, u)
    if corrected_u != u and (c == corrected_u or corrected_u in c or c in corrected_u):
        return True
    
    # Check if city value is a known typo
    corrected_c = typo_map.get(c, c)
    if corrected_c != c and (corrected_c == u or u in corrected_c or corrected_c in u):
        return True
    
    return False


def cuisine_matches(cuisine_cell: Any, user_cuisine: str) -> bool:
    """Match user cuisine phrase against any normalized token (substring allowed)."""
    if not user_cuisine:
        return True
    u = user_cuisine.strip().casefold()
    if not u:
        return True
    for token in coerce_cuisine_list(cuisine_cell):
        t = token.casefold()
        if t == u or u in t or t in u:
            return True
    return False
