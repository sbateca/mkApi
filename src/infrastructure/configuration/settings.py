from functools import lru_cache
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(extra="ignore")

    database_url: str
    jwt_secret_key: str = Field(min_length=32)
    jwt_algorithm: Literal["HS256", "HS384", "HS512"] = "HS256"
    jwt_expiration_seconds: int = Field(default=900, gt=0)
    refresh_token_expiration_seconds: int = Field(default=2592000, gt=0)


@lru_cache
def get_settings() -> Settings:
    return Settings()
