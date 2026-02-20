"""CLI commands for user management."""

from __future__ import annotations

import json

import click

from goh.db.connection import get_connection
from goh.services import user_service


@click.group("user")
def user_group() -> None:
    """User management commands."""


@user_group.command("list")
@click.option("--limit", default=50, help="Max results")
@click.pass_context
def list_users(ctx: click.Context, limit: int) -> None:
    """List all users."""
    db = get_connection(ctx.obj["db_path"])
    try:
        users = user_service.list_users(db, limit=limit)
        click.echo(json.dumps(users, indent=2))
    finally:
        db.close()


@user_group.command("get")
@click.argument("user_id", type=int)
@click.pass_context
def get_user(ctx: click.Context, user_id: int) -> None:
    """Get user profile."""
    db = get_connection(ctx.obj["db_path"])
    try:
        profile = user_service.get_profile(db, user_id)
        click.echo(json.dumps(profile, indent=2))
    finally:
        db.close()


@user_group.command("update-profile")
@click.argument("user_id", type=int)
@click.option("--display-name", default=None)
@click.option("--bio", default=None)
@click.pass_context
def update_profile(
    ctx: click.Context, user_id: int, display_name: str | None, bio: str | None
) -> None:
    """Update user profile."""
    db = get_connection(ctx.obj["db_path"])
    try:
        result = user_service.update_profile(db, user_id, display_name=display_name, bio=bio)
        click.echo(json.dumps(result, indent=2))
    finally:
        db.close()


@user_group.command("search")
@click.argument("query")
@click.pass_context
def search_users(ctx: click.Context, query: str) -> None:
    """Search users by username or display name."""
    db = get_connection(ctx.obj["db_path"])
    try:
        users = user_service.search_users(db, query)
        click.echo(json.dumps(users, indent=2))
    finally:
        db.close()


@user_group.command("set-role")
@click.argument("admin_user_id", type=int)
@click.argument("target_user_id", type=int)
@click.argument("role")
@click.pass_context
def set_role(ctx: click.Context, admin_user_id: int, target_user_id: int, role: str) -> None:
    """Set user role (admin only)."""
    db = get_connection(ctx.obj["db_path"])
    try:
        result = user_service.set_role(db, admin_user_id, target_user_id, role)
        click.echo(json.dumps(result, indent=2))
    finally:
        db.close()
