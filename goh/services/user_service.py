"""User service — profiles, search, role management."""

from __future__ import annotations

import sqlite3

import structlog

from goh.domain.exceptions import ForbiddenError, NotFoundError, ValidationError
from goh.observability.timing import timed
from goh.repositories import audit_repo, follow_repo, user_repo

logger = structlog.get_logger(__name__)


@timed
def get_profile(db: sqlite3.Connection, user_id: int) -> dict:
    user = user_repo.find_by_id(db, user_id)
    if not user:
        raise NotFoundError("User", user_id)
    profile = user.to_public_dict()
    profile["followers_count"] = follow_repo.count_followers(db, user_id)
    profile["following_count"] = follow_repo.count_following(db, user_id)
    return profile


@timed
def update_profile(
    db: sqlite3.Connection,
    user_id: int,
    *,
    display_name: str | None = None,
    bio: str | None = None,
    avatar: str | None = None,
) -> dict:
    user = user_repo.find_by_id(db, user_id)
    if not user:
        raise NotFoundError("User", user_id)

    user_repo.update_profile(db, user_id, display_name=display_name, bio=bio, avatar=avatar)

    audit_repo.log_action(
        db, user_id=user_id, action="update_profile", resource_type="user", resource_id=user_id
    )

    updated = user_repo.find_by_id(db, user_id)
    assert updated is not None
    return updated.to_private_dict()


@timed
def set_role(db: sqlite3.Connection, admin_user_id: int, target_user_id: int, role: str) -> dict:
    admin = user_repo.find_by_id(db, admin_user_id)
    if not admin or admin.role != "admin":
        raise ForbiddenError("Only admins can change roles")

    if role not in ("player", "dm", "admin"):
        raise ValidationError(f"Invalid role: {role}")

    target = user_repo.find_by_id(db, target_user_id)
    if not target:
        raise NotFoundError("User", target_user_id)

    user_repo.set_role(db, target_user_id, role)

    audit_repo.log_action(
        db, user_id=admin_user_id, action="set_role", resource_type="user",
        resource_id=target_user_id, details={"role": role},
    )

    updated = user_repo.find_by_id(db, target_user_id)
    assert updated is not None
    return updated.to_public_dict()


@timed
def search_users(db: sqlite3.Connection, query: str, limit: int = 20) -> list[dict]:
    users = user_repo.search(db, query, limit)
    return [u.to_public_dict() for u in users]


@timed
def list_users(db: sqlite3.Connection, limit: int = 50, offset: int = 0) -> list[dict]:
    users = user_repo.list_all(db, limit, offset)
    return [u.to_public_dict() for u in users]
