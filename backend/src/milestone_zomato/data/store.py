"""Restaurant store access: Phase 1 reads normalized Parquet cache when present."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from ..config import get_settings
from ..models.restaurant import RESTAURANT_DF_COLUMNS

# Project root = four levels up from this file:
# store.py → data/ → milestone_zomato/ → src/ → backend/ → project root
_PROJECT_ROOT = Path(__file__).resolve().parents[4]


def _resolve_cache_path() -> Path:
    """Return an absolute Path to the parquet cache.

    If the configured value is already absolute, use it as-is.
    If it is relative, resolve it against the project root so the
    backend works regardless of which directory uvicorn is launched from.
    """
    raw = get_settings().restaurant_cache_path
    p = Path(raw)
    if p.is_absolute():
        return p
    # Relative path — anchor to project root
    return (_PROJECT_ROOT / p).resolve()


def list_restaurants() -> pd.DataFrame:
    """Return the canonical restaurant table.

    Loads the Parquet cache written by Phase 1 ingest.
    Returns an empty frame (with the stable column set) if the file is missing.
    """
    path = _resolve_cache_path()
    if not path.is_file():
        return pd.DataFrame(columns=RESTAURANT_DF_COLUMNS)
    df = pd.read_parquet(path)
    missing = [c for c in RESTAURANT_DF_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(
            f"Parquet at {path} missing columns {missing}; "
            f"expected {RESTAURANT_DF_COLUMNS}. Re-run ingest.",
        )
    return df.loc[:, RESTAURANT_DF_COLUMNS].copy()
