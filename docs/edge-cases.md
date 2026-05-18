# Edge Cases: AI Restaurant Recommendation

This catalog aligns with the [problem statement](./problemstatement.md) (workflow, success criteria, constraints) and [phase-wise architecture](./phase-wise-architecture.md) (Phases 0–5). Use it for test design, prompts, and incident review.

**Legend**

| Severity | Meaning |
|----------|---------|
| **P0** | Wrong answers, leaks, or system failure |
| **P1** | Bad UX, wasted cost, or silent quality degradation |
| **P2** | Niche input or operational corner case |

Each item: **Scenario** → **Expected / mitigation** (what the product or pipeline should do).

---

## 1. Phase 0 — Foundation, config, contracts

| ID | Severity | Scenario | Expected / mitigation |
|-----|----------|----------|------------------------|
| E0.1 | P0 | Missing or invalid `OPENAI_API_KEY` / provider config at startup | Fail fast with clear message; do not partially start serving LLM routes. |
| E0.2 | P0 | Wrong dataset ID or revoked HF token | Loader fails with actionable error; optional offline cache path documented. |
| E0.3 | P1 | Env mixes dev/prod model names | Single source of truth in config; log model + dataset revision per request (Phase 5). |
| E0.4 | P1 | `Restaurant` schema in code does not match normalized store | Contract tests on sample rows; CI fails on drift. |
| E0.5 | P2 | Notebook code path vs packaged module path diverge | Shared library only; no duplicate normalization logic. |

---

## 2. Phase 1 — Data ingestion & restaurant store

These affect **traceability** and **repeatability** from the problem statement.

### 2.1 Source, network, and caching

| ID | Severity | Scenario | Expected / mitigation |
|-----|----------|----------|------------------------|
| E1.1 | P0 | Hugging Face download times out or rate-limits | Retry with backoff; clear user/system error; support local snapshot path. |
| E1.2 | P1 | Dataset revision changes between runs (unpinned) | Pin revision hash in config; log revision; document how to bump. |
| E1.3 | P1 | Partial download / corrupt cache file | Checksum or row-count sanity check; refuse to serve if validation fails. |
| E1.4 | P2 | Disk full while writing cache | Catch IO error; surface failure; avoid half-written DB. |

### 2.2 Schema and types

| ID | Severity | Scenario | Expected / mitigation |
|-----|----------|----------|------------------------|
| E1.5 | P0 | Unexpected column rename or drop in upstream dataset | Versioned loader + explicit column map; fail if required columns missing. |
| E1.6 | P1 | Rating stored as string (`"4.2"`, `"4,2"`, `"N/A"`) | Parse/coerce rules; quarantine or drop rows that cannot coerce; count in metrics. |
| E1.7 | P1 | Cost as free text (`"$$"`, `"moderate"`, `"500 for two"`) | Normalize to canonical low/medium/high or numeric band; document mapping table. |
| E1.8 | P1 | Multiple currency or cost semantics in same column | Treat as opaque display + single normalized bucket per business rule. |
| E1.9 | P2 | Duplicate restaurant rows (same name, different IDs) | Dedup policy: keep highest rating, or keep both with stable IDs; filtering must stay deterministic. |

### 2.3 Nulls, empties, and bad rows

| ID | Severity | Scenario | Expected / mitigation |
|-----|----------|----------|------------------------|
| E1.10 | P0 | `name` null or empty | Exclude from store or assign synthetic key only for debugging—never recommend without display name. |
| E1.11 | P1 | `location` / city null | Row excluded from location-based filter OR tagged “unknown”; document behavior. |
| E1.12 | P1 | Cuisine null or `[]` | Exclude from cuisine filter or match “any” only if product allows; avoid false positives. |
| E1.13 | P1 | Rating null | Exclude from “min rating” filter; decide whether they appear when user does not set min rating. |
| E1.14 | P2 | Whitespace-only strings (`"  "`) | Trim on ingest; treat as empty after trim. |

### 2.4 Normalization (strings, cuisine lists)

| ID | Severity | Scenario | Expected / mitigation |
|-----|----------|----------|------------------------|
| E1.15 | P1 | City aliases (`"Bengaluru"` vs `"Bangalore"`, casing) | Canonical city map + casefold; tests for known aliases. |
| E1.16 | P1 | Cuisine as comma-separated vs JSON array vs pipe-separated | Single parser producing `list[str]` of trimmed tokens. |
| E1.17 | P1 | Composite cuisines (`"Chinese, Thai"`) vs user asking for `"Chinese"` | Token contains or set intersection; document matching rule. |
| E1.18 | P2 | Very long cuisine string (KB of text) | Truncate at ingest or cap tokens; avoid prompt blow-up. |
| E1.19 | P2 | Unicode normalization (NFC vs NFD) for matching | Normalize Unicode before equality checks. |

### 2.5 Scale and storage

