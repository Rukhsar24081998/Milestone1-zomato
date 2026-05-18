"""User preference payload: intended primary source is a basic web UI posting JSON to the API."""

from __future__ import annotations

from typing import Literal, Optional

from pydantic import BaseModel, Field

BudgetBand = Literal["low", "medium", "high"]


class UserPreferences(BaseModel):
    """Structured preferences from the user.

    Optional fields follow the problem statement table; validation rules tighten in Phase 2.
    """

    location: Optional[str] = Field(
        None,
        description="City or region filter, e.g. Delhi, Bangalore.",
    )
    budget: Optional[BudgetBand] = Field(
        None,
        description="Desired spend band aligned to dataset cost.",
    )
    cuisine: Optional[str] = Field(None, description="Primary cuisine token or short phrase.")
    min_rating: Optional[float] = Field(
        default=None,
        ge=0,
        description="Minimum acceptable aggregate rating when the user sets a bar.",
    )
    notes: Optional[str] = Field(
        default=None,
        max_length=4000,
        description="Free-text hints for the LLM (Phase 3); not used in Phase 0–1 hard filters.",
    )

    model_config = {"frozen": True}
