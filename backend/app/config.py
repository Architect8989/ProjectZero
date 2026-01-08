from functools import lru_cache
from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    # Application
    APP_NAME: str = "UI Execution Backend"
    ENV: str = Field(default="development")

    # API
    API_PREFIX: str = ""

    # Database
    DATABASE_URL: str = Field(
        default="postgresql+psycopg2://user:password@localhost:5432/ui_exec"
    )

    # Storage (S3-compatible)
    STORAGE_ENDPOINT: str | None = None
    STORAGE_BUCKET: str | None = None
    STORAGE_ACCESS_KEY: str | None = None
    STORAGE_SECRET_KEY: str | None = None
    STORAGE_REGION: str | None = None

    # Security (v1: simple API key)
    API_KEY_HEADER: str = "X-API-Key"

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache
def get_settings() -> Settings:
    return Settings()
