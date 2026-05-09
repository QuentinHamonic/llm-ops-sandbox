from abc import ABC, abstractmethod

import httpx

from app.config import Settings


class LLMBackendError(RuntimeError):
    """Raised when the configured LLM backend cannot produce a reply."""


class LLMBackend(ABC):
    name: str

    @abstractmethod
    async def generate(self, message: str) -> str:
        """Generate a reply for a user message."""


class MockBackend(LLMBackend):
    name = "mock"

    async def generate(self, message: str) -> str:
        return f"Mock reply: the local API is running. Received {len(message.strip())} characters."


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


def build_backend(settings: Settings) -> LLMBackend:
    if settings.llm_backend == "ollama":
        return OllamaBackend(settings.ollama_base_url, settings.ollama_model)
    return MockBackend()
