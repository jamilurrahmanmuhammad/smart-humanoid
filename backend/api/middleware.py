"""API middleware for request timing and logging.

Provides structured logging and request tracking for observability.
FR Reference: NFR-001 (latency monitoring)
"""

import json
import logging
import time
import uuid
from typing import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware


class RequestTimingMiddleware(BaseHTTPMiddleware):
    """Middleware for request timing and structured logging.

    Adds:
    - X-Request-ID header for request correlation
    - X-Response-Time header with milliseconds
    - Structured JSON logging for each request

    FR Reference: NFR-001 (latency tracking)
    """

    def __init__(self, app, logger_name: str = "api.requests"):
        """Initialize middleware.

        Args:
            app: FastAPI application.
            logger_name: Logger name for request logs.
        """
        super().__init__(app)
        self.logger = logging.getLogger(logger_name)

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Process request with timing and logging.

        Args:
            request: Incoming request.
            call_next: Next middleware/handler.

        Returns:
            Response with added headers.
        """
        # Generate or extract request ID
        request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())

        # Start timing
        start_time = time.perf_counter()

        # Store request_id for use in handlers
        request.state.request_id = request_id

        try:
            # Process request
            response = await call_next(request)

            # Calculate duration
            duration_ms = (time.perf_counter() - start_time) * 1000

            # Add response headers
            response.headers["X-Request-ID"] = request_id
            response.headers["X-Response-Time"] = f"{duration_ms:.2f}ms"

            # Log request
            self._log_request(
                request=request,
                response=response,
                request_id=request_id,
                duration_ms=duration_ms,
            )

            return response

        except Exception as e:
            # Calculate duration even on error
            duration_ms = (time.perf_counter() - start_time) * 1000

            # Log error
            self._log_error(
                request=request,
                request_id=request_id,
                duration_ms=duration_ms,
                error=e,
            )
            raise

    def _log_request(
        self,
        request: Request,
        response: Response,
        request_id: str,
        duration_ms: float,
    ) -> None:
        """Log request in structured JSON format.

        Args:
            request: The HTTP request.
            response: The HTTP response.
            request_id: Request correlation ID.
            duration_ms: Request duration in milliseconds.
        """
        log_data = {
            "request_id": request_id,
            "method": request.method,
            "path": request.url.path,
            "status_code": response.status_code,
            "duration_ms": round(duration_ms, 2),
            "client_ip": self._get_client_ip(request),
        }

        # Add session_id if present in request state
        if hasattr(request.state, "session_id"):
            log_data["session_id"] = request.state.session_id

        # Log level based on status code
        if response.status_code >= 500:
            self.logger.error(json.dumps(log_data))
        elif response.status_code >= 400:
            self.logger.warning(json.dumps(log_data))
        else:
            self.logger.info(json.dumps(log_data))

    def _log_error(
        self,
        request: Request,
        request_id: str,
        duration_ms: float,
        error: Exception,
    ) -> None:
        """Log request error in structured JSON format.

        Does NOT include full stack trace or internal paths in output.

        Args:
            request: The HTTP request.
            request_id: Request correlation ID.
            duration_ms: Request duration in milliseconds.
            error: The exception that occurred.
        """
        log_data = {
            "request_id": request_id,
            "method": request.method,
            "path": request.url.path,
            "status_code": 500,
            "duration_ms": round(duration_ms, 2),
            "error_type": type(error).__name__,
            "client_ip": self._get_client_ip(request),
        }

        self.logger.error(json.dumps(log_data))

    def _get_client_ip(self, request: Request) -> str:
        """Get client IP from request, handling proxies.

        Args:
            request: The HTTP request.

        Returns:
            Client IP address.
        """
        # Check for forwarded header (behind proxy)
        forwarded = request.headers.get("X-Forwarded-For")
        if forwarded:
            return forwarded.split(",")[0].strip()
        return request.client.host if request.client else "unknown"


def sanitize_error_response(error: Exception) -> dict:
    """Sanitize error for safe client response.

    Removes sensitive information like:
    - Internal file paths
    - Stack traces
    - API keys/credentials

    Args:
        error: The exception to sanitize.

    Returns:
        Safe error dict for client response.

    FR Reference: FR-029 (sensitive error filtering)
    """
    error_msg = str(error)

    # Patterns to remove
    sensitive_patterns = [
        r"/home/[^\s]+",  # Home directory paths
        r"/app/[^\s]+",  # Application paths
        r"\.py\s+line\s+\d+",  # Python file references
        r"sk-[a-zA-Z0-9]+",  # OpenAI API keys
        r"api_key=[^\s]+",  # Generic API keys
        r"password=[^\s]+",  # Passwords
        r"secret=[^\s]+",  # Secrets
    ]

    import re
    for pattern in sensitive_patterns:
        error_msg = re.sub(pattern, "[REDACTED]", error_msg, flags=re.IGNORECASE)

    return {
        "error": "INTERNAL_ERROR",
        "message": "An internal error occurred. Please try again later.",
    }
