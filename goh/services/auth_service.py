"""Auth service — register, login (password/magic-link/oauth), tokens, session management."""

from __future__ import annotations

import secrets
import sqlite3
from datetime import datetime, timedelta, timezone

import bcrypt
import jwt
import structlog

from goh.domain.entities.user import User
from goh.domain.exceptions import (
    DuplicateError,
    InvalidCredentialsError,
    InvalidTokenError,
    NotFoundError,
    TokenExpiredError,
    ValidationError,
)
from goh.observability.metrics import metrics
from goh.observability.timing import timed
from goh.repositories import audit_repo, magic_link_repo, session_repo, user_repo

logger = structlog.get_logger(__name__)

# Defaults — overridable via config
DEFAULT_ACCESS_EXPIRES_MINUTES = 30
DEFAULT_REFRESH_EXPIRES_DAYS = 30
DEFAULT_MAGIC_LINK_EXPIRES_MINUTES = 15


def _hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def _verify_password(password: str, password_hash: str) -> bool:
    return bcrypt.checkpw(password.encode(), password_hash.encode())


def _create_access_token(
    user: User,
    secret: str,
    expires_minutes: int = DEFAULT_ACCESS_EXPIRES_MINUTES,
) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "sub": str(user.id),
        "username": user.username,
        "role": user.role,
        "iat": now,
        "exp": now + timedelta(minutes=expires_minutes),
        "type": "access",
    }
    return jwt.encode(payload, secret, algorithm="HS256")


def _create_refresh_token() -> str:
    return secrets.token_urlsafe(64)


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@timed
def register(
    db: sqlite3.Connection,
    *,
    username: str,
    email: str,
    password: str,
    display_name: str | None = None,
    jwt_secret: str = "change-me",
    access_expires_minutes: int = DEFAULT_ACCESS_EXPIRES_MINUTES,
    refresh_expires_days: int = DEFAULT_REFRESH_EXPIRES_DAYS,
) -> dict:
    """Register a new user with username + password."""
    # Validate
    if len(username) < 3:
        raise ValidationError("Username must be at least 3 characters")
    if len(password) < 8:
        raise ValidationError("Password must be at least 8 characters")
    if "@" not in email:
        raise ValidationError("Invalid email address")

    # Check uniqueness
    if user_repo.find_by_username(db, username):
        raise DuplicateError("User", "username", username)
    if user_repo.find_by_email(db, email):
        raise DuplicateError("User", "email", email)

    # Create user
    password_hash = _hash_password(password)
    user = user_repo.create(
        db,
        username=username,
        email=email,
        password_hash=password_hash,
        display_name=display_name or username,
    )

    # Create tokens
    access_token = _create_access_token(user, jwt_secret, access_expires_minutes)
    refresh_token = _create_refresh_token()
    refresh_expires = (
        datetime.now(timezone.utc) + timedelta(days=refresh_expires_days)
    ).isoformat()

    session_repo.create(
        db,
        user_id=user.id,
        refresh_token=refresh_token,
        expires_at=refresh_expires,
    )

    audit_repo.log_action(
        db, user_id=user.id, action="register", resource_type="user", resource_id=user.id
    )
    metrics.increment("auth.register.success")
    logger.info("auth.register", user_id=user.id, username=username)

    return {
        "user": user.to_private_dict(),
        "access_token": access_token,
        "refresh_token": refresh_token,
    }


@timed
def login_password(
    db: sqlite3.Connection,
    *,
    username: str,
    password: str,
    jwt_secret: str = "change-me",
    access_expires_minutes: int = DEFAULT_ACCESS_EXPIRES_MINUTES,
    refresh_expires_days: int = DEFAULT_REFRESH_EXPIRES_DAYS,
    user_agent: str | None = None,
    ip_address: str | None = None,
) -> dict:
    """Login with username + password."""
    user = user_repo.find_by_username(db, username)
    if not user:
        metrics.increment("auth.login.failure")
        raise InvalidCredentialsError()

    pw_hash = user_repo.get_password_hash(db, user.id)
    if not pw_hash or not _verify_password(password, pw_hash):
        metrics.increment("auth.login.failure")
        raise InvalidCredentialsError()

    access_token = _create_access_token(user, jwt_secret, access_expires_minutes)
    refresh_token = _create_refresh_token()
    refresh_expires = (
        datetime.now(timezone.utc) + timedelta(days=refresh_expires_days)
    ).isoformat()

    session_repo.create(
        db,
        user_id=user.id,
        refresh_token=refresh_token,
        expires_at=refresh_expires,
        user_agent=user_agent,
        ip_address=ip_address,
    )

    audit_repo.log_action(
        db, user_id=user.id, action="login_password", resource_type="session"
    )
    metrics.increment("auth.login.success")
    logger.info("auth.login_password", user_id=user.id)

    return {
        "user": user.to_private_dict(),
        "access_token": access_token,
        "refresh_token": refresh_token,
    }


