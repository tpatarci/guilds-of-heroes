"""Session (refresh token) repository — raw SQL data access."""

from __future__ import annotations

import sqlite3


def create(
    db: sqlite3.Connection,
    *,
    user_id: int,
    refresh_token: str,
    expires_at: str,
    user_agent: str | None = None,
    ip_address: str | None = None,
) -> int:
    cursor = db.execute(
        """INSERT INTO sessions (user_id, refresh_token, expires_at, user_agent, ip_address)
           VALUES (?, ?, ?, ?, ?)""",
        (user_id, refresh_token, expires_at, user_agent, ip_address),
    )
    db.commit()
    assert cursor.lastrowid is not None
    return cursor.lastrowid


def find_by_refresh_token(db: sqlite3.Connection, refresh_token: str) -> dict | None:
    return db.execute(
        "SELECT * FROM sessions WHERE refresh_token = ? AND revoked = 0",
        (refresh_token,),
    ).fetchone()


def revoke(db: sqlite3.Connection, refresh_token: str) -> None:
    db.execute(
        "UPDATE sessions SET revoked = 1 WHERE refresh_token = ?",
        (refresh_token,),
    )
    db.commit()


def revoke_all_for_user(db: sqlite3.Connection, user_id: int) -> None:
    db.execute(
        "UPDATE sessions SET revoked = 1 WHERE user_id = ?",
        (user_id,),
    )
    db.commit()
