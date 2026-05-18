# Problem Statement: AI-Powered Restaurant Recommendation (Zomato-Inspired)

## Overview

Build an **AI-powered restaurant recommendation service** modeled on how discovery products like Zomato help users choose where to eat. The system should combine **structured restaurant data** with a **Large Language Model (LLM)** to produce suggestions that feel personalized and easy to understand—not just a filtered list.

## Goals

The application should:

1. **Accept user preferences** — for example location, budget band, cuisine, minimum rating, and optional notes (family-friendly, fast service, etc.).
2. **Use a real restaurant dataset** — grounded in actual listings, not invented venues.
3. **Use an LLM for reasoning and narrative** — rank or refine candidates and explain *why* each pick fits the user.
4. **Present results clearly** — names, cuisines, ratings, cost signals, plus short AI explanations the user can trust at a glance.

## System Workflow

### 1. Data ingestion

- Load and preprocess the Zomato-style dataset from Hugging Face: [ManikaSaini/zomato-restaurant-recommendation](https://huggingface.co/datasets/ManikaSaini/zomato-restaurant-recommendation).
- Normalize and retain fields needed for filtering and display (e.g. restaurant name, area/city, cuisine types, cost tier, rating, and any other columns useful for matching).

### 2. User input

Collect structured preferences, for example:

| Dimension | Examples |
|-----------|----------|
| Location | Delhi, Bangalore, neighborhood or city |
| Budget | Low / medium / high (aligned to your data’s cost field) |
| Cuisine | Italian, Chinese, North Indian, etc. |
| Quality bar | Minimum acceptable rating |
| Free text | “Quiet dinner,” “kid-friendly,” “under 30 minutes” |

### 3. Integration layer

- **Filter** the dataset using hard constraints (location, budget, cuisine, minimum rating) so the LLM only sees plausible candidates.
- **Shape** the remaining rows into a compact, structured snippet for the prompt (tables or bullet lists work well).
- **Prompt design**: instruct the model to rank, compare, and justify picks using only the provided data—avoid hallucinating restaurants not in the candidate set.

### 4. Recommendation engine

Use the LLM to:

- **Rank** restaurants against the stated preferences.
- **Explain** each recommendation in natural language (fit to budget, cuisine match, rating vs. alternatives).
- **Optionally** provide a short overall summary of the shortlist.

### 5. Output display

Show the **top recommendations** in a user-friendly layout. Each item should include at minimum:

- Restaurant name  
- Cuisine(s)  
- Rating  
- Estimated cost (or cost category from the dataset)  
- **AI-generated explanation** tying that row to the user’s inputs  

## Success Criteria (Suggested)

- Recommendations are **traceable** to rows from the ingested dataset after filtering.
- Explanations are **specific** (reference cuisine, cost, rating, or location) rather than generic praise.
- The pipeline is **repeatable**: same inputs and data version yield deterministic filtering; LLM outputs may vary but stay on-topic.

## Constraints to Keep in Mind

- **Grounding**: the LLM should not invent restaurants; it should choose and explain from the candidate list you pass in.
- **Latency and cost**: batch or limit candidate count before calling the model if the dataset slice is large.
- **Privacy**: if you add real user accounts later, treat preference and location data according to your product’s privacy rules.

---

*This document describes the intended product and technical flow for the milestone project; implementation details (stack, API keys, UI framework) are left to the team.*
