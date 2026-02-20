"""Notifications blueprint."""

from __future__ import annotations

from flask import Blueprint, current_app, g, jsonify

from api.middleware.auth import require_auth
from goh.services import notification_service

notifications_bp = Blueprint("notifications", __name__, url_prefix="/api/v1/notifications")


def _db():  # type: ignore[no-untyped-def]
    return current_app.get_db()  # type: ignore[attr-defined]


@notifications_bp.route("")
@require_auth
def list_notifications():  # type: ignore[no-untyped-def]
    return jsonify(notification_service.list_notifications(_db(), g.user_id))


@notifications_bp.route("/unread-count")
@require_auth
def unread_count():  # type: ignore[no-untyped-def]
    return jsonify({"unread": notification_service.count_unread(_db(), g.user_id)})


@notifications_bp.route("/<int:notification_id>/read", methods=["PUT"])
@require_auth
def mark_read(notification_id: int):  # type: ignore[no-untyped-def]
    notification_service.mark_read(_db(), notification_id, g.user_id)
    return jsonify({"message": "Marked as read"})


@notifications_bp.route("/read-all", methods=["PUT"])
@require_auth
def mark_all_read():  # type: ignore[no-untyped-def]
    notification_service.mark_all_read(_db(), g.user_id)
    return jsonify({"message": "All marked as read"})
