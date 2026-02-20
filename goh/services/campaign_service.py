"""Campaign service — CRUD campaigns, join/leave, archive."""

from __future__ import annotations

import sqlite3

import structlog

from goh.domain.exceptions import ConflictError, ForbiddenError, NotFoundError, ValidationError
from goh.observability.timing import timed
from goh.repositories import audit_repo, campaign_repo

logger = structlog.get_logger(__name__)

VALID_STATUSES = {"active", "paused", "completed", "archived"}


@timed
def create_campaign(
    db: sqlite3.Connection,
    *,
    dm_id: int,
    name: str,
    description: str = "",
    max_players: int = 6,
) -> dict:
    if not name.strip():
        raise ValidationError("Campaign name cannot be empty")

    campaign = campaign_repo.create(db, dm_id=dm_id, name=name, description=description, max_players=max_players)
    # DM is automatically a member
    campaign_repo.add_member(db, campaign.id, dm_id, role="dm")
    audit_repo.log_action(
        db, user_id=dm_id, action="create_campaign",
        resource_type="campaign", resource_id=campaign.id,
    )
    logger.info("campaign.created", campaign_id=campaign.id)
    return campaign.to_dict()


@timed
def get_campaign(db: sqlite3.Connection, campaign_id: int) -> dict:
    campaign = campaign_repo.find_by_id(db, campaign_id)
    if not campaign:
        raise NotFoundError("Campaign", campaign_id)
    result = campaign.to_dict()
    result["members"] = campaign_repo.get_members(db, campaign_id)
    result["member_count"] = campaign_repo.count_members(db, campaign_id)
    return result


@timed
def list_campaigns(db: sqlite3.Connection, limit: int = 50, offset: int = 0) -> list[dict]:
    campaigns = campaign_repo.list_all(db, limit, offset)
    return [c.to_dict() for c in campaigns]


@timed
def join_campaign(
    db: sqlite3.Connection, campaign_id: int, user_id: int,
    character_id: int | None = None,
) -> dict:
    campaign = campaign_repo.find_by_id(db, campaign_id)
    if not campaign:
        raise NotFoundError("Campaign", campaign_id)

    if campaign.status != "active":
        raise ValidationError("Cannot join an inactive campaign")

    if campaign_repo.is_member(db, campaign_id, user_id):
        raise ConflictError("Already a member of this campaign")

    member_count = campaign_repo.count_members(db, campaign_id)
    if campaign.max_players and member_count >= campaign.max_players:
        raise ConflictError("Campaign is full")

    campaign_repo.add_member(db, campaign_id, user_id, character_id=character_id)
    audit_repo.log_action(
        db, user_id=user_id, action="join_campaign",
        resource_type="campaign", resource_id=campaign_id,
    )
    return {"joined": True, "campaign_id": campaign_id}


@timed
def leave_campaign(db: sqlite3.Connection, campaign_id: int, user_id: int) -> dict:
    campaign = campaign_repo.find_by_id(db, campaign_id)
    if not campaign:
        raise NotFoundError("Campaign", campaign_id)
    if campaign.dm_id == user_id:
        raise ForbiddenError("DM cannot leave their own campaign")

    campaign_repo.remove_member(db, campaign_id, user_id)
    audit_repo.log_action(
        db, user_id=user_id, action="leave_campaign",
        resource_type="campaign", resource_id=campaign_id,
    )
    return {"left": True, "campaign_id": campaign_id}


@timed
def archive_campaign(db: sqlite3.Connection, campaign_id: int, user_id: int) -> dict:
    campaign = campaign_repo.find_by_id(db, campaign_id)
    if not campaign:
        raise NotFoundError("Campaign", campaign_id)
    if campaign.dm_id != user_id:
        raise ForbiddenError("Only the DM can archive a campaign")

    campaign_repo.update_status(db, campaign_id, "archived")
    audit_repo.log_action(
        db, user_id=user_id, action="archive_campaign",
        resource_type="campaign", resource_id=campaign_id,
    )
    updated = campaign_repo.find_by_id(db, campaign_id)
    assert updated is not None
    return updated.to_dict()
