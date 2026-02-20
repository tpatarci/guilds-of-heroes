"""Health check service — liveness and deep checks."""

from __future__ import annotations

import sqlite3
from datetime import datetime, timezone

import structlog

from goh.observability.metrics import metrics
from goh.observability.timing import timed

logger = structlog.get_logger(__name__)


def check_basic() -> dict:
    """Basic liveness check (no DB)."""
    return {
        "status": "ok",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@timed
def check_deep(db: sqlite3.Connection) -> dict:
    """Deep health check — DB ping, WAL status, table counts, metrics."""
    result: dict = {
        "status": "ok",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "database": {},
        "metrics": {},
    }

    # DB ping
    try:
        db.execute("SELECT 1")
        result["database"]["connected"] = True
    except sqlite3.Error as e:
        result["status"] = "degraded"
        result["database"]["connected"] = False
        result["database"]["error"] = str(e)
        logger.error("health.db_ping_failed", error=str(e))
        return result

    # WAL status
    try:
        wal_row = db.execute("PRAGMA journal_mode").fetchone()
        result["database"]["journal_mode"] = wal_row["journal_mode"] if wal_row else "unknown"
    except sqlite3.Error:
        result["database"]["journal_mode"] = "unknown"

    # FK status
    try:
        fk_row = db.execute("PRAGMA foreign_keys").fetchone()
        result["database"]["foreign_keys"] = bool(
            fk_row["foreign_keys"] if fk_row else False
        )
    except sqlite3.Error:
        result["database"]["foreign_keys"] = False

    # Table counts
    try:
        tables_rows = db.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE '\\_%%' ESCAPE '\\'"
        ).fetchall()
        table_names = [row["name"] for row in tables_rows]
        result["database"]["tables"] = len(table_names)
        result["database"]["table_names"] = sorted(table_names)
    except sqlite3.Error:
        result["database"]["tables"] = 0

    # Metrics snapshot
    result["metrics"] = metrics.snapshot()

    return result
