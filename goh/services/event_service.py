"""Event service — CRUD events, RSVP."""

from __future__ import annotations

import sqlite3

import structlog

from goh.domain.exceptions import ForbiddenError, NotFoundError, ValidationError
from goh.observability.timing import timed
from goh.repositories import audit_repo, event_repo

logger = structlog.get_logger(__name__)

VALID_EVENT_TYPES = {"one_shot", "campaign_session", "tournament", "meetup"}
VALID_RSVP_STATUSES = {"going", "maybe", "not_going"}


@timed
def create_event(
    db: sqlite3.Connection,
    *,
    organizer_id: int,
    title: str,
    event_type: str = "one_shot",
    description: str = "",
    location: str | None = None,
    start_time: str = "",
    end_time: str | None = None,
    min_players: int = 1,
    max_players: int | None = None,
    campaign_id: int | None = None,
) -> dict:
    if not title.strip():
        raise ValidationError("Event title cannot be empty")
    if event_type not in VALID_EVENT_TYPES:
        raise ValidationError(f"Invalid event type: {event_type}")

    event = event_repo.create(
        db, organizer_id=organizer_id, title=title, description=description,
        event_type=event_type, location=location, start_time=start_time,
        end_time=end_time, min_players=min_players, max_players=max_players,
        campaign_id=campaign_id,
    )
    audit_repo.log_action(
        db, user_id=organizer_id, action="create_event",
        resource_type="event", resource_id=event.id,
    )
    logger.info("event.created", event_id=event.id)
    return event.to_dict()


@timed
def get_event(db: sqlite3.Connection, event_id: int) -> dict:
    event = event_repo.find_by_id(db, event_id)
    if not event:
        raise NotFoundError("Event", event_id)
    result = event.to_dict()
    result["rsvps"] = [r.to_dict() for r in event_repo.get_rsvps(db, event_id)]
    result["going_count"] = event_repo.count_going(db, event_id)
    return result


@timed
def list_events(db: sqlite3.Connection, limit: int = 50, offset: int = 0) -> list[dict]:
    events = event_repo.list_all(db, limit, offset)
    return [e.to_dict() for e in events]


@timed
def list_upcoming_events(db: sqlite3.Connection, limit: int = 50, offset: int = 0) -> list[dict]:
    events = event_repo.list_upcoming(db, limit, offset)
    return [e.to_dict() for e in events]


@timed
def rsvp_event(
    db: sqlite3.Connection, event_id: int, user_id: int, status: str = "going"
) -> dict:
    if status not in VALID_RSVP_STATUSES:
        raise ValidationError(f"Invalid RSVP status: {status}")

    event = event_repo.find_by_id(db, event_id)
    if not event:
        raise NotFoundError("Event", event_id)

    rsvp = event_repo.rsvp(db, event_id, user_id, status)
    audit_repo.log_action(
        db, user_id=user_id, action="rsvp",
        resource_type="event", resource_id=event_id,
        details={"status": status},
    )
    return rsvp.to_dict()


@timed
def cancel_event(db: sqlite3.Connection, event_id: int, user_id: int) -> dict:
    event = event_repo.find_by_id(db, event_id)
    if not event:
        raise NotFoundError("Event", event_id)
    if event.organizer_id != user_id:
        raise ForbiddenError("Only the organizer can cancel an event")

    event_repo.update_status(db, event_id, "cancelled")
    audit_repo.log_action(
        db, user_id=user_id, action="cancel_event",
        resource_type="event", resource_id=event_id,
    )
    updated = event_repo.find_by_id(db, event_id)
    assert updated is not None
    return updated.to_dict()
