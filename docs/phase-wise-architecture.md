# Phase-Wise Architecture: AI Restaurant Recommendation

This document turns the [problem statement](./problemstatement.md) into **delivery phases**, each with scope, main components, and exit criteria. Phases are ordered so later work depends on stable contracts from earlier phases.

---

## Reference: End-to-End Flow

```mermaid
flowchart LR
  subgraph P0_P1["Phases 0–1: Foundation & Data"]
    DS[(Dataset / HF)]
    ING[Ingestion & Normalize]
    DS --> ING
    STORE[(Restaurant store)]
    ING --> STORE
  end

  subgraph P2["Phase 2: Preferences & Filter"]
    UI[Basic web UI\n(prefs)]
    FIL[Filter & rank K]
    UI --> FIL
    STORE --> FIL
  end

  subgraph P3["Phase 3: LLM layer"]
    PROMPT[Prompt builder]
    LLM[LLM API]
    PARSE[Structured parse / validate]
    FIL --> PROMPT
    PROMPT --> LLM
    LLM --> PARSE
  end

  subgraph P4["Phase 4: Experience"]
    OUT[Web UI + results]
    PARSE --> OUT
  end
```

---

## Phase 0 — Foundation & Contracts

**Purpose:** Agree on boundaries so data, filtering, and the LLM can evolve independently.

| Item | Description |
|------|-------------|
| **Input channel (decision)** | A **basic web UI** is the planned primary source of user preferences: forms map to `UserPreferences` (and optional API JSON). Phase 0 does not ship the UI yet, but schemas and validation are defined so the future client is the source of truth for prefs—not ad hoc scripts. |
| **Scope** | Repo layout; runtime (e.g. Python service, Node, or notebook-first then extract); where secrets live; minimal CI or lint if required by course. |
| **Components** | Project skeleton; config for dataset ID/URL and LLM provider; shared types/schemas for `Restaurant`, `UserPreferences`, `Recommendation`. |
| **Interfaces (contracts)** | A single internal function or module boundary, e.g. `list_restaurants() → DataFrame/table`, `filter_candidates(prefs) → list[Restaurant]`, `recommend(prefs, candidates) → list[Recommendation]`. |
| **Exit criteria** | Empty or stub implementations compile/run; schemas documented in code. When you add HTTP in a later phase, document OpenAPI or equivalent so the web UI and backend share the same payload shape. |

---

## Phase 1 — Data Ingestion & Restaurant Store

**Maps to:** Problem statement §1 (Data ingestion).

