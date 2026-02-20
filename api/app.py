"""Flask application factory — paper-thin HTTP adapter."""

from __future__ import annotations

import sqlite3

from flask import Flask, g

from config.settings import Settings, get_settings
from goh.db.connection import get_connection
from goh.db.migrations.runner import run_migrations
from goh.observability.logging import setup_logging


def create_app(settings: Settings | None = None) -> Flask:
    """Create and configure the Flask application."""
    if settings is None:
        settings = get_settings()

    setup_logging(is_production=settings.is_production)

    app = Flask(__name__)
    app.config["SETTINGS"] = settings

    # Database lifecycle
    def get_db() -> sqlite3.Connection:
        if "db" not in g:
            g.db = get_connection(settings.db_path_resolved)
        return g.db

    @app.teardown_appcontext
    def close_db(exception: BaseException | None = None) -> None:
        db = g.pop("db", None)
        if db is not None:
            db.close()

    app.get_db = get_db  # type: ignore[attr-defined]

    # Ensure migrations on startup
    with app.app_context():
        db = get_db()
        run_migrations(db)

    # Register middleware
    from api.middleware.correlation_id import setup_correlation_id
    from api.middleware.error_handler import setup_error_handler
    from api.middleware.request_timing import setup_request_timing

    setup_correlation_id(app)
    setup_request_timing(app)
    setup_error_handler(app)

    # Register blueprints
    from api.blueprints.auth_bp import auth_bp
    from api.blueprints.campaigns_bp import campaigns_bp
    from api.blueprints.characters_bp import characters_bp
    from api.blueprints.dice_bp import dice_bp
    from api.blueprints.events_bp import events_bp
    from api.blueprints.follows_bp import follows_bp
    from api.blueprints.health_bp import health_bp
    from api.blueprints.notifications_bp import notifications_bp
    from api.blueprints.posts_bp import posts_bp
    from api.blueprints.session_logs_bp import session_logs_bp
    from api.blueprints.users_bp import users_bp

    app.register_blueprint(health_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(posts_bp)
    app.register_blueprint(follows_bp)
    app.register_blueprint(notifications_bp)
    app.register_blueprint(events_bp)
    app.register_blueprint(characters_bp)
    app.register_blueprint(campaigns_bp)
    app.register_blueprint(session_logs_bp)
    app.register_blueprint(dice_bp)

    return app
