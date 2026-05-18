"""Tests for Phase 1 normalization (no Hugging Face network)."""

from __future__ import annotations

import pytest

from milestone_zomato_ingestion.normalize import (
    cost_inr_to_bucket,
    infer_city,
    normalize_record,
    parse_approx_cost_inr,
    parse_rating,
    split_cuisines,
    stable_id_from_url,
)


@pytest.mark.parametrize(
    "raw,expected",
    [
        ("4.1/5", 4.1),
        ("4.5 / 5", 4.5),
        ("3", 3.0),
        ("-", None),
        ("NEW", None),
        (None, None),
    ],
)
def test_parse_rating(raw: object, expected: float | None) -> None:
    assert parse_rating(raw) == expected


@pytest.mark.parametrize(
    "raw,expected",
    [
        ("800", 800),
        ("1,200", 1200),
        ("RS 500", 500),
        ("?", None),
        (None, None),
    ],
)
def test_parse_cost(raw: object, expected: int | None) -> None:
    assert parse_approx_cost_inr(raw) == expected


def test_cost_bucket() -> None:
    assert cost_inr_to_bucket(400) == "low"
    assert cost_inr_to_bucket(800) == "medium"
    assert cost_inr_to_bucket(2000) == "high"


def test_split_cuisines() -> None:
    assert split_cuisines("North Indian, Chinese") == ["North Indian", "Chinese"]


def test_infer_city() -> None:
    assert infer_city("A, B, Bangalore", None) == "Bangalore"
    assert infer_city(None, "Delhi") == "Delhi"


def test_stable_id() -> None:
    assert len(stable_id_from_url("https://example.com/r/1", 0)) == 64
    assert stable_id_from_url(None, 3) == "row-3"


def test_normalize_record_sample() -> None:
    raw = {
        "url": "https://www.zomato.com/bangalore/jalsa-banashankari",
        "address": "942, Main Road, Banashankari, Bangalore",
        "name": "Jalsa",
        "online_order": "Yes",
        "book_table": "Yes",
        "rate": "4.1/5",
        "votes": 100,
        "phone": "080",
        "location": "Banashankari",
        "rest_type": "Casual Dining",
        "dish_liked": "",
        "cuisines": "North Indian, Mughlai",
        "approx_cost(for two people)": "800",
        "reviews_list": [],
        "menu_item": "",
        "listed_in(type)": "Buffet",
        "listed_in(city)": "Bangalore",
    }
    rec = normalize_record(raw, fallback_index=0)
    assert rec is not None
    assert rec["name"] == "Jalsa"
    assert rec["city"] == "Bangalore"
    assert rec["area"] == "Banashankari"
    assert rec["cuisines"] == ["North Indian", "Mughlai"]
    assert rec["rating"] == 4.1
    assert rec["cost_bucket"] == "medium"
    assert len(rec["id"]) == 64
