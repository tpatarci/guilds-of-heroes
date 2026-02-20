"""CLI commands for authentication."""

from __future__ import annotations

import json

import click
import structlog

from goh.db.connection import get_connection
from goh.db.migrations.runner import run_migrations
from goh.services import auth_service

logger = structlog.get_logger(__name__)

JWT_SECRET = "cli-dev-secret"


def _get_db(ctx: click.Context) -> tuple:
    """Get DB connection and ensure migrations are run."""
    db_path = ctx.obj["db_path"]
    db = get_connection(db_path)
    run_migrations(db)
    return db, db_path


@click.group("auth")
def auth_group() -> None:
    """Authentication commands."""


@auth_group.command("register")
@click.option("--username", "-u", required=True, help="Username")
@click.option("--email", "-e", required=True, help="Email address")
@click.option("--password", "-p", required=True, help="Password")
@click.option("--display-name", "-d", default=None, help="Display name")
@click.pass_context
def register(
    ctx: click.Context,
    username: str,
    email: str,
    password: str,
    display_name: str | None,
) -> None:
    """Register a new user."""
    db = get_connection(ctx.obj["db_path"])
    try:
        result = auth_service.register(
            db,
            username=username,
            email=email,
            password=password,
            display_name=display_name,
            jwt_secret=JWT_SECRET,
        )
        click.echo(json.dumps(result, indent=2))
    finally:
        db.close()


@auth_group.command("login")
@click.option("--username", "-u", required=True, help="Username")
@click.option("--password", "-p", required=True, help="Password")
@click.pass_context
def login(ctx: click.Context, username: str, password: str) -> None:
    """Login with username + password."""
    db = get_connection(ctx.obj["db_path"])
    try:
        result = auth_service.login_password(
            db,
            username=username,
            password=password,
            jwt_secret=JWT_SECRET,
        )
        click.echo(json.dumps(result, indent=2))
    finally:
        db.close()


@auth_group.command("magic-link")
@click.option("--email", "-e", required=True, help="Email address")
@click.pass_context
def magic_link(ctx: click.Context, email: str) -> None:
    """Create a magic link for passwordless login."""
    db = get_connection(ctx.obj["db_path"])
    try:
        result = auth_service.create_magic_link(db, email=email)
        click.echo(json.dumps(result, indent=2))
    finally:
        db.close()


@auth_group.command("verify-magic-link")
@click.option("--token", "-t", required=True, help="Magic link token")
@click.pass_context
def verify_magic_link(ctx: click.Context, token: str) -> None:
    """Verify a magic link token and login."""
    db = get_connection(ctx.obj["db_path"])
    try:
        result = auth_service.login_magic_link(
            db,
            token=token,
            jwt_secret=JWT_SECRET,
        )
        click.echo(json.dumps(result, indent=2))
    finally:
        db.close()


@auth_group.command("whoami")
@click.option("--token", "-t", required=True, help="Access token")
@click.pass_context
def whoami(ctx: click.Context, token: str) -> None:
    """Show current user from access token."""
    db = get_connection(ctx.obj["db_path"])
    try:
        payload = auth_service.verify_access_token(token, jwt_secret=JWT_SECRET)
        result = auth_service.whoami(db, user_id=payload["sub"])
        click.echo(json.dumps(result, indent=2))
    finally:
        db.close()


@auth_group.command("refresh")
@click.option("--token", "-t", required=True, help="Refresh token")
@click.pass_context
def refresh(ctx: click.Context, token: str) -> None:
    """Refresh access token."""
    db = get_connection(ctx.obj["db_path"])
    try:
        result = auth_service.refresh_tokens(
            db,
            refresh_token=token,
            jwt_secret=JWT_SECRET,
        )
        click.echo(json.dumps(result, indent=2))
    finally:
        db.close()
