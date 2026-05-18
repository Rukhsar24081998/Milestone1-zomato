"""CLI: download + normalize + write ``restaurants.parquet`` (requires network for HF)."""

from __future__ import annotations

import argparse
from pathlib import Path

from milestone_zomato.config import get_settings
from milestone_zomato_ingestion.pipeline import ingest_to_parquet


def main() -> None:
    parser = argparse.ArgumentParser(description="Ingest Zomato HF dataset into Parquet cache.")
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Override Parquet output path (default: from settings / env).",
    )
    parser.add_argument(
        "--metadata",
        type=Path,
        default=None,
        help="Optional JSON metadata path (default: alongside Parquet).",
    )
    args = parser.parse_args()

    s = get_settings()
    out = args.output or Path(s.restaurant_cache_path)
    meta = args.metadata
    if meta is None:
        meta = out.with_suffix(".meta.json")

    df = ingest_to_parquet(
        dataset_id=s.hf_dataset_id,
        parquet_path=out,
        metadata_path=meta,
        revision=s.hf_dataset_revision,
    )
    print(f"Wrote {len(df)} rows to {out}")
    print(f"Metadata: {meta}")


if __name__ == "__main__":
    main()
