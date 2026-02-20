"""Users blueprint."""

from __future__ import annotations

from flask import Blueprint, current_app, g, jsonify, request

from api.middleware.auth import require_auth
from goh.services import user_service

users_bp = Blueprint("users", __name__, url_prefix="/api/v1/users")


def _db():  # type: ignore[no-untyped-def]
    return current_app.get_db()  # type: ignore[attr-defined]


@users_bp.route("")
def list_users():  # type: ignore[no-untyped-def]
    limit = request.args.get("limit", 50, type=int)
    offset = request.args.get("offset", 0, type=int)
    return jsonify(user_service.list_users(_db(), limit, offset))


@users_bp.route("/search")
def search():  # type: ignore[no-untyped-def]
    q = request.args.get("q", "")
    return jsonify(user_service.search_users(_db(), q))


@users_bp.route("/<int:user_id>")
def get_user(user_id: int):  # type: ignore[no-untyped-def]
    return jsonify(user_service.get_profile(_db(), user_id))


@users_bp.route("/<int:user_id>", methods=["PUT"])
@require_auth
def update_user(user_id: int):  # type: ignore[no-untyped-def]
    if g.user_id != user_id:
        from goh.domain.exceptions import ForbiddenError
        raise ForbiddenError("Cannot update another user's profile")
    data = request.get_json(force=True)
    result = user_service.update_profile(
        _db(), user_id, display_name=data.get("display_name"),
        bio=data.get("bio"), avatar=data.get("avatar"),
    )
    return jsonify(result)
