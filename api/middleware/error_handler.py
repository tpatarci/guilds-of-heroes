"""Error handler middleware — maps AppError to HTTP responses."""

from __future__ import annotations

import structlog
from flask import Flask, g, jsonify

from goh.domain.exceptions import AppError

logger = structlog.get_logger(__name__)


def setup_error_handler(app: Flask) -> None:
    @app.errorhandler(AppError)
    def handle_app_error(error: AppError):  # type: ignore[no-untyped-def]
        response = error.to_dict()
        response["correlation_id"] = getattr(g, "correlation_id", "")
        logger.warning(
            "app_error",
            error_code=error.error_code,
            status=error.status_code,
            message=error.message,
        )
        return jsonify(response), error.status_code

    @app.errorhandler(404)
    def not_found(error):  # type: ignore[no-untyped-def]
        return jsonify({
            "error": "NOT_FOUND",
            "message": "Resource not found",
            "correlation_id": getattr(g, "correlation_id", ""),
        }), 404

    @app.errorhandler(500)
    def internal_error(error):  # type: ignore[no-untyped-def]
        logger.error("internal_error", error=str(error))
        return jsonify({
            "error": "INTERNAL_ERROR",
            "message": "Internal server error",
            "correlation_id": getattr(g, "correlation_id", ""),
        }), 500
