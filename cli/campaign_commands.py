"""CLI commands for campaigns."""

from __future__ import annotations

import json

import click

from goh.db.connection import get_connection
from goh.services import campaign_service


@click.group("campaign")
def campaign_group() -> None:
    """Campaign commands."""


@campaign_group.command("create")
@click.option("--dm-id", required=True, type=int)
@click.option("--name", "-n", required=True)
@click.option("--description", "-d", default="")
@click.option("--max-players", default=6, type=int)
@click.pass_context
def create_campaign(
    ctx: click.Context, dm_id: int, name: str, description: str, max_players: int
) -> None:
    """Create a new campaign."""
    db = get_connection(ctx.obj["db_path"])
    try:
        result = campaign_service.create_campaign(
            db, dm_id=dm_id, name=name, description=description, max_players=max_players,
        )
        click.echo(json.dumps(result, indent=2))
    finally:
        db.close()


@campaign_group.command("get")
@click.argument("campaign_id", type=int)
@click.pass_context
def get_campaign(ctx: click.Context, campaign_id: int) -> None:
    """Get campaign details with members."""
    db = get_connection(ctx.obj["db_path"])
    try:
        result = campaign_service.get_campaign(db, campaign_id)
        click.echo(json.dumps(result, indent=2))
    finally:
        db.close()


@campaign_group.command("list")
@click.pass_context
def list_campaigns(ctx: click.Context) -> None:
    """List all campaigns."""
    db = get_connection(ctx.obj["db_path"])
    try:
        campaigns = campaign_service.list_campaigns(db)
        click.echo(json.dumps(campaigns, indent=2))
    finally:
        db.close()


@campaign_group.command("join")
@click.argument("campaign_id", type=int)
@click.option("--user-id", "-u", required=True, type=int)
@click.pass_context
def join_campaign(ctx: click.Context, campaign_id: int, user_id: int) -> None:
    """Join a campaign."""
    db = get_connection(ctx.obj["db_path"])
    try:
        result = campaign_service.join_campaign(db, campaign_id, user_id)
        click.echo(json.dumps(result, indent=2))
    finally:
        db.close()


@campaign_group.command("leave")
@click.argument("campaign_id", type=int)
@click.option("--user-id", "-u", required=True, type=int)
@click.pass_context
def leave_campaign(ctx: click.Context, campaign_id: int, user_id: int) -> None:
    """Leave a campaign."""
    db = get_connection(ctx.obj["db_path"])
    try:
        result = campaign_service.leave_campaign(db, campaign_id, user_id)
        click.echo(json.dumps(result, indent=2))
    finally:
        db.close()


@campaign_group.command("archive")
@click.argument("campaign_id", type=int)
@click.option("--user-id", "-u", required=True, type=int)
@click.pass_context
def archive_campaign(ctx: click.Context, campaign_id: int, user_id: int) -> None:
    """Archive a campaign (DM only)."""
    db = get_connection(ctx.obj["db_path"])
    try:
        result = campaign_service.archive_campaign(db, campaign_id, user_id)
        click.echo(json.dumps(result, indent=2))
    finally:
        db.close()