| ID | Severity | Scenario | Expected / mitigation |
|-----|----------|----------|------------------------|
| E1.20 | P1 | Entire dataset loaded into RAM on small machine | Streaming/chunked load or DB index; document memory profile. |
| E1.21 | P2 | SQLite locked under concurrent writes | Read-only store for MVP; or WAL mode + timeout. |

---

## 3. Phase 2 — User preferences, filtering, candidate cap

Maps to **user input** + **hard constraints** before the LLM.

### 3.1 Missing or partial preferences

| ID | Severity | Scenario | Expected / mitigation |
|-----|----------|----------|------------------------|
| E2.1 | P1 | User omits location | Reject with validation error **or** explicit “all cities” mode with warning and stricter cap-K. |
| E2.2 | P1 | User omits cuisine | Same as above: validation vs “any cuisine” with documented default. |
| E2.3 | P2 | User omits min rating | Treat as `0` or “no minimum”—document; do not silently apply a hidden floor. |
| E2.4 | P1 | Only free-text field filled, structured fields empty | Decide product rule: reject **or** run retrieval on text only (out of scope for strict milestone—then document). |

### 3.2 Malformed or hostile input

| ID | Severity | Scenario | Expected / mitigation |
|-----|----------|----------|------------------------|
| E2.5 | P0 | Extremely long free-text (prompt injection, megabytes of text) | Hard max length; truncate server-side; never echo raw into logs unbounded. |
| E2.6 | P0 | Free-text instructs model to ignore system prompt (“ignore previous instructions…”) | System/developer message boundaries; preference text in quoted user section only; strip/control repeated control chars. |
| E2.7 | P1 | SQL or NoSQL injection if prefs pass to raw query | Parameterized queries / ORM; no string concat for predicates. |
| E2.8 | P1 | Wrong JSON types (`rating_min: "3"`) | Schema validation; coerce only where safe with explicit rules. |
| E2.9 | P2 | Surrogate pairs / emoji in location | Accept after normalization or reject with friendly message. |

### 3.3 Semantics of filters

| ID | Severity | Scenario | Expected / mitigation |
|-----|----------|----------|------------------------|
| E2.10 | P1 | Budget “high” but user min rating so high that zero rows match | Empty result path: **no LLM call**; message “Try relaxing X.” |
| E2.11 | P1 | Cuisine typo (`"Chineese"`) | Fuzzy match (optional) vs no results; avoid silently matching wrong cuisine. |
| E2.12 | P1 | User selects cuisine not present in dataset for that city | Empty set + clear copy; optional “nearby cities” product feature (explicit). |
| E2.13 | P1 | Min rating `5.0` when data max is `4.9` | Empty result or clarify scale (e.g. out of 5 vs 10). |
| E2.14 | P2 | Floating-point rating comparisons (`3.699999`) | Compare with tolerance or round consistently. |

### 3.4 Candidate cap and ordering

| ID | Severity | Scenario | Expected / mitigation |
|-----|----------|----------|------------------------|
| E2.15 | P1 | Filter returns 10,000 rows; cap-K is 20 | Deterministic tie-break (e.g. rating desc, name asc) so tests are stable. |
| E2.16 | P1 | All ratings equal under cap logic | Stable secondary sort key (id/name). |
| E2.17 | P2 | K larger than filtered set | Pass all; prompt size still under token budget. |

---

## 4. Phase 3 — Prompt builder, LLM, parse, grounding

Maps to **grounding**, **latency/cost**, and **explanation quality**.

### 4.1 Prompt construction

| ID | Severity | Scenario | Expected / mitigation |
|-----|----------|----------|------------------------|
| E3.1 | P0 | Candidate table exceeds model context window | Enforce max tokens: reduce K, summarize columns, or two-stage retrieve-then-rerank. |
| E3.2 | P1 | Restaurant name contains quotes or newlines | Escape for JSON/Markdown; stable `restaurant_id` in prompt beats name-only matching. |
| E3.3 | P1 | Duplicate display names in candidate list | IDs mandatory in prompt and in model output schema. |
| E3.4 | P2 | Non-English names or mixed scripts | UTF-8 end-to-end; no mangling in CSV intermediate. |

### 4.2 LLM API behavior

| ID | Severity | Scenario | Expected / mitigation |
|-----|----------|----------|------------------------|
| E3.5 | P0 | 401/403 from provider | No retry loop that burns quota; surface auth failure. |
| E3.6 | P1 | 429 rate limit | Exponential backoff + max retries; return 503 with Retry-After if HTTP API. |
| E3.7 | P1 | 5xx or timeout mid-stream | Idempotent or safe retry (same request id); avoid double-charging user-visible duplicate lists without dedup. |
| E3.8 | P1 | Empty completion | Fallback: deterministic order from filter + generic explanation template **or** retry once with stricter JSON instruction. |
| E3.9 | P2 | Model returns natural language only, no JSON | Parser repair pass or constrained decoding / tool use. |

### 4.3 Structured output and parsing

