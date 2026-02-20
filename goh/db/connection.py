"""SQLite connection factory with WAL mode, FK enforcement, and Row factory."""

from __future__ import annotations

import sqlite3
from pathlib import Path


def dict_factory(cursor: sqlite3.Cursor, row: tuple) -> dict:
    """Row factory that returns dicts instead of tuples."""
    columns = [col[0] for col in cursor.description]
    return dict(zip(columns, row, strict=True))


def get_connection(db_path: str | Path) -> sqlite3.Connection:
    """Create a configured SQLite connection.

    Enables WAL mode, foreign keys, and dict row factory.
    """
    db_path = str(db_path)
    conn = sqlite3.connect(db_path)
    conn.row_factory = dict_factory  # type: ignore[assignment]
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    conn.execute("PRAGMA busy_timeout=5000")
    return conn


def get_memory_connection() -> sqlite3.Connection:
    """Create an in-memory SQLite connection for testing."""
    conn = sqlite3.connect(":memory:")
    conn.row_factory = dict_factory  # type: ignore[assignment]
    conn.execute("PRAGMA foreign_keys=ON")
    return conn
