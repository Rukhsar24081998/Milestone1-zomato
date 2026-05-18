"""Ranked recommendation with grounded explanation (Phase 3 output shape)."""

from __future__ import annotations

from pydantic import BaseModel, Field


class Recommendation(BaseModel):
    """One ranked pick returned to the presentation layer.

    ``restaurant_id`` must refer to a row that survived filtering (grounding guard in Phase 3).
    """

    restaurant_id: str = Field(..., description="Foreign key to :class:`~milestone_zomato.models.restaurant.Restaurant`.")
    rank: int = Field(..., ge=1, description="1-based order in the response list.")
    explanation: str = Field(
        ...,
        description="LLM-generated rationale tied to user prefs and restaurant attributes.",
    )

    model_config = {"frozen": True}
