"""Notification service — list, mark read, count unread."""

from __future__ import annotations

import sqlite3

import structlog

from goh.observability.timing import timed
from goh.repositories import notification_repo

logger = structlog.get_logger(__name__)


@timed
def list_notifications(
    db: sqlite3.Connection, user_id: int, limit: int = 50, offset: int = 0
) -> list[dict]:
    notifs = notification_repo.list_for_user(db, user_id, limit, offset)
    return [n.to_dict() for n in notifs]


@timed
def count_unread(db: sqlite3.Connection, user_id: int) -> int:
    return notification_repo.count_unread(db, user_id)


@timed
def mark_read(db: sqlite3.Connection, notification_id: int, user_id: int) -> None:
    notification_repo.mark_read(db, notification_id, user_id)


@timed
def mark_all_read(db: sqlite3.Connection, user_id: int) -> None:
    notification_repo.mark_all_read(db, user_id)
