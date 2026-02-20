"""CLI commands for health checks."""

from __future__ import annotations

import json

import click

from goh.db.connection import get_connection
from goh.services.health_service import check_basic, check_deep


@click.group("health")
def health_group() -> None:
    """Health check commands."""


@health_group.command("check")
def check() -> None:
    """Basic liveness check (no DB)."""
    result = check_basic()
    click.echo(json.dumps(result, indent=2))


@health_group.command("deep")
@click.pass_context
def deep(ctx: click.Context) -> None:
    """Deep health check (DB + metrics)."""
    db_path = ctx.obj["db_path"]
    db = get_connection(db_path)
    try:
        result = check_deep(db)
        click.echo(json.dumps(result, indent=2))

        if result["status"] != "ok":
            raise SystemExit(1)
    finally:
        db.close()