| ID | Severity | Scenario | Expected / mitigation |
|-----|----------|----------|------------------------|
| E3.10 | P0 | JSON with trailing commentary (`}\n\nHope this helps`) | Extract first JSON object; reject if ambiguous. |
| E3.11 | P1 | Valid JSON but wrong shape (missing `explanation`) | Schema validation; reject item or whole response per policy. |
| E3.12 | P1 | Rankings reference 12 items but only 5 requested | Cap displayed results; enforce `top_n` in post-process. |
| E3.13 | P2 | Explanations in wrong language | Prompt locale instruction + optional detector (product decision). |

### 4.4 Grounding and hallucination

| ID | Severity | Scenario | Expected / mitigation |
|-----|----------|----------|------------------------|
| E3.14 | P0 | Model recommends restaurant not in candidate list | **Grounding guard**: drop invalid IDs; if too few left, retry with reminder or fall back to filter-only ranking. |
| E3.15 | P0 | Model invents rating or cost not in data | Merge display fields **only** from store by ID; ignore numeric claims in prose for UI numbers. |
| E3.16 | P1 | Model copies user free-text as “fact” about venue | UI labels AI text; do not show unverified claims as structured fields. |
| E3.17 | P1 | Model picks valid ID but explanation cites wrong cuisine | Optional consistency check: explanation must mention at least one true attribute (heuristic) or human QA rubric. |

---

## 5. Phase 4 — Output, API, UX

Maps to required fields: **name, cuisine, rating, cost, explanation**.

| ID | Severity | Scenario | Expected / mitigation |
|-----|----------|----------|------------------------|
| E4.1 | P1 | LLM returns fewer grounded items than requested | Show available; message “Showing N of M requested.” |
| E4.2 | P1 | Explanation contains PII from prompt echo | Sanitize or shorten; do not log full prompts in production without redaction. |
| E4.3 | P1 | Markdown in explanation breaks UI (XSS) if rendered as HTML | Escape or use safe renderer; `textContent` only if web. |
| E4.4 | P2 | Very long explanation overflows layout | CSS clamp / “Read more”; server max length. |
| E4.5 | P2 | Screen reader: list order vs visual order | DOM order matches rank; announce loading and errors. |
| E4.6 | P1 | API returns 200 with empty list and no error code | Use explicit `reason: "no_matches"` vs `reason: "ok"` in payload. |
| E4.7 | P2 | Concurrent two tabs, different prefs, shared client cache | Cache key includes prefs hash + data revision. |

---

## 6. Phase 5 — Hardening, observability, ops

| ID | Severity | Scenario | Expected / mitigation |
|-----|----------|----------|------------------------|
| E5.1 | P1 | Logs contain full prompts with addresses or user notes | Redact or hash sensitive substrings; retention policy. |
| E5.2 | P1 | Cache serves stale recommendations after data refresh | Include dataset revision in cache key. |
| E5.3 | P2 | Clock skew breaks log correlation | UTC timestamps; request IDs. |
| E5.4 | P0 | Public endpoint with no rate limit | Abuse → cost spike; add basic IP/user limits for demo deploys. |

---

## 7. Privacy and compliance (future-facing)

Per problem statement **privacy** note.

| ID | Severity | Scenario | Expected / mitigation |
|-----|----------|----------|------------------------|
| E7.1 | P0 | Storing raw free-text without purpose/consent | MVP: state retention policy; minimize stored prefs; prefer ephemeral. |
| E7.2 | P1 | Analytics events include exact user location strings | Aggregate city or use coarse bucket. |
| E7.3 | P2 | GDPR/CCPA delete request | If you persist profiles: deletion path for prefs and logs. |

---

## 8. Cross-cutting: success criteria checks

Use these as **acceptance tests** tied to the problem statement.

| Criterion | Edge-driven checks |
|-----------|-------------------|
| **Traceable** | E3.14–E3.15, E1.10, E2.15–E2.17 (IDs stable through pipeline). |
| **Specific explanations** | E3.16–E3.17, E4.4 (length vs usefulness). |
| **Repeatable filtering** | E1.2, E1.9, E2.14–E2.16 (determinism). |
| **Grounding** | E3.14, E2.5–E2.6, E3.2–E3.3. |
| **Latency / cost** | E2.15, E3.1, E3.5–E3.7, E5.4. |

---

## 9. Suggested test matrix (minimal)

| Bucket | Example tests |
|--------|----------------|
| Ingest | E1.5–E1.7, E1.10–E1.13, E1.15–E1.17 |
| Prefs | E2.5, E2.8, E2.10–E2.11 |
| Filter | E2.10, E2.15–E2.16 |
| LLM | Mock: E3.10–E3.12; integration (flagged): E3.14 |
| UI/API | E4.1, E4.3, E4.6 |

---

*Related: [problem statement](./problemstatement.md) · [phase-wise architecture](./phase-wise-architecture.md)*
