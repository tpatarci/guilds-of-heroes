"""CLI commands for dice rolling."""

from __future__ import annotations

import json

import click

from goh.db.connection import get_connection
from goh.services import dice_service


@click.group("dice")
def dice_group() -> None:
    """Dice roller commands."""


@dice_group.command("roll")
@click.argument("expression")
@click.option("--user-id", "-u", required=True, type=int)
@click.option("--campaign-id", "-c", default=None, type=int)
@click.option("--no-save", is_flag=True, help="Don't save the roll")
@click.pass_context
def roll(ctx: click.Context, expression: str, user_id: int, campaign_id: int | None, no_save: bool) -> None:
    """Roll dice (e.g. 1d20, 2d6+3, 4d8-2)."""
    db = get_connection(ctx.obj["db_path"])
    try:
        result = dice_service.roll(
            db, user_id=user_id, expression=expression,
            campaign_id=campaign_id, save=not no_save,
        )
        click.echo(json.dumps(result, indent=2))
    finally:
        db.close()


@dice_group.command("history")
@click.argument("user_id", type=int)
@click.option("--limit", default=20, type=int)
@click.option("--campaign-id", "-c", default=None, type=int)
@click.pass_context
def history(ctx: click.Context, user_id: int, limit: int, campaign_id: int | None) -> None:
    """Show dice roll history."""
    db = get_connection(ctx.obj["db_path"])
    try:
        rolls = dice_service.get_history(db, user_id, limit, campaign_id)
        click.echo(json.dumps(rolls, indent=2))
    finally:
        db.close()
