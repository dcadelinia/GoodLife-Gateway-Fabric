"""Application configuration – all secrets from environment."""

from __future__ import annotations

import os
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
    PORT: int = 8080

    # Security – must be overridden in production
    JWT_SECRET: str = "change-me-in-production-use-long-random-string"
    SECRET_KEY: str = "change-me-in-production-use-another-long-random-string"

    # Database (optional for Starter Kit)
    DATABASE_URL: str = ""

    # Optional integrations
    NVIDIA_API_KEY: str = ""
    ODYNEX_ALERT_WEBHOOK: str = ""

    # SMTP – optional contact form (never hard-code passwords)
    SMTP_HOST: str = ""
    SMTP_PORT: int = 465
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    SMTP_FROM: str = ""
    SMTP_TO: str = ""

    # CORS
    CORS_ORIGINS: List[str] = ["*"]

    # Orchestrator
    ORCHESTRATOR_INTERVAL_SEC: float = 5.0
    HEARTBEAT_PATH: str = "/tmp/fabric_heartbeat.lock"

    @property
    def is_production(self) -> bool:
        return self.ENVIRONMENT.lower() == "production"


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
