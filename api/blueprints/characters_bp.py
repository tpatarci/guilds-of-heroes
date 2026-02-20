"""Characters blueprint."""

from __future__ import annotations

from flask import Blueprint, current_app, g, jsonify, request

from api.middleware.auth import require_auth
from goh.services import character_service

characters_bp = Blueprint("characters", __name__, url_prefix="/api/v1/characters")


def _db():  # type: ignore[no-untyped-def]
    return current_app.get_db()  # type: ignore[attr-defined]


@characters_bp.route("", methods=["POST"])
@require_auth
def create_character():  # type: ignore[no-untyped-def]
    data = request.get_json(force=True)
    result = character_service.create_character(
        _db(), owner_id=g.user_id, name=data["name"],
        race=data.get("race", "Human"), char_class=data.get("class", "Fighter"),
        level=data.get("level", 1),
        strength=data.get("strength", 10), dexterity=data.get("dexterity", 10),
        constitution=data.get("constitution", 10), intelligence=data.get("intelligence", 10),
        wisdom=data.get("wisdom", 10), charisma=data.get("charisma", 10),
        hit_points=data.get("hit_points", 10), armor_class=data.get("armor_class", 10),
        backstory=data.get("backstory", ""),
    )
    return jsonify(result), 201


@characters_bp.route("/<int:char_id>")
def get_character(char_id: int):  # type: ignore[no-untyped-def]
    return jsonify(character_service.get_character(_db(), char_id))


@characters_bp.route("/mine")
@require_auth
def my_characters():  # type: ignore[no-untyped-def]
    return jsonify(character_service.list_characters(_db(), g.user_id))


@characters_bp.route("/<int:char_id>", methods=["PUT"])
@require_auth
def update_character(char_id: int):  # type: ignore[no-untyped-def]
    data = request.get_json(force=True)
    result = character_service.update_character(_db(), char_id, g.user_id, **data)
    return jsonify(result)


@characters_bp.route("/<int:char_id>", methods=["DELETE"])
@require_auth
def delete_character(char_id: int):  # type: ignore[no-untyped-def]
    character_service.delete_character(_db(), char_id, g.user_id)
    return jsonify({"message": "Deleted"})