@timed
def create_magic_link(
    db: sqlite3.Connection,
    *,
    email: str,
    expires_minutes: int = DEFAULT_MAGIC_LINK_EXPIRES_MINUTES,
) -> dict:
    """Create a magic link for passwordless login."""
    user = user_repo.find_by_email(db, email)
    if not user:
        raise NotFoundError("User", email)

    token = secrets.token_urlsafe(48)
    expires_at = (datetime.now(timezone.utc) + timedelta(minutes=expires_minutes)).isoformat()

    magic_link_repo.create(db, user_id=user.id, token=token, expires_at=expires_at)

    audit_repo.log_action(
        db, user_id=user.id, action="create_magic_link", resource_type="magic_link"
    )
    logger.info("auth.magic_link_created", user_id=user.id)

    return {"token": token, "expires_at": expires_at}


@timed
def login_magic_link(
    db: sqlite3.Connection,
    *,
    token: str,
    jwt_secret: str = "change-me",
    access_expires_minutes: int = DEFAULT_ACCESS_EXPIRES_MINUTES,
    refresh_expires_days: int = DEFAULT_REFRESH_EXPIRES_DAYS,
) -> dict:
    """Login via magic link token."""
    link = magic_link_repo.find_by_token(db, token)
    if not link:
        metrics.increment("auth.magic_link.failure")
        raise InvalidTokenError()

    # Check expiry
    expires_at = datetime.fromisoformat(link["expires_at"])
    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=timezone.utc)
    if datetime.now(timezone.utc) > expires_at:
        metrics.increment("auth.magic_link.failure")
        raise TokenExpiredError()

    magic_link_repo.mark_used(db, token)

    user = user_repo.find_by_id(db, link["user_id"])
    if not user:
        raise NotFoundError("User", link["user_id"])

    # Verify email on first magic link login
    if not user.email_verified:
        user_repo.verify_email(db, user.id)
        user = user_repo.find_by_id(db, user.id)
        assert user is not None

    access_token = _create_access_token(user, jwt_secret, access_expires_minutes)
    refresh_token = _create_refresh_token()
    refresh_expires = (
        datetime.now(timezone.utc) + timedelta(days=refresh_expires_days)
    ).isoformat()

    session_repo.create(
        db,
        user_id=user.id,
        refresh_token=refresh_token,
        expires_at=refresh_expires,
    )

    audit_repo.log_action(
        db, user_id=user.id, action="login_magic_link", resource_type="session"
    )
    metrics.increment("auth.magic_link.success")
    logger.info("auth.login_magic_link", user_id=user.id)

    return {
        "user": user.to_private_dict(),
        "access_token": access_token,
        "refresh_token": refresh_token,
    }


@timed
def refresh_tokens(
    db: sqlite3.Connection,
    *,
    refresh_token: str,
    jwt_secret: str = "change-me",
    access_expires_minutes: int = DEFAULT_ACCESS_EXPIRES_MINUTES,
    refresh_expires_days: int = DEFAULT_REFRESH_EXPIRES_DAYS,
) -> dict:
    """Exchange a refresh token for new access + refresh tokens."""
    session = session_repo.find_by_refresh_token(db, refresh_token)
    if not session:
        raise InvalidTokenError()

    expires_at = datetime.fromisoformat(session["expires_at"])
    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=timezone.utc)
    if datetime.now(timezone.utc) > expires_at:
        raise TokenExpiredError()

    # Revoke old, issue new
    session_repo.revoke(db, refresh_token)

    user = user_repo.find_by_id(db, session["user_id"])
    if not user:
        raise NotFoundError("User", session["user_id"])

    new_access = _create_access_token(user, jwt_secret, access_expires_minutes)
    new_refresh = _create_refresh_token()
    new_refresh_expires = (
        datetime.now(timezone.utc) + timedelta(days=refresh_expires_days)
    ).isoformat()

    session_repo.create(
        db,
        user_id=user.id,
        refresh_token=new_refresh,
        expires_at=new_refresh_expires,
    )

    metrics.increment("auth.refresh.success")
    return {
        "access_token": new_access,
        "refresh_token": new_refresh,
    }


def verify_access_token(token: str, *, jwt_secret: str = "change-me") -> dict:
    """Verify and decode an access token. Returns the payload."""
    try:
        payload = jwt.decode(token, jwt_secret, algorithms=["HS256"])
        if payload.get("type") != "access":
            raise InvalidTokenError()
        payload["sub"] = int(payload["sub"])
        return payload
    except jwt.ExpiredSignatureError as e:
        raise TokenExpiredError() from e
    except jwt.InvalidTokenError as e:
        raise InvalidTokenError() from e


@timed
def logout(db: sqlite3.Connection, *, refresh_token: str) -> None:
    """Revoke a refresh token (logout)."""
    session_repo.revoke(db, refresh_token)
    logger.info("auth.logout")


def whoami(db: sqlite3.Connection, *, user_id: int) -> dict:
    """Get the current user's profile."""
    user = user_repo.find_by_id(db, user_id)
    if not user:
        raise NotFoundError("User", user_id)
    return user.to_private_dict()
