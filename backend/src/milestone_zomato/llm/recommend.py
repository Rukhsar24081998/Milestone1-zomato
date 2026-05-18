"""LLM-backed ranking and explanations (Phase 3); Phase 0 stub."""

from __future__ import annotations

from typing import List

from ..models import Recommendation, Restaurant, UserPreferences


def recommend(prefs: UserPreferences, candidates: List[Restaurant]) -> tuple[List[Recommendation], str]:
    """Rank candidates and attach natural-language explanations.

    Phase 3: builds prompts, calls the configured provider, parses structured output,
    and runs grounding checks against ``candidates``.
    """
    from milestone_zomato_recommend import recommend_from_llm
    
    return recommend_from_llm(prefs, candidates)
