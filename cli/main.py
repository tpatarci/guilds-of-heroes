"""GOH CLI — root command group."""

from __future__ import annotations

import click

from goh.observability.correlation import new_correlation_id
from goh.observability.logging import setup_logging


@click.group()
@click.option("--db", envvar="GOH_DB_PATH", default="./goh.db", help="Database path")
@click.pass_context
def cli(ctx: click.Context, db: str) -> None:
    """Guilds of Heroes — D&D Social Network CLI."""
    ctx.ensure_object(dict)
    ctx.obj["db_path"] = db

    # Setup observability
    setup_logging(is_production=False)
    cid = new_correlation_id()
    ctx.obj["correlation_id"] = cid


# Import and register sub-commands
from cli.auth_commands import auth_group  # noqa: E402
from cli.campaign_commands import campaign_group  # noqa: E402
from cli.character_commands import character_group  # noqa: E402
from cli.db_commands import db_group  # noqa: E402
from cli.dice_commands import dice_group  # noqa: E402
from cli.event_commands import event_group  # noqa: E402
from cli.follow_commands import follow_group  # noqa: E402
from cli.health_commands import health_group  # noqa: E402
from cli.notification_commands import notification_group  # noqa: E402
from cli.post_commands import post_group  # noqa: E402
from cli.session_log_commands import session_log_group  # noqa: E402
from cli.user_commands import user_group  # noqa: E402

cli.add_command(auth_group, "auth")
cli.add_command(campaign_group, "campaign")
cli.add_command(character_group, "character")
cli.add_command(db_group, "db")
cli.add_command(dice_group, "dice")
cli.add_command(event_group, "event")
cli.add_command(follow_group, "follow")
cli.add_command(health_group, "health")
cli.add_command(notification_group, "notification")
cli.add_command(post_group, "post")
cli.add_command(session_log_group, "session-log")
cli.add_command(user_group, "user")


if __name__ == "__main__":
    cli()
