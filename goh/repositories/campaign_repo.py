"""Campaign repository — raw SQL data access."""

from __future__ import annotations

import sqlite3

from goh.domain.entities.campaign import Campaign, SessionLog

_CAMPAIGN_JOIN = """
    SELECT c.*, u.username as dm_username
    FROM campaigns c JOIN users u ON c.dm_id = u.id
"""


def create(
    db: sqlite3.Connection,
    *,
    dm_id: int,
    name: str,
    description: str = "",
    max_players: int = 6,
) -> Campaign:
    cursor = db.execute(
        "INSERT INTO campaigns (dm_id, name, description, max_players) VALUES (?, ?, ?, ?)",
        (dm_id, name, description, max_players),
    )
    db.commit()
    camp = find_by_id(db, cursor.lastrowid)
    assert camp is not None
    return camp


def find_by_id(db: sqlite3.Connection, campaign_id: int | None) -> Campaign | None:
    row = db.execute(f"{_CAMPAIGN_JOIN} WHERE c.id = ?", (campaign_id,)).fetchone()
    return Campaign.from_row(row) if row else None


def list_all(db: sqlite3.Connection, limit: int = 50, offset: int = 0) -> list[Campaign]:
    rows = db.execute(
        f"{_CAMPAIGN_JOIN} ORDER BY c.created_at DESC LIMIT ? OFFSET ?", (limit, offset)
    ).fetchall()
    return [Campaign.from_row(r) for r in rows]


def list_active(db: sqlite3.Connection, limit: int = 50) -> list[Campaign]:
    rows = db.execute(
        f"{_CAMPAIGN_JOIN} WHERE c.status = 'active' ORDER BY c.created_at DESC LIMIT ?", (limit,)
    ).fetchall()
    return [Campaign.from_row(r) for r in rows]


def update_status(db: sqlite3.Connection, campaign_id: int, status: str) -> None:
    db.execute(
        "UPDATE campaigns SET status = ?, updated_at = datetime('now') WHERE id = ?",
        (status, campaign_id),
    )
    db.commit()


# Members

def add_member(
    db: sqlite3.Connection, campaign_id: int, user_id: int,
    character_id: int | None = None, role: str = "player",
) -> None:
    db.execute(
        """INSERT OR IGNORE INTO campaign_members (campaign_id, user_id, character_id, role)
           VALUES (?, ?, ?, ?)""",
        (campaign_id, user_id, character_id, role),
    )
    db.commit()


def remove_member(db: sqlite3.Connection, campaign_id: int, user_id: int) -> None:
    db.execute(
        "DELETE FROM campaign_members WHERE campaign_id = ? AND user_id = ?",
        (campaign_id, user_id),
    )
    db.commit()


def get_members(db: sqlite3.Connection, campaign_id: int) -> list[dict]:
    return db.execute(
        """SELECT cm.*, u.username, u.display_name
           FROM campaign_members cm JOIN users u ON cm.user_id = u.id
           WHERE cm.campaign_id = ? ORDER BY cm.joined_at""",
        (campaign_id,),
    ).fetchall()


def is_member(db: sqlite3.Connection, campaign_id: int, user_id: int) -> bool:
    row = db.execute(
        "SELECT 1 FROM campaign_members WHERE campaign_id = ? AND user_id = ?",
        (campaign_id, user_id),
    ).fetchone()
    return row is not None


def count_members(db: sqlite3.Connection, campaign_id: int) -> int:
    row = db.execute(
        "SELECT COUNT(*) as cnt FROM campaign_members WHERE campaign_id = ?",
        (campaign_id,),
    ).fetchone()
    return row["cnt"] if row else 0


# Session Logs

def create_session_log(
    db: sqlite3.Connection,
    *,
    campaign_id: int,
    author_id: int,
    session_number: int,
    title: str,
    summary: str = "",
    session_date: str = "",
) -> SessionLog:
    cursor = db.execute(
        """INSERT INTO session_logs (campaign_id, author_id, session_number, title, summary, session_date)
           VALUES (?, ?, ?, ?, ?, ?)""",
        (campaign_id, author_id, session_number, title, summary, session_date),
    )
    db.commit()
    log = find_session_log_by_id(db, cursor.lastrowid)
    assert log is not None
    return log


def find_session_log_by_id(db: sqlite3.Connection, log_id: int | None) -> SessionLog | None:
    row = db.execute(
        """SELECT sl.*, u.username as author_username
           FROM session_logs sl JOIN users u ON sl.author_id = u.id
           WHERE sl.id = ?""",
        (log_id,),
    ).fetchone()
    return SessionLog.from_row(row) if row else None


def list_session_logs(db: sqlite3.Connection, campaign_id: int) -> list[SessionLog]:
    rows = db.execute(
        """SELECT sl.*, u.username as author_username
           FROM session_logs sl JOIN users u ON sl.author_id = u.id
           WHERE sl.campaign_id = ? ORDER BY sl.session_number""",
        (campaign_id,),
    ).fetchall()
    return [SessionLog.from_row(r) for r in rows]
