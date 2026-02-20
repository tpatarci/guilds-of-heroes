"""Tests for database CLI commands."""

from __future__ import annotations

from pathlib import Path

from click.testing import CliRunner

from cli.main import cli


class TestDBMigrate:
    def test_migrate_fresh_db(self, cli_runner: CliRunner, tmp_path: Path) -> None:
        db_path = str(tmp_path / "test.db")
        result = cli_runner.invoke(cli, ["--db", db_path, "db", "migrate"])
        assert result.exit_code == 0
        assert "Applied" in result.output or "001_initial_schema.sql" in result.output

    def test_migrate_already_applied(self, cli_runner: CliRunner, tmp_path: Path) -> None:
        db_path = str(tmp_path / "test.db")
        # Run twice
        cli_runner.invoke(cli, ["--db", db_path, "db", "migrate"])
        result = cli_runner.invoke(cli, ["--db", db_path, "db", "migrate"])
        assert result.exit_code == 0
        assert "No pending migrations" in result.output


class TestDBStats:
    def test_stats(self, cli_runner: CliRunner, tmp_path: Path) -> None:
        db_path = str(tmp_path / "test.db")
        # Must migrate first
        cli_runner.invoke(cli, ["--db", db_path, "db", "migrate"])

        result = cli_runner.invoke(cli, ["--db", db_path, "db", "stats"])
        assert result.exit_code == 0
        assert "users" in result.output
        assert "Tables:" in result.output
