"""Auth blueprint — register, login, magic-link, refresh, logout."""

from __future__ import annotations

from flask import Blueprint, current_app, g, jsonify, request

from api.middleware.auth import require_auth
from goh.services import auth_service

auth_bp = Blueprint("auth", __name__, url_prefix="/api/v1/auth")


def _settings():  # type: ignore[no-untyped-def]
    return current_app.config["SETTINGS"]


def _db():  # type: ignore[no-untyped-def]
    return current_app.get_db()  # type: ignore[attr-defined]


@auth_bp.route("/register", methods=["POST"])
def register():  # type: ignore[no-untyped-def]
    data = request.get_json(force=True)
    s = _settings()
    result = auth_service.register(
        _db(),
        username=data["username"],
        email=data["email"],
        password=data["password"],
        display_name=data.get("display_name"),
        jwt_secret=s.jwt_secret,
        access_expires_minutes=s.jwt_access_expires_minutes,
        refresh_expires_days=s.jwt_refresh_expires_days,
    )
    return jsonify(result), 201


@auth_bp.route("/login", methods=["POST"])
def login():  # type: ignore[no-untyped-def]
    data = request.get_json(force=True)
    s = _settings()
    result = auth_service.login_password(
        _db(),
        username=data["username"],
        password=data["password"],
        jwt_secret=s.jwt_secret,
        access_expires_minutes=s.jwt_access_expires_minutes,
        refresh_expires_days=s.jwt_refresh_expires_days,
        user_agent=request.headers.get("User-Agent"),
        ip_address=request.remote_addr,
    )
    return jsonify(result)


@auth_bp.route("/magic-link", methods=["POST"])
def magic_link():  # type: ignore[no-untyped-def]
    data = request.get_json(force=True)
    s = _settings()
    result = auth_service.create_magic_link(
        _db(), email=data["email"], expires_minutes=s.magic_link_expires_minutes,
    )
    return jsonify(result)


@auth_bp.route("/magic-link/verify", methods=["POST"])
def verify_magic_link():  # type: ignore[no-untyped-def]
    data = request.get_json(force=True)
    s = _settings()
    result = auth_service.login_magic_link(
        _db(), token=data["token"], jwt_secret=s.jwt_secret,
        access_expires_minutes=s.jwt_access_expires_minutes,
        refresh_expires_days=s.jwt_refresh_expires_days,
    )
    return jsonify(result)


@auth_bp.route("/refresh", methods=["POST"])
def refresh():  # type: ignore[no-untyped-def]
    data = request.get_json(force=True)
    s = _settings()
    result = auth_service.refresh_tokens(
        _db(), refresh_token=data["refresh_token"], jwt_secret=s.jwt_secret,
        access_expires_minutes=s.jwt_access_expires_minutes,
        refresh_expires_days=s.jwt_refresh_expires_days,
    )
    return jsonify(result)


@auth_bp.route("/logout", methods=["POST"])
def logout():  # type: ignore[no-untyped-def]
    data = request.get_json(force=True)
    auth_service.logout(_db(), refresh_token=data["refresh_token"])
    return jsonify({"message": "Logged out"})


@auth_bp.route("/me")
@require_auth
def me():  # type: ignore[no-untyped-def]
    result = auth_service.whoami(_db(), user_id=g.user_id)
    return jsonify(result)
