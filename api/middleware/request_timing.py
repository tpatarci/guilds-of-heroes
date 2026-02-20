"""Request timing middleware — logs request duration."""

from __future__ import annotations

import time

import structlog
from flask import Flask, g, request

logger = structlog.get_logger(__name__)


def setup_request_timing(app: Flask) -> None:
    @app.before_request
    def start_timer() -> None:
        g.start_time = time.monotonic()

    @app.after_request
    def log_timing(response):  # type: ignore[no-untyped-def]
        start = getattr(g, "start_time", None)
        if start is not None:
            elapsed_ms = (time.monotonic() - start) * 1000
            log = logger.warning if elapsed_ms > 500 else logger.info
            log(
                "request.completed",
                method=request.method,
                path=request.path,
                status=response.status_code,
                duration_ms=round(elapsed_ms, 2),
            )
        return response
