"""Notification repository — raw SQL data access."""

from __future__ import annotations

import sqlite3

from goh.domain.entities.notification import Notification


def create(
    db: sqlite3.Connection,
    *,
    user_id: int,
    type: str,
    title: str,
    body: str = "",
    link: str | None = None,
    source_user_id: int | None = None,
) -> Notification:
    cursor = db.execute(
        """INSERT INTO notifications (user_id, type, title, body, link, source_user_id)
           VALUES (?, ?, ?, ?, ?, ?)""",
        (user_id, type, title, body, link, source_user_id),
    )
    db.commit()
    notif_id = cursor.lastrowid
    row = db.execute("SELECT * FROM notifications WHERE id = ?", (notif_id,)).fetchone()
    assert row is not None
    return Notification.from_row(row)


def list_for_user(
    db: sqlite3.Connection, user_id: int, limit: int = 50, offset: int = 0
) -> list[Notification]:
    rows = db.execute(
        "SELECT * FROM notifications WHERE user_id = ? ORDER BY created_at DESC LIMIT ? OFFSET ?",
        (user_id, limit, offset),
    ).fetchall()
    return [Notification.from_row(r) for r in rows]


def count_unread(db: sqlite3.Connection, user_id: int) -> int:
    row = db.execute(
        "SELECT COUNT(*) as cnt FROM notifications WHERE user_id = ? AND is_read = 0",
        (user_id,),
    ).fetchone()
    return row["cnt"] if row else 0


def mark_read(db: sqlite3.Connection, notification_id: int, user_id: int) -> None:
    db.execute(
        "UPDATE notifications SET is_read = 1 WHERE id = ? AND user_id = ?",
        (notification_id, user_id),
    )
    db.commit()


def mark_all_read(db: sqlite3.Connection, user_id: int) -> None:
    db.execute(
        "UPDATE notifications SET is_read = 1 WHERE user_id = ? AND is_read = 0",
        (user_id,),
    )
    db.commit()
