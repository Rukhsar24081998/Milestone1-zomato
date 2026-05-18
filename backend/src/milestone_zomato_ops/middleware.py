"""FastAPI middleware for request ID tracking and operational logging."""

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from milestone_zomato_ops.logging import set_request_id, Timer

class OperationalMiddleware(BaseHTTPMiddleware):
    """Middleware to inject request IDs and log overall request latency."""
    
    async def dispatch(self, request: Request, call_next):
        # Set a unique request ID for this thread/task
        request_id = request.headers.get("X-Request-ID")
        rid = set_request_id(request_id)
        
        # Measure total request time
        with Timer("request_total", path=request.url.path, method=request.method):
            response = await call_next(request)
            
        # Add request ID to response headers
        response.headers["X-Request-ID"] = rid
        return response