| Item | Description |
|------|-------------|
| **Scope** | Load [ManikaSaini/zomato-restaurant-recommendation](https://huggingface.co/datasets/ManikaSaini/zomato-restaurant-recommendation); clean types; handle nulls; map raw columns to your canonical `Restaurant` model. |
| **Components** | **Loader** (HF `datasets` or cached CSV/Parquet); **Normalizer** (city/area strings, cuisine lists, numeric rating, cost buckets); **Store** (in-memory for MVP, or SQLite/DuckDB if you need persistence and SQL filters). |
| **Cross-cutting** | Pin dataset revision or snapshot hash so “repeatable pipeline” from the problem statement is achievable. |
| **Exit criteria** | All rows pass validation; you can query by location/cuisine/cost/rating in tests; documented field mapping from raw → canonical. |

---

## Phase 2 — Preferences, Filtering & Candidate Cap

**Maps to:** §2 (User input) + hard constraints in §3 (Integration layer).

| Item | Description |
|------|-------------|
| **Scope** | Parse and validate `UserPreferences` (location, budget band, cuisine, min rating, optional free text for downstream LLM only). **Deterministic filter** over the store: no LLM here. |
| **Components** | **Preference validator**; **Filter engine** (SQL or DataFrame/pandas/polars); **Candidate cap** (top-N by rating or hybrid score) to control LLM cost/latency per problem constraints. Implemented for this milestone under **`phase2/milestone_zomato_filter/`** (package ``milestone_zomato_filter``); ``src/milestone_zomato/filter/engine.py`` delegates to it. |
| **Exit criteria** | Unit tests: given fixed prefs and tiny fixture data, output set is stable; empty result returns a clear “no matches” path without calling the LLM. |

---

## Phase 3 — Integration & Recommendation Engine (LLM)

**Maps to:** §3 (prompt + structured context) + §4 (Recommendation engine).

| Item | Description |
|------|-------------|
| **Scope** | Build **prompt builder**: inject only the capped candidate list (table or JSON), user prefs, and strict instructions—**choose names only from the list**; no invented venues. **LLM client** with timeouts/retries; **response handler** that parses structured output (JSON schema, tool calling, or strict delimiters). |
| **Components** | `PromptTemplate` + `LlmClient` + `RecommendationParser`; optional **second pass** (repair JSON) if the model returns invalid structure. |
| **Grounding guard** | Post-parse check: every recommended `restaurant_id` or name exists in the candidate set; drop or retry on failure. |
| **Exit criteria** | Integration test with mocked LLM + one golden-file test with real API (optional, behind env flag); explanations reference concrete fields (cuisine, cost, rating, area). |

---

## Phase 4 — Output & User Experience

**Maps to:** §5 (Output display).

| Item | Description |
|------|-------------|
| **Scope** | **Basic web UI** collects prefs (same channel as Phase 0 decision) and displays ranked results; surface **name, cuisine, rating, cost**, **AI explanation** per row; loading and error states; optional summary blurb. |
| **Components** | **API layer** (REST/JSON) backing the web UI; **presentation DTO** decoupled from internal `Restaurant` to avoid leaking raw dataset quirks. |
| **Exit criteria** | Demo path: user submits prefs from the web UI → visible ranked list with explanations; accessibility basics (headings, contrast, keyboard). |

---

## Phase 5 — Hardening, Observability & Quality

**Maps to:** Success criteria + constraints in the problem statement.

| Item | Description |
|------|-------------|
| **Exit criteria** | You can answer: “How many candidates went to the LLM?” and “Are all IDs grounded?” for a sample run. |

---

## Phase 6 — Production Readiness & Health Monitoring

**Maps to:** Operational requirements for highly available services.

| Item | Description |
|------|-------------|
| **Scope** | Health and Readiness probes (`/health`, `/ready`); system metadata; security headers; graceful degradation. |
| **Components** | Health checks (data availability, LLM connectivity check); basic prometheus-style metrics (optional). |
| **Exit criteria** | Endpoints return 200 OK when data is loaded; frontend reflects system health. |

---

## Phase 7 — Deployment via Streamlit Cloud

**Maps to:** Public accessibility and zero-infrastructure demo hosting.

| Item | Description |
|------|-------------|
| **Scope** | Replace or complement the Next.js frontend with a **Streamlit app** that calls the existing FastAPI backend; deploy the Streamlit app to [Streamlit Community Cloud](https://streamlit.io/cloud) (free, no credit card). The FastAPI backend is deployed separately on [Render](https://render.com) free tier. |
| **Components** | `streamlit_app/app.py` — single-file Streamlit UI with location, budget, cuisine, and min-rating inputs; calls `POST /api/recommend` on the deployed backend URL; renders results as styled cards with name, cuisines, rating, cost bucket, and AI explanation. `streamlit_app/requirements.txt` — minimal deps (`streamlit`, `requests`). `render.yaml` — Render service config for the FastAPI backend (build command, start command, env vars). |
| **Deployment steps** | 1. Push repo to GitHub. 2. Deploy backend on Render: root dir `backend`, build `pip install -e .`, start `uvicorn milestone_zomato_api.main:app --host 0.0.0.0 --port $PORT`; set `OPENAI_API_KEY` and other env vars in Render dashboard. 3. Copy the Render public URL (e.g. `https://zomato-ai.onrender.com`) into a Streamlit secret `BACKEND_URL`. 4. Deploy `streamlit_app/` on Streamlit Community Cloud; connect GitHub repo, set root to `streamlit_app`, add secret `BACKEND_URL`. |
| **CORS update** | Add the Streamlit app's public URL to the FastAPI `allow_origins` list so browser requests are not blocked. |
| **Limitations** | Render free tier spins down after 15 min of inactivity (cold start ~30 s). Streamlit Community Cloud has a 1 GB memory limit. Both are sufficient for demos and coursework. |
| **Exit criteria** | Public URL (e.g. `https://zomato-ai.streamlit.app`) is shareable; a user can enter preferences and receive AI-ranked restaurant results without running anything locally; backend `/health` returns `{"status":"healthy"}` from Render. |

---

## Phase Dependency Summary

| Phase | Depends on | Delivers |
|-------|------------|----------|
| 0 | — | Contracts, config, skeleton |
| 1 | 0 | Normalized restaurant store |
| 2 | 1 | Deterministic ``filter_candidates`` (``phase2/milestone_zomato_filter``) |
| 3 | 2 | Grounded `recommend` with explanations |
| 4 | 3 | User-visible API/UI |
| 5 | 4 | Operable, measurable system |
| 6 | 5 | Production-ready health monitoring |
| 7 | 6 | Publicly deployed app (Streamlit Cloud + Render) |

---

## Optional: Logical Module Map (Same Phases, Folder View)

| Module | Typical responsibility |
|--------|-------------------------|
| `config/` | Env, dataset revision, LLM model name |
| `data/` | Load, normalize, validate, store |
| `preferences/` | Types + validation for user input |
| `filter/` (thin) | Re-exports Phase 2 engine from ``milestone_zomato_filter`` |
| `phase2/milestone_zomato_filter/` | Preference normalization, pandas masks, cap-K |
| `llm/` | Prompts, client, parse, grounding checks |
| `api/` + `ui/` | Phase 4: **basic web UI** sends/receives JSON aligned with Phase 0 schemas |

---

*Keep this document in sync when the problem statement changes (e.g. new preference dimensions or a different dataset).*
