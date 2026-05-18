"""Normalize raw dataset dict rows into canonical restaurant records."""

from __future__ import annotations

import hashlib
import re
from typing import Any, Dict, List, Optional, Tuple

from milestone_zomato.models.restaurant import CostBucket
from milestone_zomato_ingestion.mapping import (
    COL_ADDRESS,
    COL_COST,
    COL_CUISINES,
    COL_LISTED_CITY,
    COL_LOCATION,
    COL_NAME,
    COL_RATE,
    COL_URL,
    COST_LOW_MAX_EXCL,
    COST_MED_MAX_EXCL,
)


def _clean_str(value: Any) -> Optional[str]:
    if value is None:
        return None
    s = str(value).strip()
    return s or None


def parse_rating(raw: Any) -> Optional[float]:
    """Parse Zomato-style ``4.1/5`` or plain numeric strings."""
    s = _clean_str(raw)
    if s is None:
        return None
    low = s.lower()
    if low in {"nan", "-", "none", "new", "--"}:
        return None
    m = re.match(r"^\s*(\d+(?:\.\d+)?)\s*/\s*5\s*$", s, re.I)
    if m:
        return float(m.group(1))
    m = re.match(r"^\s*(\d+(?:\.\d+)?)\s*$", s)
    if m:
        return float(m.group(1))
    return None


def parse_approx_cost_inr(raw: Any) -> Optional[int]:
    """Parse ``approx_cost(for two people)`` cell to integer INR."""
    s = _clean_str(raw)
    if s is None:
        return None
    digits = re.sub(r"[^\d]", "", s)
    if not digits:
        return None
    try:
        return int(digits)
    except ValueError:
        return None


def cost_inr_to_bucket(cost: Optional[int]) -> Optional[CostBucket]:
    if cost is None:
        return None
    if cost < COST_LOW_MAX_EXCL:
        return "low"
    if cost < COST_MED_MAX_EXCL:
        return "medium"
    return "high"


def split_cuisines(raw: Any) -> List[str]:
    s = _clean_str(raw)
    if s is None:
        return []
    parts = [p.strip() for p in s.split(",")]
    return [p for p in parts if p]


def infer_city(address: Optional[str], listed_in_city: Optional[str]) -> Optional[str]:
    """Infer display city: prefer last segment of full address, else listed_in(city)."""
    addr = _clean_str(address)
    if addr:
        parts = [p.strip() for p in addr.split(",") if p.strip()]
        if parts:
            return parts[-1]
    return _clean_str(listed_in_city)


def stable_id_from_url(url: Optional[str], fallback_index: int) -> str:
    u = _clean_str(url)
    if u:
        return hashlib.sha256(u.encode("utf-8")).hexdigest()
    return f"row-{fallback_index}"


def normalize_record(raw: Dict[str, Any], fallback_index: int = 0) -> Optional[Dict[str, Any]]:
    """Return one canonical row dict for the store DataFrame, or ``None`` to skip."""
    name = _clean_str(raw.get(COL_NAME))
    if not name:
        return None

    rid = stable_id_from_url(raw.get(COL_URL), fallback_index)
    city = infer_city(raw.get(COL_ADDRESS), raw.get(COL_LISTED_CITY))
    area = _clean_str(raw.get(COL_LOCATION))
    cuisines = split_cuisines(raw.get(COL_CUISINES))
    rating = parse_rating(raw.get(COL_RATE))
    cost_inr = parse_approx_cost_inr(raw.get(COL_COST))
    cost_bucket = cost_inr_to_bucket(cost_inr)

    return {
        "id": rid,
        "name": name,
        "city": city,
        "area": area,
        "cuisines": cuisines,
        "cost_bucket": cost_bucket,
        "rating": rating,
    }


def validate_record(rec: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
    """Optional strict check using Pydantic model."""
    from milestone_zomato.models.restaurant import Restaurant

    try:
        Restaurant(
            id=str(rec["id"]),
            name=str(rec["name"]),
            city=rec.get("city"),
            area=rec.get("area"),
            cuisines=list(rec.get("cuisines") or []),
            cost_bucket=rec.get("cost_bucket"),
            rating=rec.get("rating"),
        )
        return True, None
    except Exception as exc:  # noqa: BLE001 — surface validation message
        return False, str(exc)
