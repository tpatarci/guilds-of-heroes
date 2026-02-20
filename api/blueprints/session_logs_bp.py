"""Session logs blueprint (nested under campaigns)."""

from __future__ import annotations

from flask import Blueprint, current_app, g, jsonify, request

from api.middleware.auth import require_auth
from goh.services import session_log_service

session_logs_bp = Blueprint("session_logs", __name__, url_prefix="/api/v1/campaigns")


def _db():  # type: ignore[no-untyped-def]
    return current_app.get_db()  # type: ignore[attr-defined]


@session_logs_bp.route("/<int:campaign_id>/sessions", methods=["POST"])
@require_auth
def create_session_log(campaign_id: int):  # type: ignore[no-untyped-def]
    data = request.get_json(force=True)
    result = session_log_service.create_session_log(
        _db(), campaign_id=campaign_id, author_id=g.user_id,
        session_number=data["session_number"], title=data["title"],
        summary=data.get("summary", ""), session_date=data.get("session_date", ""),
    )
    return jsonify(result), 201


@session_logs_bp.route("/<int:campaign_id>/sessions")
def list_session_logs(campaign_id: int):  # type: ignore[no-untyped-def]
    return jsonify(session_log_service.list_session_logs(_db(), campaign_id))


@session_logs_bp.route("/<int:campaign_id>/sessions/<int:log_id>")
def get_session_log(campaign_id: int, log_id: int):  # type: ignore[no-untyped-def]
    return jsonify(session_log_service.get_session_log(_db(), log_id))
