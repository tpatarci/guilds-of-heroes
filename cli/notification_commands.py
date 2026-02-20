"""CLI commands for notifications."""

from __future__ import annotations

import json

import click

from goh.db.connection import get_connection
from goh.services import notification_service


@click.group("notification")
def notification_group() -> None:
    """Notification commands."""


@notification_group.command("list")
@click.argument("user_id", type=int)
@click.pass_context
def list_notifications(ctx: click.Context, user_id: int) -> None:
    """List notifications for a user."""
    db = get_connection(ctx.obj["db_path"])
    try:
        notifs = notification_service.list_notifications(db, user_id)
        click.echo(json.dumps(notifs, indent=2))
    finally:
        db.close()


@notification_group.command("count-unread")
@click.argument("user_id", type=int)
@click.pass_context
def count_unread(ctx: click.Context, user_id: int) -> None:
    """Count unread notifications."""
    db = get_connection(ctx.obj["db_path"])
    try:
        count = notification_service.count_unread(db, user_id)
        click.echo(json.dumps({"unread": count}))
    finally:
        db.close()


@notification_group.command("mark-read")
@click.argument("notification_id", type=int)
@click.option("--user-id", "-u", required=True, type=int)
@click.pass_context
def mark_read(ctx: click.Context, notification_id: int, user_id: int) -> None:
    """Mark a notification as read."""
    db = get_connection(ctx.obj["db_path"])
    try:
        notification_service.mark_read(db, notification_id, user_id)
        click.echo("Marked as read.")
    finally:
        db.close()
