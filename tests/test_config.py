from app.config import get_settings


def test_default_backend_is_mock(monkeypatch):
    monkeypatch.delenv("LLM_BACKEND", raising=False)
    monkeypatch.delenv("OLLAMA_BASE_URL", raising=False)
    monkeypatch.delenv("OLLAMA_MODEL", raising=False)
    get_settings.cache_clear()

    settings = get_settings()

    assert settings.llm_backend == "mock"
    assert settings.ollama_base_url == "http://localhost:11434"
    assert settings.ollama_model == "mistral:latest"
