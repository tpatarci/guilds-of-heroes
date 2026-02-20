"""User repository — raw SQL data access."""

from __future__ import annotations

import sqlite3

from goh.domain.entities.user import User


def find_by_id(db: sqlite3.Connection, user_id: int) -> User | None:
    row = db.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    return User.from_row(row) if row else None


def find_by_username(db: sqlite3.Connection, username: str) -> User | None:
    row = db.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
    return User.from_row(row) if row else None


def find_by_email(db: sqlite3.Connection, email: str) -> User | None:
    row = db.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
    return User.from_row(row) if row else None


def get_password_hash(db: sqlite3.Connection, user_id: int) -> str | None:
    row = db.execute("SELECT password_hash FROM users WHERE id = ?", (user_id,)).fetchone()
    return row["password_hash"] if row else None


def create(
    db: sqlite3.Connection,
    *,
    username: str,
    email: str,
    password_hash: str | None,
    display_name: str,
    role: str = "player",
) -> User:
    cursor = db.execute(
        """INSERT INTO users (username, email, password_hash, display_name, role)
           VALUES (?, ?, ?, ?, ?)""",
        (username, email, password_hash, display_name, role),
    )
    db.commit()
    user_id = cursor.lastrowid
    assert user_id is not None
    user = find_by_id(db, user_id)
    assert user is not None
    return user


def update_profile(
    db: sqlite3.Connection,
    user_id: int,
    *,
    display_name: str | None = None,
    bio: str | None = None,
    avatar: str | None = None,
) -> None:
    updates: list[str] = []
    params: list = []
    if display_name is not None:
        updates.append("display_name = ?")
        params.append(display_name)
    if bio is not None:
        updates.append("bio = ?")
        params.append(bio)
    if avatar is not None:
        updates.append("avatar = ?")
        params.append(avatar)
    if not updates:
        return
    updates.append("updated_at = datetime('now')")
    params.append(user_id)
    db.execute(f"UPDATE users SET {', '.join(updates)} WHERE id = ?", params)
    db.commit()


def set_role(db: sqlite3.Connection, user_id: int, role: str) -> None:
    db.execute(
        "UPDATE users SET role = ?, updated_at = datetime('now') WHERE id = ?",
        (role, user_id),
    )
    db.commit()


def verify_email(db: sqlite3.Connection, user_id: int) -> None:
    db.execute(
        "UPDATE users SET email_verified = 1, updated_at = datetime('now') WHERE id = ?",
        (user_id,),
    )
    db.commit()


def search(db: sqlite3.Connection, query: str, limit: int = 20) -> list[User]:
    pattern = f"%{query}%"
    rows = db.execute(
        """SELECT * FROM users
           WHERE username LIKE ? OR display_name LIKE ?
           ORDER BY username LIMIT ?""",
        (pattern, pattern, limit),
    ).fetchall()
    return [User.from_row(r) for r in rows]


def list_all(db: sqlite3.Connection, limit: int = 50, offset: int = 0) -> list[User]:
    rows = db.execute(
        "SELECT * FROM users ORDER BY created_at DESC LIMIT ? OFFSET ?",
        (limit, offset),
    ).fetchall()
    return [User.from_row(r) for r in rows]
