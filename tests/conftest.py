"""Test fixtures — in-memory SQLite, CLI runner, connection factory."""

from __future__ import annotations

import sqlite3

import pytest
from click.testing import CliRunner

from goh.db.connection import get_memory_connection
from goh.db.migrations.runner import run_migrations
from goh.observability.logging import setup_logging
from goh.observability.metrics import metrics


@pytest.fixture(autouse=True)
def _setup_logging() -> None:
    """Configure structlog for tests."""
    setup_logging(is_production=False)


@pytest.fixture(autouse=True)
def _reset_metrics() -> None:
    """Reset metrics between tests."""
    metrics.reset()


@pytest.fixture()
def db() -> sqlite3.Connection:
    """In-memory SQLite connection with all migrations applied."""
    conn = get_memory_connection()
    run_migrations(conn)
    return conn


@pytest.fixture()
def cli_runner() -> CliRunner:
    """Click CLI test runner."""
    return CliRunner()
