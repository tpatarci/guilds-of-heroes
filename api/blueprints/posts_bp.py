"""Posts blueprint."""

from __future__ import annotations

from flask import Blueprint, current_app, g, jsonify, request

from api.middleware.auth import require_auth
from goh.services import post_service

posts_bp = Blueprint("posts", __name__, url_prefix="/api/v1/posts")


def _db():  # type: ignore[no-untyped-def]
    return current_app.get_db()  # type: ignore[attr-defined]


@posts_bp.route("", methods=["POST"])
@require_auth
def create_post():  # type: ignore[no-untyped-def]
    data = request.get_json(force=True)
    result = post_service.create_post(
        _db(), author_id=g.user_id, content=data["content"],
        post_type=data.get("post_type", "text"), image_url=data.get("image_url"),
    )
    return jsonify(result), 201


@posts_bp.route("/<int:post_id>")
def get_post(post_id: int):  # type: ignore[no-untyped-def]
    return jsonify(post_service.get_post(_db(), post_id))


@posts_bp.route("/<int:post_id>", methods=["DELETE"])
@require_auth
def delete_post(post_id: int):  # type: ignore[no-untyped-def]
    post_service.delete_post(_db(), post_id, g.user_id)
    return jsonify({"message": "Deleted"})


@posts_bp.route("/feed")
@require_auth
def feed():  # type: ignore[no-untyped-def]
    limit = request.args.get("limit", 50, type=int)
    offset = request.args.get("offset", 0, type=int)
    return jsonify(post_service.get_feed(_db(), g.user_id, limit, offset))


@posts_bp.route("/timeline")
def timeline():  # type: ignore[no-untyped-def]
    limit = request.args.get("limit", 50, type=int)
    offset = request.args.get("offset", 0, type=int)
    return jsonify(post_service.get_timeline(_db(), limit, offset))


@posts_bp.route("/by/<int:author_id>")
def by_author(author_id: int):  # type: ignore[no-untyped-def]
    limit = request.args.get("limit", 50, type=int)
    offset = request.args.get("offset", 0, type=int)
    return jsonify(post_service.list_posts(_db(), author_id, limit, offset))
