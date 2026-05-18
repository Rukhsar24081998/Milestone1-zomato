"""Deterministic candidate filtering (Phase 2 via ``milestone_zomato_filter``)."""

from __future__ import annotations

from typing import List

from milestone_zomato.models import Restaurant, UserPreferences


def filter_candidates(prefs: UserPreferences) -> List[Restaurant]:
    """Apply hard constraints and cap-K ordering over the restaurant store."""

    from milestone_zomato_filter.engine import (
        filter_candidates as _phase2_filter_candidates,
    )

    return _phase2_filter_candidates(prefs)