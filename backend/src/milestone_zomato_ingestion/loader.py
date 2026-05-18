"""Load raw rows from Hugging Face ``datasets``."""

from __future__ import annotations

from typing import Any, Dict, Iterator, List, Optional

from milestone_zomato_ingestion.mapping import (
    COL_ADDRESS,
    COL_COST,
    COL_CUISINES,
    COL_LISTED_CITY,
    COL_LOCATION,
    COL_NAME,
    COL_RATE,
    COL_URL,
)


def _required_columns() -> List[str]:
    return [
        COL_URL,
        COL_NAME,
        COL_ADDRESS,
        COL_LOCATION,
        COL_CUISINES,
        COL_RATE,
        COL_COST,
        COL_LISTED_CITY,
    ]


def load_hf_train_rows(
    dataset_id: str,
    revision: Optional[str] = None,
) -> Iterator[Dict[str, Any]]:
    """Stream or iterate ``train`` split rows as dicts.

    Raises if the dataset schema is missing expected columns.
    """
    from datasets import load_dataset

    ds = load_dataset(
        dataset_id,
        split="train",
        revision=revision,
        trust_remote_code=False,
    )
    cols = set(ds.column_names)
    missing = [c for c in _required_columns() if c not in cols]
    if missing:
        raise ValueError(
            f"Dataset {dataset_id!r} missing expected columns: {missing}. "
            f"Found: {sorted(cols)}",
        )
    for row in ds:
        yield dict(row)
