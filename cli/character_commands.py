"""CLI commands for characters."""

from __future__ import annotations

import json

import click

from goh.db.connection import get_connection
from goh.services import character_service


@click.group("character")
def character_group() -> None:
    """Character commands."""


@character_group.command("create")
@click.option("--owner-id", "-o", required=True, type=int)
@click.option("--name", "-n", required=True)
@click.option("--race", "-r", default="Human")
@click.option("--class", "char_class", default="Fighter")
@click.option("--level", "-l", default=1, type=int)
@click.pass_context
def create_character(
    ctx: click.Context, owner_id: int, name: str, race: str, char_class: str, level: int
) -> None:
    """Create a new character."""
    db = get_connection(ctx.obj["db_path"])
    try:
        result = character_service.create_character(
            db, owner_id=owner_id, name=name, race=race, char_class=char_class, level=level,
        )
        click.echo(json.dumps(result, indent=2))
    finally:
        db.close()


@character_group.command("get")
@click.argument("char_id", type=int)
@click.pass_context
def get_character(ctx: click.Context, char_id: int) -> None:
    """Get character details."""
    db = get_connection(ctx.obj["db_path"])
    try:
        result = character_service.get_character(db, char_id)
        click.echo(json.dumps(result, indent=2))
    finally:
        db.close()


@character_group.command("list")
@click.argument("owner_id", type=int)
@click.pass_context
def list_characters(ctx: click.Context, owner_id: int) -> None:
    """List characters owned by a user."""
    db = get_connection(ctx.obj["db_path"])
    try:
        chars = character_service.list_characters(db, owner_id)
        click.echo(json.dumps(chars, indent=2))
    finally:
        db.close()


@character_group.command("delete")
@click.argument("char_id", type=int)
@click.option("--user-id", "-u", required=True, type=int)
@click.pass_context
def delete_character(ctx: click.Context, char_id: int, user_id: int) -> None:
    """Delete a character."""
    db = get_connection(ctx.obj["db_path"])
    try:
        character_service.delete_character(db, char_id, user_id)
        click.echo("Character deleted.")
    finally:
        db.close()
