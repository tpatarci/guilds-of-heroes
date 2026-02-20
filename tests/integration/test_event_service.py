"""Integration tests for event_service."""

from __future__ import annotations

import sqlite3

import pytest

from goh.domain.exceptions import ForbiddenError, ValidationError
from goh.repositories import user_repo
from goh.services import event_service


def _create_user(db: sqlite3.Connection, username: str = "dm") -> int:
    user = user_repo.create(
        db, username=username, email=f"{username}@test.com",
        password_hash="fakehash", display_name=username.title(), role="dm",
    )
    return user.id


class TestEventService:
    def test_create_event(self, db: sqlite3.Connection) -> None:
        uid = _create_user(db)
        event = event_service.create_event(
            db, organizer_id=uid, title="Dragon's Lair One-Shot",
            start_time="2026-03-01T18:00:00", max_players=5,
        )
        assert event["title"] == "Dragon's Lair One-Shot"
        assert event["organizer_username"] == "dm"

    def test_create_event_empty_title(self, db: sqlite3.Connection) -> None:
        uid = _create_user(db)
        with pytest.raises(ValidationError, match="title"):
            event_service.create_event(db, organizer_id=uid, title="  ", start_time="2026-03-01")

    def test_get_event(self, db: sqlite3.Connection) -> None:
        uid = _create_user(db)
        created = event_service.create_event(
            db, organizer_id=uid, title="Test Event", start_time="2026-03-01",
        )
        fetched = event_service.get_event(db, created["id"])
        assert fetched["title"] == "Test Event"
        assert "rsvps" in fetched
        assert "going_count" in fetched

    def test_list_events(self, db: sqlite3.Connection) -> None:
        uid = _create_user(db)
        event_service.create_event(db, organizer_id=uid, title="E1", start_time="2026-03-01")
        event_service.create_event(db, organizer_id=uid, title="E2", start_time="2026-03-02")
        events = event_service.list_events(db)
        assert len(events) == 2

    def test_rsvp(self, db: sqlite3.Connection) -> None:
        dm = _create_user(db, "dm")
        player = _create_user(db, "player")
        event = event_service.create_event(
            db, organizer_id=dm, title="Game Night", start_time="2026-03-01",
        )
        rsvp = event_service.rsvp_event(db, event["id"], player, "going")
        assert rsvp["status"] == "going"
        assert rsvp["username"] == "player"

    def test_rsvp_change_status(self, db: sqlite3.Connection) -> None:
        dm = _create_user(db, "dm")
        player = _create_user(db, "player")
        event = event_service.create_event(
            db, organizer_id=dm, title="Game Night", start_time="2026-03-01",
        )
        event_service.rsvp_event(db, event["id"], player, "going")
        rsvp = event_service.rsvp_event(db, event["id"], player, "maybe")
        assert rsvp["status"] == "maybe"

    def test_cancel_event(self, db: sqlite3.Connection) -> None:
        uid = _create_user(db)
        event = event_service.create_event(
            db, organizer_id=uid, title="Cancel Me", start_time="2026-03-01",
        )
        result = event_service.cancel_event(db, event["id"], uid)
        assert result["status"] == "cancelled"

    def test_cancel_event_not_organizer(self, db: sqlite3.Connection) -> None:
        dm = _create_user(db, "dm")
        player = _create_user(db, "player")
        event = event_service.create_event(
            db, organizer_id=dm, title="Game", start_time="2026-03-01",
        )
        with pytest.raises(ForbiddenError):
            event_service.cancel_event(db, event["id"], player)
