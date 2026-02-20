"""CLI commands for session logs."""

from __future__ import annotations

import json

import click

from goh.db.connection import get_connection
from goh.services import session_log_service


@click.group("session-log")
def session_log_group() -> None:
    """Session log commands."""


@session_log_group.command("create")
@click.option("--campaign-id", "-c", required=True, type=int)
@click.option("--author-id", "-a", required=True, type=int)
@click.option("--session-number", "-n", required=True, type=int)
@click.option("--title", "-t", required=True)
@click.option("--summary", "-s", default="")
@click.option("--date", "session_date", default="")
@click.pass_context
def create_log(
    ctx: click.Context, campaign_id: int, author_id: int,
    session_number: int, title: str, summary: str, session_date: str,
) -> None:
    """Create a session log entry."""
    db = get_connection(ctx.obj["db_path"])
    try:
        result = session_log_service.create_session_log(
            db, campaign_id=campaign_id, author_id=author_id,
            session_number=session_number, title=title,
            summary=summary, session_date=session_date,
        )
        click.echo(json.dumps(result, indent=2))
    finally:
        db.close()


@session_log_group.command("list")
@click.argument("campaign_id", type=int)
@click.pass_context
def list_logs(ctx: click.Context, campaign_id: int) -> None:
    """List session logs for a campaign."""
    db = get_connection(ctx.obj["db_path"])
    try:
        logs = session_log_service.list_session_logs(db, campaign_id)
        click.echo(json.dumps(logs, indent=2))
    finally:
        db.close()


@session_log_group.command("get")
@click.argument("log_id", type=int)
@click.pass_context
def get_log(ctx: click.Context, log_id: int) -> None:
    """Get a session log entry."""
    db = get_connection(ctx.obj["db_path"])
    try:
        result = session_log_service.get_session_log(db, log_id)
        click.echo(json.dumps(result, indent=2))
    finally:
        db.close()
