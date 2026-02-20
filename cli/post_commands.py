"""CLI commands for posts."""

from __future__ import annotations

import json

import click

from goh.db.connection import get_connection
from goh.services import post_service


@click.group("post")
def post_group() -> None:
    """Post commands."""


@post_group.command("create")
@click.option("--author-id", "-a", required=True, type=int)
@click.option("--content", "-c", required=True)
@click.option("--type", "post_type", default="text")
@click.pass_context
def create_post(ctx: click.Context, author_id: int, content: str, post_type: str) -> None:
    """Create a new post."""
    db = get_connection(ctx.obj["db_path"])
    try:
        result = post_service.create_post(db, author_id=author_id, content=content, post_type=post_type)
        click.echo(json.dumps(result, indent=2))
    finally:
        db.close()


@post_group.command("list")
@click.argument("author_id", type=int)
@click.pass_context
def list_posts(ctx: click.Context, author_id: int) -> None:
    """List posts by a user."""
    db = get_connection(ctx.obj["db_path"])
    try:
        posts = post_service.list_posts(db, author_id)
        click.echo(json.dumps(posts, indent=2))
    finally:
        db.close()


@post_group.command("feed")
@click.argument("user_id", type=int)
@click.pass_context
def feed(ctx: click.Context, user_id: int) -> None:
    """Get user's feed (posts from followed users)."""
    db = get_connection(ctx.obj["db_path"])
    try:
        posts = post_service.get_feed(db, user_id)
        click.echo(json.dumps(posts, indent=2))
    finally:
        db.close()


@post_group.command("timeline")
@click.pass_context
def timeline(ctx: click.Context) -> None:
    """Get global timeline."""
    db = get_connection(ctx.obj["db_path"])
    try:
        posts = post_service.get_timeline(db)
        click.echo(json.dumps(posts, indent=2))
    finally:
        db.close()


@post_group.command("delete")
@click.argument("post_id", type=int)
@click.option("--user-id", "-u", required=True, type=int)
@click.pass_context
def delete_post(ctx: click.Context, post_id: int, user_id: int) -> None:
    """Delete a post."""
    db = get_connection(ctx.obj["db_path"])
    try:
        post_service.delete_post(db, post_id, user_id)
        click.echo("Post deleted.")
    finally:
        db.close()
