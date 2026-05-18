"""Tests for Phase 4 API and Groq summary."""

from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient

from milestone_zomato_api.main import app

client = TestClient(app)


def test_ui_index_loads() -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert "Zomato AI" in response.text


@patch("milestone_zomato_api.main.generate_summary_blurb")
@patch("milestone_zomato_api.main.recommend")
@patch("milestone_zomato_api.main.filter_candidates")
@patch("milestone_zomato_api.main.list_restaurants")
def test_recommend_api(
    mock_list_restaurants: MagicMock,
    mock_filter_candidates: MagicMock,
    mock_recommend: MagicMock,
    mock_generate_summary_blurb: MagicMock,
) -> None:
    import pandas as pd

    from milestone_zomato.models.recommendation import Recommendation
    from milestone_zomato.models.restaurant import Restaurant

    # Mock the pipeline components
    mock_list_restaurants.return_value = pd.DataFrame([{"id": "r1"}])
    
    mock_candidates = [
        Restaurant(
            id="r1", name="Cafe 1", city="Delhi", area="CP", cuisines=["Cafe"], cost_bucket="low", rating=4.0
        )
    ]
    mock_filter_candidates.return_value = mock_candidates
    
    mock_recommend.return_value = (
        [Recommendation(restaurant_id="r1", rank=1, explanation="Perfect match.")],
        "Expert summary"
    )
    
    mock_generate_summary_blurb.return_value = "Groq says these are awesome."

    # Call the API
    response = client.post(
        "/api/recommend",
        json={"location": "Delhi", "budget": "low", "cuisine": "Cafe"}
    )
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["summary_blurb"] == "Expert summary"
    assert len(data["results"]) == 1
    assert data["results"][0]["name"] == "Cafe 1"
    assert data["results"][0]["explanation"] == "Perfect match."
