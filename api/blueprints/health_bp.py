"""Health check blueprint."""

from __future__ import annotations

from flask import Blueprint, current_app, jsonify

from goh.services.health_service import check_basic, check_deep

health_bp = Blueprint("health", __name__, url_prefix="/api/v1")


@health_bp.route("/health")
def health():  # type: ignore[no-untyped-def]
    return jsonify(check_basic())


@health_bp.route("/health/deep")
def health_deep():  # type: ignore[no-untyped-def]
    db = current_app.get_db()  # type: ignore[attr-defined]
    return jsonify(check_deep(db))
