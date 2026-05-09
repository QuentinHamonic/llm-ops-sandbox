import os

import pytest
from fastapi.testclient import TestClient

from app.config import get_settings
from app.main import app

pytestmark = pytest.mark.integration


@pytest.mark.skipif(
    os.getenv("OLLAMA_INTEGRATION") != "1",
    reason="Set OLLAMA_INTEGRATION=1 to call a local Ollama service.",
)
def test_chat_with_real_ollama_backend(monkeypatch):
    monkeypatch.setenv("LLM_BACKEND", "ollama")
    monkeypatch.setenv("OLLAMA_BASE_URL", os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"))
    monkeypatch.setenv("OLLAMA_MODEL", os.getenv("OLLAMA_MODEL", "mistral:latest"))
    get_settings.cache_clear()

    with TestClient(app) as client:
        status_response = client.get("/backend/status")
        chat_response = client.post("/chat", json={"message": "Reply with exactly: OK"})

    assert status_response.status_code == 200
    assert status_response.json()["available"] is True
    assert chat_response.status_code == 200
    assert chat_response.json()["backend"] == "ollama"
