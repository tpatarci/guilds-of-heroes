"""Auth middleware — JWT verification for protected routes."""

from __future__ import annotations

import functools
from typing import Any

from flask import current_app, g, request

from goh.domain.exceptions import AuthenticationError
from goh.services.auth_service import verify_access_token


def require_auth(f):  # type: ignore[no-untyped-def]
    """Decorator that requires a valid JWT access token."""
    @functools.wraps(f)
    def decorated(*args: Any, **kwargs: Any) -> Any:
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            raise AuthenticationError("Missing or invalid Authorization header")

        token = auth_header[7:]
        settings = current_app.config["SETTINGS"]
        payload = verify_access_token(token, jwt_secret=settings.jwt_secret)
        g.user_id = payload["sub"]
        g.username = payload["username"]
        g.user_role = payload["role"]
        return f(*args, **kwargs)

    return decorated
