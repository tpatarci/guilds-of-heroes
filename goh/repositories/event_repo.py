"""Event and RSVP repository — raw SQL data access."""

from __future__ import annotations

import sqlite3

from goh.domain.entities.event import RSVP, Event

_EVENT_JOIN = """
    SELECT e.*, u.username as organizer_username
    FROM events e JOIN users u ON e.organizer_id = u.id
"""


def create(
    db: sqlite3.Connection,
    *,
    organizer_id: int,
    title: str,
    description: str = "",
    event_type: str = "one_shot",
    location: str | None = None,
    start_time: str = "",
    end_time: str | None = None,
    min_players: int = 1,
    max_players: int | None = None,
    campaign_id: int | None = None,
) -> Event:
    cursor = db.execute(
        """INSERT INTO events (organizer_id, title, description, event_type, location,
           start_time, end_time, min_players, max_players, campaign_id)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (organizer_id, title, description, event_type, location,
         start_time, end_time, min_players, max_players, campaign_id),
    )
    db.commit()
    event = find_by_id(db, cursor.lastrowid)
    assert event is not None
    return event


def find_by_id(db: sqlite3.Connection, event_id: int | None) -> Event | None:
    row = db.execute(f"{_EVENT_JOIN} WHERE e.id = ?", (event_id,)).fetchone()
    return Event.from_row(row) if row else None


def list_upcoming(db: sqlite3.Connection, limit: int = 50, offset: int = 0) -> list[Event]:
    rows = db.execute(
        f"{_EVENT_JOIN} WHERE e.status IN ('upcoming', 'ongoing') ORDER BY e.start_time ASC LIMIT ? OFFSET ?",
        (limit, offset),
    ).fetchall()
    return [Event.from_row(r) for r in rows]


def list_all(db: sqlite3.Connection, limit: int = 50, offset: int = 0) -> list[Event]:
    rows = db.execute(
        f"{_EVENT_JOIN} ORDER BY e.start_time DESC LIMIT ? OFFSET ?",
        (limit, offset),
    ).fetchall()
    return [Event.from_row(r) for r in rows]


def update_status(db: sqlite3.Connection, event_id: int, status: str) -> None:
    db.execute(
        "UPDATE events SET status = ?, updated_at = datetime('now') WHERE id = ?",
        (status, event_id),
    )
    db.commit()


def delete(db: sqlite3.Connection, event_id: int) -> None:
    db.execute("DELETE FROM events WHERE id = ?", (event_id,))
    db.commit()


# RSVP operations

def rsvp(db: sqlite3.Connection, event_id: int, user_id: int, status: str = "going") -> RSVP:
    db.execute(
        """INSERT INTO rsvps (event_id, user_id, status) VALUES (?, ?, ?)
           ON CONFLICT(event_id, user_id) DO UPDATE SET status = ?, updated_at = datetime('now')""",
        (event_id, user_id, status, status),
    )
    db.commit()
    row = db.execute(
        """SELECT r.*, u.username, u.display_name FROM rsvps r
           JOIN users u ON r.user_id = u.id
           WHERE r.event_id = ? AND r.user_id = ?""",
        (event_id, user_id),
    ).fetchone()
    assert row is not None
    return RSVP.from_row(row)


def get_rsvps(db: sqlite3.Connection, event_id: int) -> list[RSVP]:
    rows = db.execute(
        """SELECT r.*, u.username, u.display_name FROM rsvps r
           JOIN users u ON r.user_id = u.id
           WHERE r.event_id = ? ORDER BY r.created_at""",
        (event_id,),
    ).fetchall()
    return [RSVP.from_row(r) for r in rows]


def count_going(db: sqlite3.Connection, event_id: int) -> int:
    row = db.execute(
        "SELECT COUNT(*) as cnt FROM rsvps WHERE event_id = ? AND status = 'going'",
        (event_id,),
    ).fetchone()
    return row["cnt"] if row else 0
