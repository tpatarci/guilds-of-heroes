"""Database migration runner — sequential .sql file execution."""

from __future__ import annotations

import sqlite3
from pathlib import Path

import structlog

logger = structlog.get_logger(__name__)

MIGRATIONS_DIR = Path(__file__).parent


def get_applied_migrations(db: sqlite3.Connection) -> set[str]:
    """Get set of already-applied migration filenames."""
    db.execute("""
        CREATE TABLE IF NOT EXISTS _migrations (
            id INTEGER PRIMARY KEY,
            filename TEXT NOT NULL UNIQUE,
            applied_at TEXT NOT NULL DEFAULT (datetime('now'))
        )
    """)
    rows = db.execute("SELECT filename FROM _migrations ORDER BY id").fetchall()
    return {row["filename"] for row in rows}


def get_pending_migrations(db: sqlite3.Connection) -> list[Path]:
    """Get list of migration files that haven't been applied yet."""
    applied = get_applied_migrations(db)
    sql_files = sorted(MIGRATIONS_DIR.glob("*.sql"))
    return [f for f in sql_files if f.name not in applied]


def run_migrations(db: sqlite3.Connection) -> list[str]:
    """Run all pending migrations and return list of applied filenames."""
    pending = get_pending_migrations(db)
    applied: list[str] = []

    for migration_file in pending:
        sql = migration_file.read_text(encoding="utf-8")
        logger.info("migration.applying", filename=migration_file.name)

        try:
            db.executescript(sql)
            db.execute(
                "INSERT INTO _migrations (filename) VALUES (?)",
                (migration_file.name,),
            )
            db.commit()
            applied.append(migration_file.name)
            logger.info("migration.applied", filename=migration_file.name)
        except sqlite3.Error as e:
            logger.error("migration.failed", filename=migration_file.name, error=str(e))
            raise

    return applied
