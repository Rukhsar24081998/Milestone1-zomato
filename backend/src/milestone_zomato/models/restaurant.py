"""Canonical restaurant row (post–Phase 1 normalization)."""

from __future__ import annotations

from typing import List, Literal, Optional

from pydantic import BaseModel, Field

CostBucket = Literal["low", "medium", "high"]

# Column order for :func:`milestone_zomato.data.store.list_restaurants` empty stub / future DataFrame.
RESTAURANT_DF_COLUMNS: List[str] = [
    "id",
    "name",
    "city",
    "area",
    "cuisines",
    "cost_bucket",
    "rating",
]


class Restaurant(BaseModel):
    """Single venue in the internal store.

    Field names are stable contracts for filtering (Phase 2) and LLM context (Phase 3).
    """

    id: str = Field(..., description="Stable unique id after ingestion (slug, hash, or source id).")
    name: str = Field(..., description="Display name.")
    city: Optional[str] = Field(None, description="City or primary location label.")
    area: Optional[str] = Field(None, description="Neighborhood or locality when available.")
    cuisines: List[str] = Field(default_factory=list, description="Normalized cuisine tokens.")
    cost_bucket: Optional[CostBucket] = Field(
        None,
        description="Mapped from dataset cost for two / price band (low | medium | high).",
    )
    rating: Optional[float] = Field(
        default=None,
        ge=0,
        description="Aggregate rating if present; scale follows source data (Phase 1 documents mapping).",
    )

    model_config = {"frozen": True}
