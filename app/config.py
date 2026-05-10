from functools import lru_cache
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    llm_backend: Literal["mock", "ollama", "vllm"] = "mock"
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "mistral:latest"
    vllm_base_url: str = "http://localhost:8001/v1"
    vllm_model: str = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"


@lru_cache
def get_settings() -> Settings:
    return Settings()
