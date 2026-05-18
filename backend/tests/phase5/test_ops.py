"""Tests for Phase 5 operational modules."""

import pytest
from unittest.mock import MagicMock
from milestone_zomato.models.preferences import UserPreferences
from milestone_zomato_ops.logging import set_request_id, get_request_id, Timer
from milestone_zomato_ops.cache import RecommendationCache

def test_request_id_context():
    rid = set_request_id("test-id")
    assert get_request_id() == "test-id"
    assert rid == "test-id"

def test_cache_logic():
    cache = RecommendationCache(max_size=2)
    prefs1 = UserPreferences(location="Delhi", budget="low")
    prefs2 = UserPreferences(location="Mumbai", budget="high")
    
    cache.set(prefs1, "result1")
    cache.set(prefs2, "result2")
    
    assert cache.get(prefs1) == "result1"
    assert cache.get(prefs2) == "result2"
    
    # Test eviction
    prefs3 = UserPreferences(location="Bangalore")
    cache.set(prefs3, "result3")
    
    # First one (Delhi) should be evicted (FIFO in my simple implementation)
    assert cache.get(prefs1) is None
    assert cache.get(prefs3) == "result3"

def test_timer_logging(caplog):
    caplog.set_level("INFO")
    with Timer("test_event", extra="data"):
        pass
    
    assert "[METRIC]" in caplog.text
    assert "event=test_event" in caplog.text
    assert "latency_ms=" in caplog.text
    assert "extra=data" in caplog.text
