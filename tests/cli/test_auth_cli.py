"""Tests for auth CLI commands."""

from __future__ import annotations

import json
from pathlib import Path

from click.testing import CliRunner

from cli.main import cli
from goh.db.connection import get_connection
from goh.db.migrations.runner import run_migrations


def _setup_db(tmp_path: Path) -> str:
    db_path = str(tmp_path / "test.db")
    db = get_connection(db_path)
    run_migrations(db)
    db.close()
    return db_path


def _extract_json(output: str) -> dict:
    """Extract JSON from CLI output that may contain structlog lines."""
    start = output.index("{")
    depth = 0
    for i, ch in enumerate(output[start:], start):
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return json.loads(output[start : i + 1])
    raise ValueError("No JSON found")


class TestAuthCLI:
    def test_register(self, cli_runner: CliRunner, tmp_path: Path) -> None:
        db_path = _setup_db(tmp_path)
        result = cli_runner.invoke(
            cli,
            ["--db", db_path, "auth", "register",
             "-u", "testuser", "-e", "test@test.com", "-p", "password123"],
        )
        assert result.exit_code == 0
        data = _extract_json(result.output)
        assert data["user"]["username"] == "testuser"

    def test_login(self, cli_runner: CliRunner, tmp_path: Path) -> None:
        db_path = _setup_db(tmp_path)
        # Register first
        cli_runner.invoke(
            cli,
            ["--db", db_path, "auth", "register",
             "-u", "testuser", "-e", "test@test.com", "-p", "password123"],
        )
        # Login
        result = cli_runner.invoke(
            cli,
            ["--db", db_path, "auth", "login", "-u", "testuser", "-p", "password123"],
        )
        assert result.exit_code == 0
        data = _extract_json(result.output)
        assert data["user"]["username"] == "testuser"
        assert "access_token" in data

    def test_whoami(self, cli_runner: CliRunner, tmp_path: Path) -> None:
        db_path = _setup_db(tmp_path)
        # Register
        result = cli_runner.invoke(
            cli,
            ["--db", db_path, "auth", "register",
             "-u", "testuser", "-e", "test@test.com", "-p", "password123"],
        )
        data = _extract_json(result.output)
        token = data["access_token"]

        # Whoami
        result = cli_runner.invoke(
            cli, ["--db", db_path, "auth", "whoami", "-t", token],
        )
        assert result.exit_code == 0
        data = _extract_json(result.output)
        assert data["username"] == "testuser"
