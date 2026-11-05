from __future__ import annotations
from functools import lru_cache
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    ENVIRONMENT: str = "production"
    APP_NAME: str = "GoodLife Gateway Fabric"
    VERSION: str = "1.2.1"
    PORT: int = 8080
    CORS_ORIGINS: List[str] = ["*"]
    HEARTBEAT_PATH: str = "/tmp/fabric_heartbeat.lock"
    SECRET_KEY: str = "set-via-fly-secrets"

@lru_cache
def get_settings() -> Settings:
    return Settings()

settings = get_settings()
