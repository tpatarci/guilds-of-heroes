"""AppError hierarchy — all custom exceptions for the GOH application."""

from __future__ import annotations


class AppError(Exception):
    """Base application error with HTTP status code mapping."""

    status_code: int = 500
    error_code: str = "INTERNAL_ERROR"

    def __init__(self, message: str, details: dict | None = None) -> None:
        super().__init__(message)
        self.message = message
        self.details = details or {}

    def to_dict(self) -> dict:
        result: dict = {
            "error": self.error_code,
            "message": self.message,
        }
        if self.details:
            result["details"] = self.details
        return result


# --- 400 Bad Request ---


class ValidationError(AppError):
    status_code = 400
    error_code = "VALIDATION_ERROR"


class InvalidInputError(AppError):
    status_code = 400
    error_code = "INVALID_INPUT"


# --- 401 Unauthorized ---


class AuthenticationError(AppError):
    status_code = 401
    error_code = "AUTHENTICATION_ERROR"


class InvalidCredentialsError(AuthenticationError):
    error_code = "INVALID_CREDENTIALS"

    def __init__(self) -> None:
        super().__init__("Invalid credentials")


class TokenExpiredError(AuthenticationError):
    error_code = "TOKEN_EXPIRED"

    def __init__(self) -> None:
        super().__init__("Token has expired")


class InvalidTokenError(AuthenticationError):
    error_code = "INVALID_TOKEN"

    def __init__(self) -> None:
        super().__init__("Invalid token")


# --- 403 Forbidden ---


class ForbiddenError(AppError):
    status_code = 403
    error_code = "FORBIDDEN"

    def __init__(self, message: str = "Access denied") -> None:
        super().__init__(message)


# --- 404 Not Found ---


class NotFoundError(AppError):
    status_code = 404
    error_code = "NOT_FOUND"

    def __init__(self, resource: str, identifier: str | int = "") -> None:
        msg = f"{resource} not found"
        if identifier:
            msg = f"{resource} with id '{identifier}' not found"
        super().__init__(msg, {"resource": resource, "identifier": str(identifier)})


# --- 409 Conflict ---


class ConflictError(AppError):
    status_code = 409
    error_code = "CONFLICT"


class DuplicateError(ConflictError):
    error_code = "DUPLICATE"

    def __init__(self, resource: str, field: str, value: str) -> None:
        super().__init__(
            f"{resource} with {field} '{value}' already exists",
            {"resource": resource, "field": field, "value": value},
        )
