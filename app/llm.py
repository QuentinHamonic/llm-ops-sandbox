from abc import ABC, abstractmethod
from dataclasses import dataclass

import httpx

from app.config import Settings


class LLMBackendError(RuntimeError):
    """Raised when the configured LLM backend cannot produce a reply."""


@dataclass(frozen=True)
class LLMBackendStatus:
    name: str
    available: bool
    model: str
    detail: str


class LLMBackend(ABC):
    name: str

    @abstractmethod
    async def generate(self, message: str) -> str:
        """Generate a reply for a user message."""

    @abstractmethod
    async def status(self) -> LLMBackendStatus:
        """Return a non-generative backend health signal."""


class MockBackend(LLMBackend):
    name = "mock"

    async def generate(self, message: str) -> str:
        return f"Mock reply: the local API is running. Received {len(message.strip())} characters."

    async def status(self) -> LLMBackendStatus:
        return LLMBackendStatus(
            name=self.name,
            available=True,
            model="mock",
            detail="Mock backend is always available and does not require a model service.",
        )


class OllamaBackend(LLMBackend):
    name = "ollama"

    def __init__(self, base_url: str, model: str) -> None:
        self.base_url = base_url.rstrip("/")
        self.model = model

    async def generate(self, message: str) -> str:
        payload = {
            "model": self.model,
            "prompt": message,
            "stream": False,
        }
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(f"{self.base_url}/api/generate", json=payload)
                response.raise_for_status()
        except httpx.HTTPError as exc:
            raise LLMBackendError(f"Ollama request failed: {exc}") from exc

        data = response.json()
        reply = data.get("response")
        if not isinstance(reply, str) or not reply.strip():
            raise LLMBackendError("Ollama response did not contain a usable 'response' field.")
        return reply.strip()

    async def status(self) -> LLMBackendStatus:
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(f"{self.base_url}/api/tags")
                response.raise_for_status()
        except httpx.HTTPError as exc:
            raise LLMBackendError(f"Ollama status check failed: {exc}") from exc

        data = response.json()
        models = data.get("models", [])
        available_models = {
            item.get("name")
            for item in models
            if isinstance(item, dict) and isinstance(item.get("name"), str)
        }
        if self.model in available_models:
            return LLMBackendStatus(
                name=self.name,
                available=True,
                model=self.model,
                detail="Configured Ollama model is available.",
            )
        return LLMBackendStatus(
            name=self.name,
            available=False,
            model=self.model,
            detail="Ollama is reachable, but the configured model is not listed.",
        )


def build_backend(settings: Settings) -> LLMBackend:
    if settings.llm_backend == "ollama":
        return OllamaBackend(settings.ollama_base_url, settings.ollama_model)
    return MockBackend()
