"""Phase 0: contracts, schemas, and stub pipeline."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

import pandas as pd
import pytest
from pydantic import ValidationError

from milestone_zomato import (
    Recommendation,
    Restaurant,
    UserPreferences,
    filter_candidates,
    list_restaurants,
    recommend,
)
from milestone_zomato.config import get_settings
from milestone_zomato.models.restaurant import RESTAURANT_DF_COLUMNS


def test_list_restaurants_empty_schema(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    missing = tmp_path / "nope.parquet"
    monkeypatch.setenv("ZOMATO_RESTAURANT_CACHE_PATH", str(missing))
    get_settings.cache_clear()
    try:
        df = list_restaurants()
        assert isinstance(df, pd.DataFrame)
        assert df.empty
        assert list(df.columns) == RESTAURANT_DF_COLUMNS
    finally:
        get_settings.cache_clear()


@patch("milestone_zomato.data.store.list_restaurants", return_value=pd.DataFrame(columns=RESTAURANT_DF_COLUMNS))
def test_filter_and_recommend_stubs(_mock_list: object) -> None:
    prefs = UserPreferences(location="Bangalore", budget="low", cuisine="South Indian", min_rating=4.0)
    assert filter_candidates(prefs) == []
    assert recommend(prefs, []) == ([], "No candidates found.")


def test_user_preferences_notes_max_length() -> None:
    with pytest.raises(ValidationError):
        UserPreferences(notes="x" * 4001)


def test_recommendation_rank_validation() -> None:
    with pytest.raises(ValidationError):
        Recommendation(restaurant_id="r1", rank=0, explanation="too low")


def test_restaurant_round_trip() -> None:
    r = Restaurant(
        id="1",
        name="Test Kitchen",
        city="Delhi",
        area="CP",
        cuisines=["North Indian"],
        cost_bucket="medium",
        rating=4.2,
    )
    assert r.id == "1"


def test_settings_default_dataset(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("ZOMATO_HF_DATASET", raising=False)
    get_settings.cache_clear()
    s = get_settings()
    assert "zomato" in s.hf_dataset_id.lower() or "ManikaSaini" in s.hf_dataset_id
    get_settings.cache_clear()
