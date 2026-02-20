"""CLI commands for database management."""

from __future__ import annotations

import click
import structlog

from goh.db.connection import get_connection
from goh.db.migrations.runner import run_migrations

logger = structlog.get_logger(__name__)


@click.group("db")
def db_group() -> None:
    """Database management commands."""


@db_group.command("migrate")
@click.pass_context
def migrate(ctx: click.Context) -> None:
    """Run all pending database migrations."""
    db_path = ctx.obj["db_path"]
    db = get_connection(db_path)
    try:
        applied = run_migrations(db)
        if applied:
            click.echo(f"Applied {len(applied)} migration(s):")
            for name in applied:
                click.echo(f"  ✓ {name}")
        else:
            click.echo("No pending migrations.")
    finally:
        db.close()


@db_group.command("stats")
@click.pass_context
def stats(ctx: click.Context) -> None:
    """Show database statistics."""
    db_path = ctx.obj["db_path"]
    db = get_connection(db_path)
    try:
        # Table list and row counts
        tables = db.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE '\\_%%' ESCAPE '\\' ORDER BY name"
        ).fetchall()

        click.echo(f"Database: {db_path}")
        click.echo(f"Tables: {len(tables)}")
        click.echo()
        for table in tables:
            name = table["name"]
            count_row = db.execute(f"SELECT COUNT(*) as cnt FROM [{name}]").fetchone()
            count = count_row["cnt"] if count_row else 0
            click.echo(f"  {name}: {count} rows")

        # WAL info
        wal_row = db.execute("PRAGMA journal_mode").fetchone()
        click.echo(f"\nJournal mode: {wal_row['journal_mode'] if wal_row else 'unknown'}")
    finally:
        db.close()


@db_group.command("seed")
@click.pass_context
def seed(ctx: click.Context) -> None:
    """Seed the database with sample data."""
    db_path = ctx.obj["db_path"]
    db = get_connection(db_path)
    try:
        # Check if users exist already
        count_row = db.execute("SELECT COUNT(*) as cnt FROM users").fetchone()
        if count_row and count_row["cnt"] > 0:
            click.echo("Database already has data. Skipping seed.")
            return

        # Import bcrypt here for password hashing
        import bcrypt

        password_hash = bcrypt.hashpw(b"password123", bcrypt.gensalt()).decode()

        users = [
            ("dungeonmaster", "dm@goh.local", password_hash, "Dungeon Master", "dm", 1),
            ("aragorn", "aragorn@goh.local", password_hash, "Aragorn Elessar", "player", 1),
            ("gandalf", "gandalf@goh.local", password_hash, "Gandalf the Grey", "dm", 1),
            ("legolas", "legolas@goh.local", password_hash, "Legolas Greenleaf", "player", 1),
            ("gimli", "gimli@goh.local", password_hash, "Gimli son of Glóin", "player", 1),
        ]

        for username, email, pw_hash, display_name, role, verified in users:
            db.execute(
                """INSERT INTO users (username, email, password_hash, display_name, role, email_verified)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (username, email, pw_hash, display_name, role, verified),
            )

        db.commit()
        click.echo(f"Seeded {len(users)} users (password: password123)")
    finally:
        db.close()


@db_group.command("backup")
@click.argument("output_path", default="goh_backup.db")
@click.pass_context
def backup(ctx: click.Context, output_path: str) -> None:
    """Create a backup of the database."""
    import sqlite3

    db_path = ctx.obj["db_path"]
    source = get_connection(db_path)
    try:
        dest = sqlite3.connect(output_path)
        source.backup(dest)  # type: ignore[arg-type]
        dest.close()
        click.echo(f"Backup created: {output_path}")
    finally:
        source.close()
