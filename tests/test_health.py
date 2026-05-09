def test_health_returns_service_status(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.json()["service"] == "llm-ops-sandbox"
    assert response.json()["llm_backend"] == "mock"
