"""CLI commands for events."""

from __future__ import annotations

import json

import click

from goh.db.connection import get_connection
from goh.services import event_service


@click.group("event")
def event_group() -> None:
    """Event commands."""


@event_group.command("create")
@click.option("--organizer-id", "-o", required=True, type=int)
@click.option("--title", "-t", required=True)
@click.option("--type", "event_type", default="one_shot")
@click.option("--description", "-d", default="")
@click.option("--location", "-l", default=None)
@click.option("--start", "start_time", required=True)
@click.option("--max-players", type=int, default=None)
@click.pass_context
def create_event(
    ctx: click.Context, organizer_id: int, title: str, event_type: str,
    description: str, location: str | None, start_time: str, max_players: int | None,
) -> None:
    """Create a new event."""
    db = get_connection(ctx.obj["db_path"])
    try:
        result = event_service.create_event(
            db, organizer_id=organizer_id, title=title, event_type=event_type,
            description=description, location=location, start_time=start_time,
            max_players=max_players,
        )
        click.echo(json.dumps(result, indent=2))
    finally:
        db.close()


@event_group.command("list")
@click.pass_context
def list_events(ctx: click.Context) -> None:
    """List all events."""
    db = get_connection(ctx.obj["db_path"])
    try:
        events = event_service.list_events(db)
        click.echo(json.dumps(events, indent=2))
    finally:
        db.close()


@event_group.command("get")
@click.argument("event_id", type=int)
@click.pass_context
def get_event(ctx: click.Context, event_id: int) -> None:
    """Get event details with RSVPs."""
    db = get_connection(ctx.obj["db_path"])
    try:
        event = event_service.get_event(db, event_id)
        click.echo(json.dumps(event, indent=2))
    finally:
        db.close()


@event_group.command("rsvp")
@click.argument("event_id", type=int)
@click.option("--user-id", "-u", required=True, type=int)
@click.option("--status", "-s", default="going", type=click.Choice(["going", "maybe", "not_going"]))
@click.pass_context
def rsvp(ctx: click.Context, event_id: int, user_id: int, status: str) -> None:
    """RSVP to an event."""
    db = get_connection(ctx.obj["db_path"])
    try:
        result = event_service.rsvp_event(db, event_id, user_id, status)
        click.echo(json.dumps(result, indent=2))
    finally:
        db.close()


@event_group.command("cancel")
@click.argument("event_id", type=int)
@click.option("--user-id", "-u", required=True, type=int)
@click.pass_context
def cancel(ctx: click.Context, event_id: int, user_id: int) -> None:
    """Cancel an event (organizer only)."""
    db = get_connection(ctx.obj["db_path"])
    try:
        result = event_service.cancel_event(db, event_id, user_id)
        click.echo(json.dumps(result, indent=2))
    finally:
        db.close()
