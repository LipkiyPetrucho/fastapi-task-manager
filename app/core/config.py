from functools import lru_cache

from pydantic import PostgresDsn, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: PostgresDsn = Field(..., alias="DATABASE_URL")

    jwt_secret: str = Field(..., alias="JWT_SECRET")
    jwt_algo: str = Field(default="HS256", alias="JWT_ALGO")
    access_expires_minutes: int = Field(default=30, alias="ACCESS_EXPIRES_MINUTES")
    refresh_expires_days: int = Field(default=7, alias="REFRESH_EXPIRES_DAYS")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
