"""Tests for AppError hierarchy."""

from __future__ import annotations

from goh.domain.exceptions import (
    AppError,
    AuthenticationError,
    ConflictError,
    DuplicateError,
    ForbiddenError,
    InvalidCredentialsError,
    InvalidInputError,
    InvalidTokenError,
    NotFoundError,
    TokenExpiredError,
    ValidationError,
)


class TestAppError:
    def test_base_error(self) -> None:
        err = AppError("Something went wrong")
        assert err.message == "Something went wrong"
        assert err.status_code == 500
        assert err.error_code == "INTERNAL_ERROR"
        assert err.details == {}

    def test_base_error_with_details(self) -> None:
        err = AppError("Oops", details={"key": "value"})
        d = err.to_dict()
        assert d["error"] == "INTERNAL_ERROR"
        assert d["message"] == "Oops"
        assert d["details"] == {"key": "value"}

    def test_to_dict_without_details(self) -> None:
        err = AppError("Oops")
        d = err.to_dict()
        assert "details" not in d


class TestValidationErrors:
    def test_validation_error(self) -> None:
        err = ValidationError("Invalid field")
        assert err.status_code == 400
        assert err.error_code == "VALIDATION_ERROR"

    def test_invalid_input_error(self) -> None:
        err = InvalidInputError("Bad input")
        assert err.status_code == 400
        assert err.error_code == "INVALID_INPUT"


class TestAuthErrors:
    def test_authentication_error(self) -> None:
        err = AuthenticationError("Not authenticated")
        assert err.status_code == 401

    def test_invalid_credentials(self) -> None:
        err = InvalidCredentialsError()
        assert err.message == "Invalid credentials"
        assert err.status_code == 401
        assert err.error_code == "INVALID_CREDENTIALS"

    def test_token_expired(self) -> None:
        err = TokenExpiredError()
        assert err.message == "Token has expired"
        assert err.error_code == "TOKEN_EXPIRED"

    def test_invalid_token(self) -> None:
        err = InvalidTokenError()
        assert err.message == "Invalid token"
        assert err.error_code == "INVALID_TOKEN"


class TestForbiddenError:
    def test_default_message(self) -> None:
        err = ForbiddenError()
        assert err.message == "Access denied"
        assert err.status_code == 403

    def test_custom_message(self) -> None:
        err = ForbiddenError("Not your resource")
        assert err.message == "Not your resource"


class TestNotFoundError:
    def test_without_identifier(self) -> None:
        err = NotFoundError("User")
        assert err.message == "User not found"
        assert err.status_code == 404

    def test_with_identifier(self) -> None:
        err = NotFoundError("User", 42)
        assert err.message == "User with id '42' not found"
        assert err.details["resource"] == "User"


class TestConflictErrors:
    def test_conflict_error(self) -> None:
        err = ConflictError("Resource conflict")
        assert err.status_code == 409

    def test_duplicate_error(self) -> None:
        err = DuplicateError("User", "email", "test@example.com")
        assert err.status_code == 409
        assert err.error_code == "DUPLICATE"
        assert "test@example.com" in err.message
        assert err.details["field"] == "email"


class TestExceptionHierarchy:
    def test_all_inherit_from_app_error(self) -> None:
        errors = [
            ValidationError("x"),
            InvalidInputError("x"),
            AuthenticationError("x"),
            InvalidCredentialsError(),
            TokenExpiredError(),
            InvalidTokenError(),
            ForbiddenError(),
            NotFoundError("x"),
            ConflictError("x"),
            DuplicateError("x", "y", "z"),
        ]
        for err in errors:
            assert isinstance(err, AppError)

    def test_all_are_exceptions(self) -> None:
        err = NotFoundError("Test")
        assert isinstance(err, Exception)
