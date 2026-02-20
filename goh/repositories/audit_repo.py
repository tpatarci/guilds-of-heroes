"""Audit log repository — raw SQL data access."""

from __future__ import annotations

import json
import sqlite3

from goh.observability.correlation import get_correlation_id


def log_action(
    db: sqlite3.Connection,
    *,
    user_id: int | None,
    action: str,
    resource_type: str,
    resource_id: int | None = None,
    details: dict | None = None,
) -> None:
    db.execute(
        """INSERT INTO audit_log (user_id, action, resource_type, resource_id, details, correlation_id)
           VALUES (?, ?, ?, ?, ?, ?)""",
        (
            user_id,
            action,
            resource_type,
            resource_id,
            json.dumps(details) if details else None,
            get_correlation_id(),
        ),
    )
    db.commit()
