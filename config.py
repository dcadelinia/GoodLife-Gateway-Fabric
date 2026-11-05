from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
class Settings(BaseSettings):
    model_config = SettingsConfigDict(extra="ignore")
    ENVIRONMENT: str = "production"
    APP_NAME: str = "GoodLife Gateway Fabric"
    VERSION: str = "1.2.1"
    PORT: int = 8080
    HEARTBEAT_PATH: str = "/tmp/fabric_heartbeat.lock"
settings = Settings()
