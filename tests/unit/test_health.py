"""Tests for health service."""

from __future__ import annotations

import sqlite3

from goh.services.health_service import check_basic, check_deep


class TestCheckBasic:
    def test_returns_ok_status(self) -> None:
        result = check_basic()
        assert result["status"] == "ok"
        assert "timestamp" in result


class TestCheckDeep:
    def test_returns_ok_with_db(self, db: sqlite3.Connection) -> None:
        result = check_deep(db)
        assert result["status"] == "ok"
        assert result["database"]["connected"] is True
        assert result["database"]["foreign_keys"] is True
        assert result["database"]["tables"] > 0
        assert "users" in result["database"]["table_names"]

    def test_includes_metrics(self, db: sqlite3.Connection) -> None:
        from goh.observability.metrics import metrics

        metrics.increment("test.counter", 5)
        result = check_deep(db)
        assert result["metrics"]["test.counter"] == 5
