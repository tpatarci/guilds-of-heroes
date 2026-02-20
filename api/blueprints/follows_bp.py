"""Follows blueprint."""

from __future__ import annotations

from flask import Blueprint, current_app, g, jsonify

from api.middleware.auth import require_auth
from goh.services import follow_service

follows_bp = Blueprint("follows", __name__, url_prefix="/api/v1/follows")


def _db():  # type: ignore[no-untyped-def]
    return current_app.get_db()  # type: ignore[attr-defined]


@follows_bp.route("/<int:user_id>", methods=["POST"])
@require_auth
def follow(user_id: int):  # type: ignore[no-untyped-def]
    return jsonify(follow_service.follow_user(_db(), g.user_id, user_id))


@follows_bp.route("/<int:user_id>", methods=["DELETE"])
@require_auth
def unfollow(user_id: int):  # type: ignore[no-untyped-def]
    return jsonify(follow_service.unfollow_user(_db(), g.user_id, user_id))


@follows_bp.route("/<int:user_id>/followers")
def followers(user_id: int):  # type: ignore[no-untyped-def]
    return jsonify(follow_service.get_followers(_db(), user_id))


@follows_bp.route("/<int:user_id>/following")
def following(user_id: int):  # type: ignore[no-untyped-def]
    return jsonify(follow_service.get_following(_db(), user_id))
