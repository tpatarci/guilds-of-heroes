"""Campaigns blueprint."""

from __future__ import annotations

from flask import Blueprint, current_app, g, jsonify, request

from api.middleware.auth import require_auth
from goh.services import campaign_service

campaigns_bp = Blueprint("campaigns", __name__, url_prefix="/api/v1/campaigns")


def _db():  # type: ignore[no-untyped-def]
    return current_app.get_db()  # type: ignore[attr-defined]


@campaigns_bp.route("", methods=["POST"])
@require_auth
def create_campaign():  # type: ignore[no-untyped-def]
    data = request.get_json(force=True)
    result = campaign_service.create_campaign(
        _db(), dm_id=g.user_id, name=data["name"],
        description=data.get("description", ""),
        max_players=data.get("max_players", 6),
    )
    return jsonify(result), 201


@campaigns_bp.route("")
def list_campaigns():  # type: ignore[no-untyped-def]
    return jsonify(campaign_service.list_campaigns(_db()))


@campaigns_bp.route("/<int:campaign_id>")
def get_campaign(campaign_id: int):  # type: ignore[no-untyped-def]
    return jsonify(campaign_service.get_campaign(_db(), campaign_id))


@campaigns_bp.route("/<int:campaign_id>/join", methods=["POST"])
@require_auth
def join_campaign(campaign_id: int):  # type: ignore[no-untyped-def]
    data = request.get_json(silent=True) or {}
    result = campaign_service.join_campaign(
        _db(), campaign_id, g.user_id, character_id=data.get("character_id"),
    )
    return jsonify(result)


@campaigns_bp.route("/<int:campaign_id>/leave", methods=["POST"])
@require_auth
def leave_campaign(campaign_id: int):  # type: ignore[no-untyped-def]
    return jsonify(campaign_service.leave_campaign(_db(), campaign_id, g.user_id))


@campaigns_bp.route("/<int:campaign_id>/archive", methods=["POST"])
@require_auth
def archive_campaign(campaign_id: int):  # type: ignore[no-untyped-def]
    return jsonify(campaign_service.archive_campaign(_db(), campaign_id, g.user_id))
