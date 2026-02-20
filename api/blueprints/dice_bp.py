"""Dice roller blueprint."""

from __future__ import annotations

from flask import Blueprint, current_app, g, jsonify, request

from api.middleware.auth import require_auth
from goh.services import dice_service

dice_bp = Blueprint("dice", __name__, url_prefix="/api/v1/dice")


def _db():  # type: ignore[no-untyped-def]
    return current_app.get_db()  # type: ignore[attr-defined]


@dice_bp.route("/roll", methods=["POST"])
@require_auth
def roll():  # type: ignore[no-untyped-def]
    data = request.get_json(force=True)
    result = dice_service.roll(
        _db(), user_id=g.user_id, expression=data["expression"],
        campaign_id=data.get("campaign_id"),
    )
    return jsonify(result)


@dice_bp.route("/history")
@require_auth
def history():  # type: ignore[no-untyped-def]
    limit = request.args.get("limit", 20, type=int)
    campaign_id = request.args.get("campaign_id", type=int)
    return jsonify(dice_service.get_history(_db(), g.user_id, limit, campaign_id))
