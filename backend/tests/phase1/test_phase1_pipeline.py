"""Phase 1 pipeline + store integration (Parquet, no HF)."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import pytest

from milestone_zomato.data.store import list_restaurants
from milestone_zomato.models.restaurant import RESTAURANT_DF_COLUMNS
from milestone_zomato_ingestion.pipeline import build_restaurants_dataframe


def _minimal_raw(
    *,
    url: str,
    name: str,
    address: str = "St, City",
    location: str = "Area",
    cuisines: str = "Italian",
    rate: str = "4.0/5",
    cost: str = "400",
    listed_city: str = "City",
) -> dict:
    return {
        "url": url,
        "address": address,
        "name": name,
        "online_order": "Yes",
        "book_table": "No",
        "rate": rate,
        "votes": 10,
        "phone": "1",
        "location": location,
        "rest_type": "Casual",
        "dish_liked": "",
        "cuisines": cuisines,
        "approx_cost(for two people)": cost,
        "reviews_list": [],
        "menu_item": "",
        "listed_in(type)": "Delivery",
        "listed_in(city)": listed_city,
    }


def test_build_dataframe_from_raw_rows() -> None:
    rows = [
        _minimal_raw(url="https://zomato.com/a", name="Place A"),
        _minimal_raw(url="https://zomato.com/b", name=""),
    ]
    df = build_restaurants_dataframe(rows)
    assert len(df) == 1
    assert list(df.columns) == RESTAURANT_DF_COLUMNS
    assert df.iloc[0]["name"] == "Place A"


def test_list_restaurants_reads_parquet(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    p = tmp_path / "r.parquet"
    df = pd.DataFrame(
        [
            {
                "id": "abc",
                "name": "N",
                "city": "Delhi",
                "area": "A",
                "cuisines": ["Chinese"],
                "cost_bucket": "low",
                "rating": 4.0,
            }
        ],
    )
    df = df.loc[:, RESTAURANT_DF_COLUMNS]
    df.to_parquet(p, index=False)

    monkeypatch.setenv("ZOMATO_RESTAURANT_CACHE_PATH", str(p))
    from milestone_zomato.config.settings import get_settings

    get_settings.cache_clear()
    try:
        out = list_restaurants()
        assert len(out) == 1
        assert out.iloc[0]["id"] == "abc"
    finally:
        get_settings.cache_clear()
