from functools import lru_cache
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    llm_backend: Literal["mock", "ollama"] = "mock"
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "mistral:latest"


@lru_cache
def get_settings() -> Settings:
    return Settings()
