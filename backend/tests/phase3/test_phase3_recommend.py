"""Tests for Phase 3 LLM recommendations."""

import os
from unittest.mock import MagicMock, patch

import pytest

from milestone_zomato.models.preferences import UserPreferences
from milestone_zomato.models.recommendation import Recommendation
from milestone_zomato.models.restaurant import Restaurant
from milestone_zomato_recommend.engine import recommend_from_llm
from milestone_zomato_recommend.prompts import build_user_prompt


@pytest.fixture
def mock_candidates() -> list[Restaurant]:
    return [
        Restaurant(
            id="r1", name="Cafe 1", city="Delhi", area="CP", cuisines=["Cafe"], cost_bucket="low", rating=4.0
        ),
        Restaurant(
            id="r2", name="Diner 2", city="Delhi", area="South", cuisines=["North Indian"], cost_bucket="medium", rating=4.5
        ),
    ]


@pytest.fixture
def user_prefs() -> UserPreferences:
    return UserPreferences(location="Delhi", cuisine="Cafe", budget="low", min_rating=3.5)


def test_build_user_prompt(user_prefs: UserPreferences, mock_candidates: list[Restaurant]) -> None:
    prompt = build_user_prompt(user_prefs, mock_candidates)
    assert "USER PREFERENCES" in prompt
    assert "Delhi" in prompt
    assert "Cafe 1" in prompt
    assert "Diner 2" in prompt


@patch("milestone_zomato_recommend.engine.call_llm")
def test_recommend_from_llm_success(
    mock_call_llm: MagicMock, user_prefs: UserPreferences, mock_candidates: list[Restaurant]
) -> None:
    from milestone_zomato_recommend.client import LLMRecommendationResponse
    # Mock LLM returning valid recommendation
    mock_call_llm.return_value = LLMRecommendationResponse(
        recommendations=[
            Recommendation(restaurant_id="r1", rank=1, explanation="Matches perfectly."),
        ],
        summary_blurb="Awesome picks!"
    )

    results, blurb = recommend_from_llm(user_prefs, mock_candidates)
    assert len(results) == 1
    assert results[0].restaurant_id == "r1"
    assert results[0].rank == 1
    assert blurb == "Awesome picks!"


@patch("milestone_zomato_recommend.engine.call_llm")
def test_recommend_from_llm_grounding_guard(
    mock_call_llm: MagicMock, user_prefs: UserPreferences, mock_candidates: list[Restaurant]
) -> None:
    from milestone_zomato_recommend.client import LLMRecommendationResponse
    # Mock LLM returning one valid and one hallucinated ID
    mock_call_llm.return_value = LLMRecommendationResponse(
        recommendations=[
            Recommendation(restaurant_id="r1", rank=1, explanation="Valid."),
            Recommendation(restaurant_id="fake_id", rank=2, explanation="Hallucinated."),
        ],
        summary_blurb="Validating..."
    )

    results, blurb = recommend_from_llm(user_prefs, mock_candidates)
    assert len(results) == 1
    assert results[0].restaurant_id == "r1"
    # Ensure rank is fixed
    assert results[0].rank == 1


@patch("milestone_zomato_recommend.engine.call_llm")
def test_recommend_from_llm_empty_candidates(
    mock_call_llm: MagicMock, user_prefs: UserPreferences
) -> None:
    results, blurb = recommend_from_llm(user_prefs, [])
    assert len(results) == 0
    assert blurb == "No candidates found."
    mock_call_llm.assert_not_called()


@pytest.mark.skipif(not os.getenv("OPENAI_API_KEY"), reason="OPENAI_API_KEY not set")
def test_golden_recommendation(user_prefs: UserPreferences, mock_candidates: list[Restaurant]) -> None:
    # This will actually hit OpenAI if OPENAI_API_KEY is present
    results, blurb = recommend_from_llm(user_prefs, mock_candidates)
    # The LLM should definitely pick Cafe 1 since user_prefs explicitly asks for Cafe and low budget.
    assert len(results) > 0
    assert results[0].restaurant_id in ["r1", "r2"]
