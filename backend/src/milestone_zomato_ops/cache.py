"""In-memory recommendation cache for Phase 5."""

import hashlib
import json
from functools import wraps
from typing import Any, Callable, Dict, Optional

from milestone_zomato.models.preferences import UserPreferences
from milestone_zomato_ops.logging import MetricsLogger, Timer

class RecommendationCache:
    """Simple in-memory cache for recommendation results."""
    
    def __init__(self, max_size: int = 100):
        self._cache: Dict[str, Any] = {}
        self.max_size = max_size

    def _get_key(self, prefs: UserPreferences) -> str:
        """Generate a stable hash key for user preferences."""
        # Normalize by using model_dump_json which preserves order in newer Pydantic
        # or just sort keys manually.
        data = prefs.model_dump()
        # Ensure we don't cache based on temporary notes if needed, but here we cache everything.
        stable_str = json.dumps(data, sort_keys=True)
        return hashlib.sha256(stable_str.encode()).hexdigest()

    def get(self, prefs: UserPreferences) -> Optional[Any]:
        key = self._get_key(prefs)
        result = self._cache.get(key)
        MetricsLogger.log_metrics("cache_lookup", hit=result is not None)
        return result

    def set(self, prefs: UserPreferences, value: Any):
        if len(self._cache) >= self.max_size:
            # Simple FIFO eviction for now
            first_key = next(iter(self._cache))
            del self._cache[first_key]
        
        key = self._get_key(prefs)
        self._cache[key] = value

# Global cache instance
_GLOBAL_CACHE = RecommendationCache()

def cached_recommendation(func: Callable):
    """Decorator to wrap recommendation calls with caching."""
    @wraps(func)
    def wrapper(prefs: UserPreferences, *args, **kwargs):
        cached_val = _GLOBAL_CACHE.get(prefs)
        if cached_val is not None:
            return cached_val
        
        result = func(prefs, *args, **kwargs)
        _GLOBAL_CACHE.set(prefs, result)
        return result
    return wrapper
