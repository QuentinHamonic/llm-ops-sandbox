from app.config import get_settings
from app.llm import LLMBackendError, OllamaBackend, VLLMBackend


def test_chat_uses_mock_backend_by_default(client):
    response = client.post("/chat", json={"message": "Hello"})

    assert response.status_code == 200
    body = response.json()
    assert body["backend"] == "mock"
    assert "Mock reply" in body["reply"]


def test_chat_rejects_empty_message(client):
    response = client.post("/chat", json={"message": ""})

    assert response.status_code == 422


def test_chat_rejects_missing_message(client):
    response = client.post("/chat", json={})

    assert response.status_code == 422


def test_chat_rejects_too_long_message(client):
    response = client.post("/chat", json={"message": "x" * 4001})

    assert response.status_code == 422


def test_chat_returns_bad_gateway_when_ollama_backend_fails(client, monkeypatch):
    async def fail_generate(self, message: str) -> str:
        raise LLMBackendError("Ollama request failed: connection refused")

    monkeypatch.setenv("LLM_BACKEND", "ollama")
    get_settings.cache_clear()
    monkeypatch.setattr(OllamaBackend, "generate", fail_generate)

    response = client.post("/chat", json={"message": "Hello"})

    assert response.status_code == 502
    assert "Ollama request failed" in response.json()["detail"]


def test_chat_returns_bad_gateway_when_vllm_backend_fails(client, monkeypatch):
    async def fail_generate(self, message: str) -> str:
        raise LLMBackendError("vLLM request failed: connection refused")

    monkeypatch.setenv("LLM_BACKEND", "vllm")
    get_settings.cache_clear()
    monkeypatch.setattr(VLLMBackend, "generate", fail_generate)

    response = client.post("/chat", json={"message": "Hello"})

    assert response.status_code == 502
    assert "vLLM request failed" in response.json()["detail"]
