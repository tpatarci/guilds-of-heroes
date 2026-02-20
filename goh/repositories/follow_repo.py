"""Follow repository — raw SQL data access."""

from __future__ import annotations

import sqlite3

from goh.domain.entities.user import User


def follow(db: sqlite3.Connection, follower_id: int, following_id: int) -> None:
    db.execute(
        "INSERT OR IGNORE INTO follows (follower_id, following_id) VALUES (?, ?)",
        (follower_id, following_id),
    )
    db.commit()


def unfollow(db: sqlite3.Connection, follower_id: int, following_id: int) -> None:
    db.execute(
        "DELETE FROM follows WHERE follower_id = ? AND following_id = ?",
        (follower_id, following_id),
    )
    db.commit()


def is_following(db: sqlite3.Connection, follower_id: int, following_id: int) -> bool:
    row = db.execute(
        "SELECT 1 FROM follows WHERE follower_id = ? AND following_id = ?",
        (follower_id, following_id),
    ).fetchone()
    return row is not None


def get_followers(
    db: sqlite3.Connection, user_id: int, limit: int = 50, offset: int = 0
) -> list[User]:
    rows = db.execute(
        """SELECT u.* FROM users u
           JOIN follows f ON f.follower_id = u.id
           WHERE f.following_id = ?
           ORDER BY f.created_at DESC LIMIT ? OFFSET ?""",
        (user_id, limit, offset),
    ).fetchall()
    return [User.from_row(r) for r in rows]


def get_following(
    db: sqlite3.Connection, user_id: int, limit: int = 50, offset: int = 0
) -> list[User]:
    rows = db.execute(
        """SELECT u.* FROM users u
           JOIN follows f ON f.following_id = u.id
           WHERE f.follower_id = ?
           ORDER BY f.created_at DESC LIMIT ? OFFSET ?""",
        (user_id, limit, offset),
    ).fetchall()
    return [User.from_row(r) for r in rows]


def count_followers(db: sqlite3.Connection, user_id: int) -> int:
    row = db.execute(
        "SELECT COUNT(*) as cnt FROM follows WHERE following_id = ?", (user_id,)
    ).fetchone()
    return row["cnt"] if row else 0


def count_following(db: sqlite3.Connection, user_id: int) -> int:
    row = db.execute(
        "SELECT COUNT(*) as cnt FROM follows WHERE follower_id = ?", (user_id,)
    ).fetchone()
    return row["cnt"] if row else 0
