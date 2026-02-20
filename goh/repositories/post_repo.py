"""Post repository — raw SQL data access."""

from __future__ import annotations

import sqlite3

from goh.domain.entities.post import Post

_POST_JOIN = """
    SELECT p.*, u.username as author_username,
           u.display_name as author_display_name, u.avatar as author_avatar
    FROM posts p JOIN users u ON p.author_id = u.id
"""


def create(
    db: sqlite3.Connection,
    *,
    author_id: int,
    content: str,
    post_type: str = "text",
    image_url: str | None = None,
) -> Post:
    cursor = db.execute(
        "INSERT INTO posts (author_id, content, post_type, image_url) VALUES (?, ?, ?, ?)",
        (author_id, content, post_type, image_url),
    )
    db.commit()
    post_id = cursor.lastrowid
    post = find_by_id(db, post_id)
    assert post is not None
    return post


def find_by_id(db: sqlite3.Connection, post_id: int | None) -> Post | None:
    row = db.execute(f"{_POST_JOIN} WHERE p.id = ?", (post_id,)).fetchone()
    return Post.from_row(row) if row else None


def list_by_author(
    db: sqlite3.Connection, author_id: int, limit: int = 50, offset: int = 0
) -> list[Post]:
    rows = db.execute(
        f"{_POST_JOIN} WHERE p.author_id = ? ORDER BY p.created_at DESC LIMIT ? OFFSET ?",
        (author_id, limit, offset),
    ).fetchall()
    return [Post.from_row(r) for r in rows]


def feed(
    db: sqlite3.Connection, user_id: int, limit: int = 50, offset: int = 0
) -> list[Post]:
    """Get posts from followed users + own posts, sorted by newest."""
    rows = db.execute(
        f"""{_POST_JOIN}
        WHERE p.author_id IN (
            SELECT following_id FROM follows WHERE follower_id = ?
            UNION SELECT ?
        )
        ORDER BY p.created_at DESC LIMIT ? OFFSET ?""",
        (user_id, user_id, limit, offset),
    ).fetchall()
    return [Post.from_row(r) for r in rows]


def timeline(db: sqlite3.Connection, limit: int = 50, offset: int = 0) -> list[Post]:
    """Global timeline — all posts, newest first."""
    rows = db.execute(
        f"{_POST_JOIN} ORDER BY p.created_at DESC LIMIT ? OFFSET ?",
        (limit, offset),
    ).fetchall()
    return [Post.from_row(r) for r in rows]


def delete(db: sqlite3.Connection, post_id: int) -> None:
    db.execute("DELETE FROM posts WHERE id = ?", (post_id,))
    db.commit()
