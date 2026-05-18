"""Normalize and validate :class:`~milestone_zomato.models.preferences.UserPreferences` for hard filters."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from milestone_zomato.models.preferences import BudgetBand, UserPreferences


@dataclass(frozen=True)
class EffectiveFilterPrefs:
    """Whitespace-stripped prefs; blank strings treated as unset (``None``)."""

    location: Optional[str]
    budget: Optional[BudgetBand]
    cuisine: Optional[str]
    min_rating: Optional[float]
    # notes intentionally omitted from hard filters (Phase 3)


def effective_prefs(prefs: UserPreferences) -> EffectiveFilterPrefs:
    """Derive fields used by the deterministic filter."""
    loc = prefs.location.strip() if prefs.location else None
    if loc == "":
        loc = None
    cu = prefs.cuisine.strip() if prefs.cuisine else None
    if cu == "":
        cu = None
    return EffectiveFilterPrefs(
        location=loc,
        budget=prefs.budget,
        cuisine=cu,
        min_rating=prefs.min_rating,
    )


def validate_preferences_for_filter(prefs: UserPreferences) -> None:
    """Reject prefs that violate basic rules before querying the store."""
    if prefs.min_rating is not None and prefs.min_rating < 0:
        raise ValueError("min_rating must be non-negative")
