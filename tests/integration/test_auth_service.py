"""Integration tests for auth_service — uses real SQLite."""

from __future__ import annotations

import sqlite3

import pytest

from goh.domain.exceptions import (
    DuplicateError,
    InvalidCredentialsError,
    InvalidTokenError,
    ValidationError,
)
from goh.services import auth_service

JWT_SECRET = "test-secret"


def _register_user(db: sqlite3.Connection, username: str = "testuser") -> dict:
    return auth_service.register(
        db,
        username=username,
        email=f"{username}@test.com",
        password="password123",
        jwt_secret=JWT_SECRET,
    )


class TestRegister:
    def test_register_success(self, db: sqlite3.Connection) -> None:
        result = _register_user(db)
        assert result["user"]["username"] == "testuser"
        assert result["user"]["email"] == "testuser@test.com"
        assert "access_token" in result
        assert "refresh_token" in result

    def test_register_duplicate_username(self, db: sqlite3.Connection) -> None:
        _register_user(db)
        with pytest.raises(DuplicateError, match="username"):
            _register_user(db)

    def test_register_duplicate_email(self, db: sqlite3.Connection) -> None:
        _register_user(db)
        with pytest.raises(DuplicateError, match="email"):
            auth_service.register(
                db,
                username="other",
                email="testuser@test.com",
                password="password123",
                jwt_secret=JWT_SECRET,
            )

    def test_register_short_username(self, db: sqlite3.Connection) -> None:
        with pytest.raises(ValidationError, match="Username"):
            auth_service.register(
                db, username="ab", email="a@b.com", password="password123", jwt_secret=JWT_SECRET
            )

    def test_register_short_password(self, db: sqlite3.Connection) -> None:
        with pytest.raises(ValidationError, match="Password"):
            auth_service.register(
                db, username="testuser", email="a@b.com", password="short", jwt_secret=JWT_SECRET
            )

    def test_register_invalid_email(self, db: sqlite3.Connection) -> None:
        with pytest.raises(ValidationError, match="email"):
            auth_service.register(
                db, username="testuser", email="invalid", password="password123",
                jwt_secret=JWT_SECRET,
            )


class TestLoginPassword:
    def test_login_success(self, db: sqlite3.Connection) -> None:
        _register_user(db)
        result = auth_service.login_password(
            db, username="testuser", password="password123", jwt_secret=JWT_SECRET
        )
        assert result["user"]["username"] == "testuser"
        assert "access_token" in result
        assert "refresh_token" in result

    def test_login_wrong_password(self, db: sqlite3.Connection) -> None:
        _register_user(db)
        with pytest.raises(InvalidCredentialsError):
            auth_service.login_password(
                db, username="testuser", password="wrong", jwt_secret=JWT_SECRET
            )

    def test_login_nonexistent_user(self, db: sqlite3.Connection) -> None:
        with pytest.raises(InvalidCredentialsError):
            auth_service.login_password(
                db, username="nobody", password="password123", jwt_secret=JWT_SECRET
            )


class TestMagicLink:
    def test_create_and_verify(self, db: sqlite3.Connection) -> None:
        _register_user(db)
        link = auth_service.create_magic_link(db, email="testuser@test.com")
        assert "token" in link

        result = auth_service.login_magic_link(
            db, token=link["token"], jwt_secret=JWT_SECRET
        )
        assert result["user"]["username"] == "testuser"
        assert result["user"]["email_verified"] is True

    def test_invalid_magic_link(self, db: sqlite3.Connection) -> None:
        with pytest.raises(InvalidTokenError):
            auth_service.login_magic_link(
                db, token="bogus-token", jwt_secret=JWT_SECRET
            )

    def test_used_magic_link(self, db: sqlite3.Connection) -> None:
        _register_user(db)
        link = auth_service.create_magic_link(db, email="testuser@test.com")
        auth_service.login_magic_link(db, token=link["token"], jwt_secret=JWT_SECRET)

        with pytest.raises(InvalidTokenError):
            auth_service.login_magic_link(db, token=link["token"], jwt_secret=JWT_SECRET)


class TestTokens:
    def test_verify_access_token(self, db: sqlite3.Connection) -> None:
        result = _register_user(db)
        payload = auth_service.verify_access_token(
            result["access_token"], jwt_secret=JWT_SECRET
        )
        assert payload["username"] == "testuser"
        assert payload["type"] == "access"

    def test_invalid_access_token(self) -> None:
        with pytest.raises(InvalidTokenError):
            auth_service.verify_access_token("bogus", jwt_secret=JWT_SECRET)

    def test_refresh_tokens(self, db: sqlite3.Connection) -> None:
        result = _register_user(db)
        new_tokens = auth_service.refresh_tokens(
            db, refresh_token=result["refresh_token"], jwt_secret=JWT_SECRET
        )
        assert "access_token" in new_tokens
        assert "refresh_token" in new_tokens
        # Old refresh should be revoked
        with pytest.raises(InvalidTokenError):
            auth_service.refresh_tokens(
                db, refresh_token=result["refresh_token"], jwt_secret=JWT_SECRET
            )


class TestLogout:
    def test_logout_revokes_session(self, db: sqlite3.Connection) -> None:
        result = _register_user(db)
        auth_service.logout(db, refresh_token=result["refresh_token"])
        # Refresh should fail after logout
        with pytest.raises(InvalidTokenError):
            auth_service.refresh_tokens(
                db, refresh_token=result["refresh_token"], jwt_secret=JWT_SECRET
            )


class TestWhoami:
    def test_whoami(self, db: sqlite3.Connection) -> None:
        result = _register_user(db)
        payload = auth_service.verify_access_token(
            result["access_token"], jwt_secret=JWT_SECRET
        )
        user_info = auth_service.whoami(db, user_id=payload["sub"])
        assert user_info["username"] == "testuser"
