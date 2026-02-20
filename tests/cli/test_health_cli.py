"""Tests for health CLI commands."""

from __future__ import annotations

import json
from pathlib import Path

from click.testing import CliRunner

from cli.main import cli
from goh.db.connection import get_connection
from goh.db.migrations.runner import run_migrations


def _extract_json(output: str) -> dict:
    """Extract a JSON object from CLI output that may contain structlog lines."""
    # Find the first { and match to its closing }
    start = output.index("{")
    depth = 0
    for i, ch in enumerate(output[start:], start):
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return json.loads(output[start : i + 1])
    raise ValueError("No complete JSON object found")


class TestHealthCLI:
    def test_health_check(self, cli_runner: CliRunner) -> None:
        result = cli_runner.invoke(cli, ["health", "check"])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["status"] == "ok"

    def test_health_deep(self, cli_runner: CliRunner, tmp_path: Path) -> None:
        db_path = str(tmp_path / "test.db")
        # Create and migrate DB
        db = get_connection(db_path)
        run_migrations(db)
        db.close()

        result = cli_runner.invoke(cli, ["--db", db_path, "health", "deep"])
        assert result.exit_code == 0
        data = _extract_json(result.output)
        assert data["status"] == "ok"
        assert data["database"]["connected"] is True
