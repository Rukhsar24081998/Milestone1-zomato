"""Orchestration of Phase 3 LLM recommendations."""

from __future__ import annotations

import logging
from typing import List

from milestone_zomato.models.preferences import UserPreferences
from milestone_zomato.models.recommendation import Recommendation
from milestone_zomato.models.restaurant import Restaurant
from milestone_zomato_recommend.client import call_llm
from milestone_zomato_recommend.prompts import SYSTEM_PROMPT, build_user_prompt

logger = logging.getLogger(__name__)


def recommend_from_llm(prefs: UserPreferences, candidates: List[Restaurant]) -> tuple[List[Recommendation], str]:
    """Rank candidates and attach explanations using an LLM.

    Builds prompts, calls the LLM, parses the response, and runs a grounding check.
    """
    if not candidates:
        return [], "No candidates found."

    # 1. Build prompt
    user_prompt = build_user_prompt(prefs, candidates)

    # 2. Call LLM
    try:
        response = call_llm(SYSTEM_PROMPT, user_prompt)
        raw_recommendations = response.recommendations
        summary_blurb = response.summary_blurb
    except Exception as e:
        logger.error(f"Failed to fetch recommendations from LLM: {e}")
        return [], "We couldn't reach our foodie expert at the moment. Please try again later."

    # 3. Grounding Guard
    valid_ids = {r.id for r in candidates}
    grounded_recommendations = []
    
    for rec in raw_recommendations:
        if rec.restaurant_id in valid_ids:
            grounded_recommendations.append(rec)
        else:
            logger.warning(f"Hallucinated restaurant_id filtered out: {rec.restaurant_id}")

    # Re-rank if any were dropped
    for idx, rec in enumerate(grounded_recommendations):
        if rec.rank != idx + 1:
            grounded_recommendations[idx] = Recommendation(
                restaurant_id=rec.restaurant_id,
                rank=idx + 1,
                explanation=rec.explanation
            )

    return grounded_recommendations, summary_blurb
