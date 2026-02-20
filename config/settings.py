"""Application settings — single source of truth via Pydantic BaseSettings."""

from __future__ import annotations

from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """GOH application settings loaded from environment variables."""

    model_config = {"env_prefix": "GOH_", "env_file": ".env", "env_file_encoding": "utf-8"}

    # Application
    env: str = Field(default="development", alias="GOH_ENV")
    debug: bool = Field(default=False, alias="GOH_DEBUG")
    secret_key: str = Field(default="change-me", alias="GOH_SECRET_KEY")

    # Database
    db_path: str = Field(default="./goh.db", alias="GOH_DB_PATH")

    # JWT
    jwt_secret: str = Field(default="change-me-jwt", alias="GOH_JWT_SECRET")
    jwt_access_expires_minutes: int = Field(default=30, alias="GOH_JWT_ACCESS_EXPIRES_MINUTES")
    jwt_refresh_expires_days: int = Field(default=30, alias="GOH_JWT_REFRESH_EXPIRES_DAYS")

    # Magic Link
    magic_link_expires_minutes: int = Field(default=15, alias="GOH_MAGIC_LINK_EXPIRES_MINUTES")
    magic_link_base_url: str = Field(
        default="http://localhost:5173", alias="GOH_MAGIC_LINK_BASE_URL"
    )

    # OAuth
    google_client_id: str = Field(default="", alias="GOH_GOOGLE_CLIENT_ID")
    google_client_secret: str = Field(default="", alias="GOH_GOOGLE_CLIENT_SECRET")
    discord_client_id: str = Field(default="", alias="GOH_DISCORD_CLIENT_ID")
    discord_client_secret: str = Field(default="", alias="GOH_DISCORD_CLIENT_SECRET")

    # Server
    host: str = Field(default="0.0.0.0", alias="GOH_HOST")
    port: int = Field(default=5050, alias="GOH_PORT")

    # Frontend
    frontend_url: str = Field(default="http://localhost:5173", alias="GOH_FRONTEND_URL")

    @property
    def is_production(self) -> bool:
        return self.env == "production"

    @property
    def is_development(self) -> bool:
        return self.env == "development"

    @property
    def db_path_resolved(self) -> Path:
        return Path(self.db_path).resolve()


def get_settings() -> Settings:
    """Get application settings (cached singleton pattern via module-level)."""
    return Settings()
