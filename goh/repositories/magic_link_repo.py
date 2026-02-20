"""Magic link repository — raw SQL data access."""

from __future__ import annotations

import sqlite3


def create(
    db: sqlite3.Connection,
    *,
    user_id: int,
    token: str,
    expires_at: str,
) -> int:
    cursor = db.execute(
        "INSERT INTO magic_links (user_id, token, expires_at) VALUES (?, ?, ?)",
        (user_id, token, expires_at),
    )
    db.commit()
    assert cursor.lastrowid is not None
    return cursor.lastrowid


def find_by_token(db: sqlite3.Connection, token: str) -> dict | None:
    return db.execute(
        "SELECT * FROM magic_links WHERE token = ? AND used = 0",
        (token,),
    ).fetchone()


def mark_used(db: sqlite3.Connection, token: str) -> None:
    db.execute(
        "UPDATE magic_links SET used = 1 WHERE token = ?",
        (token,),
    )
    db.commit()
