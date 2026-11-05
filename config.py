"""Application settings – loaded from environment / .env."""

from __future__ import annotations

from functools import lru_cache
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    ENVIRONMENT: str = "development"
    APP_NAME: str = "GoodLife Gateway Fabric"
    VERSION: str = "1.2.0"

    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8080

    # CORS – tighten in production
    CORS_ORIGINS: List[str] = ["*"]

    # Heartbeat file used by health checks
    HEARTBEAT_PATH: str = "/tmp/fabric_heartbeat.lock"

    # Secrets (set via fly secrets)
    SECRET_KEY: str = "change-me-in-production-use-fly-secrets"
    JWT_SECRET: str = "change-me-in-production-use-fly-secrets"

    # Optional email (contact form)
    SMTP_HOST: str | None = None
    SMTP_PORT: int = 587
    SMTP_USER: str | None = None
    SMTP_PASSWORD: str | None = None
    ADMIN_EMAIL: str = "david@odynexaxis.biz"
    EMAIL_FROM: str = "GoodLife Gateway <noreply@odynexaxis.biz>"


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
