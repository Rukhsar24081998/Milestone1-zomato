"""Operational logging and metrics tracking for Phase 5."""

import logging
import time
import uuid
from contextvars import ContextVar
from typing import Optional

# Context variable to store the request ID for the current execution context
REQUEST_ID_CTX: ContextVar[str] = ContextVar("request_id", default="unknown")

logger = logging.getLogger("milestone_zomato_ops")

def get_request_id() -> str:
    """Retrieve the current request ID from context."""
    return REQUEST_ID_CTX.get()

def set_request_id(request_id: Optional[str] = None) -> str:
    """Set the request ID for the current context."""
    rid = request_id or str(uuid.uuid4())
    REQUEST_ID_CTX.set(rid)
    return rid

class MetricsLogger:
    """Helper to log structured metrics with request context."""
    
    @staticmethod
    def log_metrics(event_name: str, **metrics):
        """Log a metrics event with standard prefixes for easy parsing."""
        rid = get_request_id()
        metrics_str = " ".join([f"{k}={v}" for k, v in metrics.items()])
        logger.info(f"[METRIC] rid={rid} event={event_name} {metrics_str}")

class Timer:
    """Context manager to measure latency."""
    def __init__(self, event_name: str, **extra_metrics):
        self.event_name = event_name
        self.extra_metrics = extra_metrics
        self.start_time = 0.0

    def __enter__(self):
        self.start_time = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        latency = (time.perf_counter() - self.start_time) * 1000  # ms
        MetricsLogger.log_metrics(
            self.event_name, 
            latency_ms=f"{latency:.2f}", 
            success=exc_type is None,
            **self.extra_metrics
        )
