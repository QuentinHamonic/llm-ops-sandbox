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
