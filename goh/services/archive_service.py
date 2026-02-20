"""Archive service — archive completed campaigns."""

from __future__ import annotations

import sqlite3

import structlog

from goh.observability.timing import timed
from goh.repositories import campaign_repo

logger = structlog.get_logger(__name__)


@timed
def archive_completed_campaigns(db: sqlite3.Connection) -> list[int]:
    """Archive all campaigns with status 'completed'. Returns list of archived campaign IDs."""
    campaigns = campaign_repo.list_all(db, limit=1000)
    archived: list[int] = []
    for c in campaigns:
        if c.status == "completed":
            campaign_repo.update_status(db, c.id, "archived")
            archived.append(c.id)
            logger.info("archive.campaign_archived", campaign_id=c.id)
    return archived
