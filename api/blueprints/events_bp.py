"""Events blueprint."""

from __future__ import annotations

from flask import Blueprint, current_app, g, jsonify, request

from api.middleware.auth import require_auth
from goh.services import event_service

events_bp = Blueprint("events", __name__, url_prefix="/api/v1/events")


def _db():  # type: ignore[no-untyped-def]
    return current_app.get_db()  # type: ignore[attr-defined]


@events_bp.route("", methods=["POST"])
@require_auth
def create_event():  # type: ignore[no-untyped-def]
    data = request.get_json(force=True)
    result = event_service.create_event(
        _db(), organizer_id=g.user_id, title=data["title"],
        event_type=data.get("event_type", "one_shot"),
        description=data.get("description", ""),
        location=data.get("location"),
        start_time=data["start_time"],
        end_time=data.get("end_time"),
        min_players=data.get("min_players", 1),
        max_players=data.get("max_players"),
    )
    return jsonify(result), 201


@events_bp.route("")
def list_events():  # type: ignore[no-untyped-def]
    return jsonify(event_service.list_events(_db()))


@events_bp.route("/upcoming")
def upcoming():  # type: ignore[no-untyped-def]
    return jsonify(event_service.list_upcoming_events(_db()))


@events_bp.route("/<int:event_id>")
def get_event(event_id: int):  # type: ignore[no-untyped-def]
    return jsonify(event_service.get_event(_db(), event_id))


@events_bp.route("/<int:event_id>/rsvp", methods=["POST"])
@require_auth
def rsvp(event_id: int):  # type: ignore[no-untyped-def]
    data = request.get_json(force=True)
    result = event_service.rsvp_event(_db(), event_id, g.user_id, data.get("status", "going"))
    return jsonify(result)


@events_bp.route("/<int:event_id>/cancel", methods=["POST"])
@require_auth
def cancel(event_id: int):  # type: ignore[no-untyped-def]
    return jsonify(event_service.cancel_event(_db(), event_id, g.user_id))
