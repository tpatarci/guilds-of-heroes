"""Follow service — follow/unfollow, followers/following lists."""

from __future__ import annotations

import sqlite3

import structlog

from goh.domain.exceptions import NotFoundError, ValidationError
from goh.observability.timing import timed
from goh.repositories import audit_repo, follow_repo, notification_repo, user_repo

logger = structlog.get_logger(__name__)


@timed
def follow_user(db: sqlite3.Connection, follower_id: int, following_id: int) -> dict:
    if follower_id == following_id:
        raise ValidationError("Cannot follow yourself")

    target = user_repo.find_by_id(db, following_id)
    if not target:
        raise NotFoundError("User", following_id)

    already = follow_repo.is_following(db, follower_id, following_id)
    follow_repo.follow(db, follower_id, following_id)

    if not already:
        follower = user_repo.find_by_id(db, follower_id)
        follower_name = follower.display_name if follower else "Someone"
        notification_repo.create(
            db,
            user_id=following_id,
            type="follow",
            title=f"{follower_name} started following you",
            link=f"/users/{follower_id}",
            source_user_id=follower_id,
        )
        audit_repo.log_action(
            db, user_id=follower_id, action="follow", resource_type="follow",
            details={"following_id": following_id},
        )
        logger.info("follow.created", follower_id=follower_id, following_id=following_id)

    return {"following": True}


@timed
def unfollow_user(db: sqlite3.Connection, follower_id: int, following_id: int) -> dict:
    follow_repo.unfollow(db, follower_id, following_id)
    audit_repo.log_action(
        db, user_id=follower_id, action="unfollow", resource_type="follow",
        details={"following_id": following_id},
    )
    logger.info("follow.removed", follower_id=follower_id, following_id=following_id)
    return {"following": False}


@timed
def get_followers(
    db: sqlite3.Connection, user_id: int, limit: int = 50, offset: int = 0
) -> list[dict]:
    users = follow_repo.get_followers(db, user_id, limit, offset)
    return [u.to_public_dict() for u in users]


@timed
def get_following(
    db: sqlite3.Connection, user_id: int, limit: int = 50, offset: int = 0
) -> list[dict]:
    users = follow_repo.get_following(db, user_id, limit, offset)
    return [u.to_public_dict() for u in users]


@timed
def check_following(db: sqlite3.Connection, follower_id: int, following_id: int) -> bool:
    return follow_repo.is_following(db, follower_id, following_id)
