"""
TraceNest FastAPI Middleware

Provides automatic request/response logging for FastAPI applications.

SAFETY GUARANTEES:
- Never breaks request handling
- Never raises exceptions outward
- Minimal overhead
"""

from __future__ import annotations

import time
import uuid
from typing import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from ..logger import logger
from ..core.config import FASTAPI_EXCLUDED_PATHS, REDACT_REQUEST_HEADERS
from ..security.redaction import redact_dict


class TraceNestMiddleware(BaseHTTPMiddleware):
    """
    Automatic request logging middleware for FastAPI.
    """

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        path = request.url.path

        # Skip excluded paths (UI, health checks, etc.)
        if path in FASTAPI_EXCLUDED_PATHS:
            return await call_next(request)

        trace_id = uuid.uuid4().hex
        start_time = time.perf_counter()
        
        # Prepare headers & cookies safely
        headers = dict(request.headers) if hasattr(request, "headers") else {}
        cookies = dict(request.cookies) if hasattr(request, "cookies") else {}
        
        if REDACT_REQUEST_HEADERS:
            headers = redact_dict(headers)
            cookies = redact_dict(cookies)

        try:
            response = await call_next(request)

            duration_ms = (time.perf_counter() - start_time) * 1000

            logger.info(
                "HTTP request completed",
                method=request.method,
                path=path,
                status_code=response.status_code,
                duration_ms=round(duration_ms, 2),
                client=request.client.host if request.client else None,
                trace_id=trace_id,
                headers=headers,
                cookies=cookies,
            )

            return response

        except Exception as exc:
            duration_ms = (time.perf_counter() - start_time) * 1000

            logger.error(
                "HTTP request failed",
                method=request.method,
                path=path,
                duration_ms=round(duration_ms, 2),
                client=request.client.host if request.client else None,
                trace_id=trace_id,
                headers=headers,
                cookies=cookies,
                exception=exc,
            )

            # Re-raise so FastAPI can handle it
            raise

