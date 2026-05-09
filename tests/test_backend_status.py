from app.config import get_settings
from app.llm import LLMBackendError, OllamaBackend


def test_backend_status_reports_mock_available(client):
    response = client.get("/backend/status")

    assert response.status_code == 200
    body = response.json()
    assert body["backend"] == "mock"
    assert body["available"] is True
    assert body["model"] == "mock"


def test_backend_status_reports_ollama_unavailable_without_prompt(client, monkeypatch):
    async def fail_status(self):
        raise LLMBackendError("Ollama status check failed: connection refused")

    monkeypatch.setenv("LLM_BACKEND", "ollama")
    monkeypatch.setenv("OLLAMA_MODEL", "mistral:latest")
    get_settings.cache_clear()
    monkeypatch.setattr(OllamaBackend, "status", fail_status)

    response = client.get("/backend/status")

    assert response.status_code == 200
    body = response.json()
    assert body["backend"] == "ollama"
    assert body["available"] is False
    assert body["model"] == "mistral:latest"
    assert "Ollama status check failed" in body["detail"]
