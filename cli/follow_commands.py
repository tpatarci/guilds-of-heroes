"""CLI commands for follows."""

from __future__ import annotations

import json

import click

from goh.db.connection import get_connection
from goh.services import follow_service


@click.group("follow")
def follow_group() -> None:
    """Follow commands."""


@follow_group.command("add")
@click.argument("follower_id", type=int)
@click.argument("following_id", type=int)
@click.pass_context
def follow_user(ctx: click.Context, follower_id: int, following_id: int) -> None:
    """Follow a user."""
    db = get_connection(ctx.obj["db_path"])
    try:
        result = follow_service.follow_user(db, follower_id, following_id)
        click.echo(json.dumps(result, indent=2))
    finally:
        db.close()


@follow_group.command("remove")
@click.argument("follower_id", type=int)
@click.argument("following_id", type=int)
@click.pass_context
def unfollow_user(ctx: click.Context, follower_id: int, following_id: int) -> None:
    """Unfollow a user."""
    db = get_connection(ctx.obj["db_path"])
    try:
        result = follow_service.unfollow_user(db, follower_id, following_id)
        click.echo(json.dumps(result, indent=2))
    finally:
        db.close()


@follow_group.command("followers")
@click.argument("user_id", type=int)
@click.pass_context
def followers(ctx: click.Context, user_id: int) -> None:
    """List followers of a user."""
    db = get_connection(ctx.obj["db_path"])
    try:
        users = follow_service.get_followers(db, user_id)
        click.echo(json.dumps(users, indent=2))
    finally:
        db.close()


@follow_group.command("following")
@click.argument("user_id", type=int)
@click.pass_context
def following(ctx: click.Context, user_id: int) -> None:
    """List users followed by a user."""
    db = get_connection(ctx.obj["db_path"])
    try:
        users = follow_service.get_following(db, user_id)
        click.echo(json.dumps(users, indent=2))
    finally:
        db.close()
