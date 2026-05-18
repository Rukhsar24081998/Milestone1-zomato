"""Prompt construction for Phase 3 LLM recommendations."""

from __future__ import annotations

import json
from typing import List

from milestone_zomato.models.preferences import UserPreferences
from milestone_zomato.models.restaurant import Restaurant

SYSTEM_PROMPT = """You are an expert restaurant recommendation engine.
You are provided with a user's preferences and a STRICT candidate list of restaurants.
Your task is to recommend up to 10 restaurants from the candidate list that best match the user's preferences.

CRITICAL INSTRUCTIONS:
1. ONLY recommend restaurants that exist in the provided candidate list.
2. DO NOT invent or hallucinate any restaurant names or IDs.
3. Your output MUST be a JSON object containing:
   - "recommendations": A list of up to 10 recommendation objects (restaurant_id, rank, explanation).
   - "summary_blurb": A catchy, concise 2-sentence summary of the recommendations to get the user excited.
4. Provide a clear, natural-language explanation for each recommendation referencing specific fields (like cuisine, cost, rating, and location) and why it matches the user's preferences.
5. Avoid recommending the same restaurant more than once.
"""


def build_user_prompt(prefs: UserPreferences, candidates: List[Restaurant]) -> str:
    """Build the user prompt containing preferences and candidate data."""
    prefs_dict = prefs.model_dump(exclude_none=True)
    prefs_json = json.dumps(prefs_dict, indent=2)

    candidates_simplified = [
        {
            "id": r.id,
            "name": r.name,
            "city": r.city,
            "area": r.area,
            "cuisines": r.cuisines,
            "cost_bucket": r.cost_bucket,
            "rating": r.rating,
        }
        for r in candidates
    ]
    candidates_json = json.dumps(candidates_simplified, indent=2)

    return f"""USER PREFERENCES:
{prefs_json}

CANDIDATE RESTAURANTS (Choose ONLY from these):
{candidates_json}

Please provide your ranked recommendations (top 10 max). Do not repeat the same restaurant."""
