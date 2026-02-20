"""Post service — create, list, feed, timeline, delete."""

from __future__ import annotations

import sqlite3

import structlog

from goh.domain.exceptions import ForbiddenError, NotFoundError, ValidationError
from goh.observability.timing import timed
from goh.repositories import audit_repo, post_repo

logger = structlog.get_logger(__name__)

VALID_POST_TYPES = {"text", "image", "event_share", "character_share"}


@timed
def create_post(
    db: sqlite3.Connection,
    *,
    author_id: int,
    content: str,
    post_type: str = "text",
    image_url: str | None = None,
) -> dict:
    if not content.strip():
        raise ValidationError("Post content cannot be empty")
    if post_type not in VALID_POST_TYPES:
        raise ValidationError(f"Invalid post type: {post_type}")

    post = post_repo.create(
        db, author_id=author_id, content=content,
        post_type=post_type, image_url=image_url,
    )
    audit_repo.log_action(
        db, user_id=author_id, action="create_post", resource_type="post", resource_id=post.id
    )
    logger.info("post.created", post_id=post.id, author_id=author_id)
    return post.to_dict()


@timed
def get_post(db: sqlite3.Connection, post_id: int) -> dict:
    post = post_repo.find_by_id(db, post_id)
    if not post:
        raise NotFoundError("Post", post_id)
    return post.to_dict()


@timed
def list_posts(
    db: sqlite3.Connection, author_id: int, limit: int = 50, offset: int = 0
) -> list[dict]:
    posts = post_repo.list_by_author(db, author_id, limit, offset)
    return [p.to_dict() for p in posts]


@timed
def get_feed(db: sqlite3.Connection, user_id: int, limit: int = 50, offset: int = 0) -> list[dict]:
    posts = post_repo.feed(db, user_id, limit, offset)
    return [p.to_dict() for p in posts]


@timed
def get_timeline(db: sqlite3.Connection, limit: int = 50, offset: int = 0) -> list[dict]:
    posts = post_repo.timeline(db, limit, offset)
    return [p.to_dict() for p in posts]


@timed
def delete_post(db: sqlite3.Connection, post_id: int, user_id: int) -> None:
    post = post_repo.find_by_id(db, post_id)
    if not post:
        raise NotFoundError("Post", post_id)
    if post.author_id != user_id:
        raise ForbiddenError("Cannot delete another user's post")

    post_repo.delete(db, post_id)
    audit_repo.log_action(
        db, user_id=user_id, action="delete_post", resource_type="post", resource_id=post_id
    )
    logger.info("post.deleted", post_id=post_id, user_id=user_id)
