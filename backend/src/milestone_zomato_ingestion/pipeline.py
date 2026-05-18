"""Build canonical DataFrame and write Parquet cache."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Iterable, Iterator, List, Optional

import pandas as pd

from milestone_zomato.models.restaurant import RESTAURANT_DF_COLUMNS
from milestone_zomato_ingestion.normalize import normalize_record, validate_record


def build_restaurants_dataframe(rows: Iterable[Dict[str, Any]]) -> pd.DataFrame:
    """Normalize raw HF dict rows into the canonical store schema."""
    records: List[Dict[str, Any]] = []
    for i, raw in enumerate(rows):
        rec = normalize_record(raw, fallback_index=i)
        if rec is None:
            continue
        ok, _ = validate_record(rec)
        if not ok:
            continue
        records.append(rec)
    df = pd.DataFrame.from_records(records, columns=RESTAURANT_DF_COLUMNS)
    # Ensure column order even if empty
    if df.empty:
        return pd.DataFrame(columns=RESTAURANT_DF_COLUMNS)
    return df


def ingest_to_parquet(
    dataset_id: str,
    parquet_path: Path,
    metadata_path: Optional[Path] = None,
    revision: Optional[str] = None,
) -> pd.DataFrame:
    """Load HF dataset, normalize, write Parquet + optional metadata JSON."""
    from milestone_zomato_ingestion.loader import load_hf_train_rows

    parquet_path = Path(parquet_path)
    parquet_path.parent.mkdir(parents=True, exist_ok=True)

    rows: Iterator[Dict[str, Any]] = load_hf_train_rows(dataset_id, revision=revision)
    df = build_restaurants_dataframe(rows)
    df.to_parquet(parquet_path, index=False)

    meta = {
        "dataset_id": dataset_id,
        "revision": revision,
        "rows_written": int(len(df)),
        "parquet_path": str(parquet_path.resolve()),
    }
    if metadata_path is not None:
        metadata_path = Path(metadata_path)
        metadata_path.parent.mkdir(parents=True, exist_ok=True)
        metadata_path.write_text(json.dumps(meta, indent=2), encoding="utf-8")
    return df
