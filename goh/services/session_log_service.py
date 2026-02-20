"""Session log service — CRUD session logs for campaigns."""

from __future__ import annotations

import sqlite3

import structlog

from goh.domain.exceptions import ForbiddenError, NotFoundError, ValidationError
from goh.observability.timing import timed
from goh.repositories import audit_repo, campaign_repo

logger = structlog.get_logger(__name__)


@timed
def create_session_log(
    db: sqlite3.Connection,
    *,
    campaign_id: int,
    author_id: int,
    session_number: int,
    title: str,
    summary: str = "",
    session_date: str = "",
) -> dict:
    campaign = campaign_repo.find_by_id(db, campaign_id)
    if not campaign:
        raise NotFoundError("Campaign", campaign_id)
    if not campaign_repo.is_member(db, campaign_id, author_id):
        raise ForbiddenError("Must be a campaign member to create session logs")
    if not title.strip():
        raise ValidationError("Session log title cannot be empty")

    log = campaign_repo.create_session_log(
        db, campaign_id=campaign_id, author_id=author_id,
        session_number=session_number, title=title,
        summary=summary, session_date=session_date,
    )
    audit_repo.log_action(
        db, user_id=author_id, action="create_session_log",
        resource_type="session_log", resource_id=log.id,
    )
    return log.to_dict()


@timed
def list_session_logs(db: sqlite3.Connection, campaign_id: int) -> list[dict]:
    logs = campaign_repo.list_session_logs(db, campaign_id)
    return [log.to_dict() for log in logs]


@timed
def get_session_log(db: sqlite3.Connection, log_id: int) -> dict:
    log = campaign_repo.find_session_log_by_id(db, log_id)
    if not log:
        raise NotFoundError("SessionLog", log_id)
    return log.to_dict()
