"""Character service — CRUD character sheets."""

from __future__ import annotations

import sqlite3

import structlog

from goh.domain.exceptions import ForbiddenError, NotFoundError, ValidationError
from goh.observability.timing import timed
from goh.repositories import audit_repo, character_repo

logger = structlog.get_logger(__name__)


@timed
def create_character(
    db: sqlite3.Connection,
    *,
    owner_id: int,
    name: str,
    race: str = "Human",
    char_class: str = "Fighter",
    level: int = 1,
    strength: int = 10,
    dexterity: int = 10,
    constitution: int = 10,
    intelligence: int = 10,
    wisdom: int = 10,
    charisma: int = 10,
    hit_points: int = 10,
    armor_class: int = 10,
    backstory: str = "",
    campaign_id: int | None = None,
) -> dict:
    if not name.strip():
        raise ValidationError("Character name cannot be empty")
    if level < 1 or level > 20:
        raise ValidationError("Level must be between 1 and 20")

    char = character_repo.create(
        db, owner_id=owner_id, name=name, race=race, char_class=char_class,
        level=level, strength=strength, dexterity=dexterity,
        constitution=constitution, intelligence=intelligence,
        wisdom=wisdom, charisma=charisma, hit_points=hit_points,
        armor_class=armor_class, backstory=backstory, campaign_id=campaign_id,
    )
    audit_repo.log_action(
        db, user_id=owner_id, action="create_character",
        resource_type="character", resource_id=char.id,
    )
    logger.info("character.created", character_id=char.id)
    return char.to_dict()


@timed
def get_character(db: sqlite3.Connection, char_id: int) -> dict:
    char = character_repo.find_by_id(db, char_id)
    if not char:
        raise NotFoundError("Character", char_id)
    return char.to_dict()


@timed
def list_characters(db: sqlite3.Connection, owner_id: int) -> list[dict]:
    chars = character_repo.list_by_owner(db, owner_id)
    return [c.to_dict() for c in chars]


@timed
def update_character(db: sqlite3.Connection, char_id: int, user_id: int, **fields: object) -> dict:
    char = character_repo.find_by_id(db, char_id)
    if not char:
        raise NotFoundError("Character", char_id)
    if char.owner_id != user_id:
        raise ForbiddenError("Cannot edit another user's character")

    character_repo.update(db, char_id, **fields)
    audit_repo.log_action(
        db, user_id=user_id, action="update_character",
        resource_type="character", resource_id=char_id,
    )
    updated = character_repo.find_by_id(db, char_id)
    assert updated is not None
    return updated.to_dict()


@timed
def delete_character(db: sqlite3.Connection, char_id: int, user_id: int) -> None:
    char = character_repo.find_by_id(db, char_id)
    if not char:
        raise NotFoundError("Character", char_id)
    if char.owner_id != user_id:
        raise ForbiddenError("Cannot delete another user's character")

    character_repo.delete(db, char_id)
    audit_repo.log_action(
        db, user_id=user_id, action="delete_character",
        resource_type="character", resource_id=char_id,
    )
