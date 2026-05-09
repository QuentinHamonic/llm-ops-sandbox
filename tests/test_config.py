from app.config import get_settings


def test_default_backend_is_mock(monkeypatch):
    monkeypatch.delenv("LLM_BACKEND", raising=False)
    get_settings.cache_clear()

    settings = get_settings()

    assert settings.llm_backend == "mock"
