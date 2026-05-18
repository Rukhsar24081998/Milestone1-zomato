# Milestone Zomato

Phase 0 delivers the **project skeleton**, **environment-based config**, **shared schemas** (`Restaurant`, `UserPreferences`, `Recommendation`), and **stub** implementations of `list_restaurants`, `filter_candidates`, and `recommend`. **User preferences are intended to come from a basic web UI** in a later phase; `UserPreferences` is the JSON/form contract that UI will post to the API (Phase 0 establishes the model only).

## Setup

Requires **Python 3.9+** (see `requires-python` in `pyproject.toml`).

```bash
cd "MILESTONE - ZOMATO"
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env
```

## Phase 1 — ingest Hugging Face data

Ingestion lives in **`phase1/milestone_zomato_ingestion/`** (see `phase1/README.md`). It downloads the configured dataset, normalizes rows into the canonical schema, and writes **Parquet** (default: `data/cache/restaurants.parquet`). `list_restaurants()` reads that file when it exists.

```bash
milestone-zomato-ingest
# or: python -m milestone_zomato_ingestion
```

Optional: `ZOMATO_HF_DATASET_REVISION` pins a commit for repeatable runs.

## Phase 2 — filtering

Deterministic filter + cap-K lives in **`phase2/milestone_zomato_filter/`** (see `phase2/README.md`). Tune **`ZOMATO_FILTER_TOP_K`** (default `50`).

## Verify Phase 0

```bash
python -m milestone_zomato
pytest -q
ruff check src tests
```

Secrets (e.g. `OPENAI_API_KEY`) are optional for Phase 0; they load from `.env` if present via `pydantic-settings`.
