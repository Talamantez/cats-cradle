from functools import lru_cache
from pydantic_settings import BaseSettings
from typing import List
from pydantic import ConfigDict

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "String Theory Dashboard"
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:8000", "http://localhost:3000"]
    REDIS_URL: str = "redis://redis:6379"

    model_config = ConfigDict(
        case_sensitive=True
    )

@lru_cache()
def get_settings() -> Settings:
    return Settings()