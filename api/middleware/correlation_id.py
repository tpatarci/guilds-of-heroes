"""Correlation ID middleware — reads X-Correlation-Id or generates new."""

from __future__ import annotations

from flask import Flask, g, request

from goh.observability.correlation import new_correlation_id, set_correlation_id


def setup_correlation_id(app: Flask) -> None:
    @app.before_request
    def inject_correlation_id() -> None:
        cid = request.headers.get("X-Correlation-Id")
        if cid:
            set_correlation_id(cid)
        else:
            cid = new_correlation_id()
        g.correlation_id = cid

    @app.after_request
    def add_correlation_header(response):  # type: ignore[no-untyped-def]
        cid = getattr(g, "correlation_id", "")
        if cid:
            response.headers["X-Correlation-Id"] = cid
        return response
