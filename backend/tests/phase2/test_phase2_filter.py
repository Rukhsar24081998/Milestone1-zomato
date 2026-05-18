"""Phase 2 deterministic filtering."""

from __future__ import annotations

import pandas as pd
import pytest

from milestone_zomato.models import UserPreferences
from milestone_zomato.models.restaurant import RESTAURANT_DF_COLUMNS
from milestone_zomato_filter.engine import filter_candidates_from_frame
from milestone_zomato_filter.matching import city_matches, coerce_cuisine_list, cuisine_matches
from milestone_zomato_ingestion.pipeline import build_restaurants_dataframe


def _raw_row(
    *,
    url: str,
    name: str,
    address: str,
    location: str,
    cuisines: str,
    rate: str,
    cost: str,
    listed_city: str,
) -> dict:
    return {
        "url": url,
        "address": address,
        "name": name,
        "online_order": "Yes",
        "book_table": "No",
        "rate": rate,
        "votes": 1,
        "phone": "1",
        "location": location,
        "rest_type": "Casual",
        "dish_liked": "",
        "cuisines": cuisines,
        "approx_cost(for two people)": cost,
        "reviews_list": [],
        "menu_item": "",
        "listed_in(type)": "X",
        "listed_in(city)": listed_city,
    }


@pytest.fixture
def sample_df() -> pd.DataFrame:
    rows = [
        _raw_row(
            url="https://z.com/a",
            name="Alpha",
            address="St, Delhi",
            location="CP",
            cuisines="Chinese, Thai",
            rate="4.5/5",
            cost="800",
            listed_city="Delhi",
        ),
        _raw_row(
            url="https://z.com/b",
            name="Beta",
            address="Rd, Delhi",
            location="GK",
            cuisines="North Indian",
            rate="4.5/5",
            cost="400",
            listed_city="Delhi",
        ),
        _raw_row(
            url="https://z.com/c",
            name="Gamma",
            address="1, Koramangala, Bangalore",
            location="Koramangala",
            cuisines="Italian",
            rate="3.0/5",
            cost="1500",
            listed_city="Bangalore",
        ),
        _raw_row(
            url="https://z.com/d",
            name="Delta",
            address="2, Indiranagar, Bangalore",
            location="Indiranagar",
            cuisines="Chinese",
            rate="",
            cost="600",
            listed_city="Bangalore",
        ),
    ]
    return build_restaurants_dataframe(rows)


def test_filter_city_and_cuisine(sample_df: pd.DataFrame) -> None:
    prefs = UserPreferences(location="Delhi", cuisine="Chinese", budget=None, min_rating=None)
    out = filter_candidates_from_frame(prefs, sample_df)
    assert len(out) == 1
    assert out[0].name == "Alpha"


def test_filter_budget(sample_df: pd.DataFrame) -> None:
    prefs = UserPreferences(location="Delhi", budget="low")
    out = filter_candidates_from_frame(prefs, sample_df)
    assert len(out) == 1
    assert out[0].name == "Beta"


def test_filter_min_rating_excludes_null_rating(sample_df: pd.DataFrame) -> None:
    prefs = UserPreferences(location="Bangalore", cuisine="Chinese", min_rating=3.0)
    out = filter_candidates_from_frame(prefs, sample_df)
    assert len(out) == 0


def test_cap_k_and_stable_sort(monkeypatch: pytest.MonkeyPatch, sample_df: pd.DataFrame) -> None:
    monkeypatch.setenv("ZOMATO_FILTER_TOP_K", "1")
    from milestone_zomato.config.settings import get_settings

    get_settings.cache_clear()
    try:
        prefs = UserPreferences(location="Delhi")
        out = filter_candidates_from_frame(prefs, sample_df)
        assert len(out) == 1
        assert out[0].name == "Alpha"
    finally:
        get_settings.cache_clear()


def test_deterministic_tie_break_same_rating(monkeypatch: pytest.MonkeyPatch) -> None:
    rows = []
    for i, letter in enumerate(["Zed", "Amy", "Bob"]):
        rows.append(
            _raw_row(
                url=f"https://z.com/x{i}",
                name=letter,
                address="X, Delhi",
                location="L",
                cuisines="Cafe",
                rate="4.0/5",
                cost="600",
                listed_city="Delhi",
            ),
        )
    df = build_restaurants_dataframe(rows)
    monkeypatch.setenv("ZOMATO_FILTER_TOP_K", "10")
    from milestone_zomato.config.settings import get_settings

    get_settings.cache_clear()
    try:
        prefs = UserPreferences(location="Delhi")
        out = filter_candidates_from_frame(prefs, df)
        names = [r.name for r in out]
        assert names == ["Amy", "Bob", "Zed"]
    finally:
        get_settings.cache_clear()


def test_matching_helpers() -> None:
    assert city_matches("New Delhi", "delhi") is True
    assert city_matches(None, "Delhi") is False
    assert cuisine_matches(["South Indian", "Chinese"], "chinese") is True
    assert coerce_cuisine_list("A, B") == ["A", "B"]


def test_filter_empty_frame() -> None:
    df = pd.DataFrame(columns=RESTAURANT_DF_COLUMNS)
    out = filter_candidates_from_frame(UserPreferences(location="Delhi"), df)
    assert out == []
