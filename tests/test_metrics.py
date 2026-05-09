def test_metrics_endpoint_exposes_prometheus_metrics(client):
    client.get("/health")
    client.post("/chat", json={"message": "Metrics please"})

    response = client.get("/metrics")

    assert response.status_code == 200
    assert "http_requests_total" in response.text
    assert "http_request_duration_seconds" in response.text
    assert "llm_requests_total" in response.text


def test_metrics_do_not_expose_prompt_content(client):
    sensitive_prompt = "private-email-alice@example.test secret-token-123"

    client.post("/chat", json={"message": sensitive_prompt})
    response = client.get("/metrics")

    assert response.status_code == 200
    assert sensitive_prompt not in response.text
    assert "alice@example.test" not in response.text
    assert "secret-token-123" not in response.text


def test_metrics_do_not_expose_unmatched_raw_paths(client):
    raw_path = "/missing/private-user-id-123"

    response = client.get(raw_path)
    metrics = client.get("/metrics")

    assert response.status_code == 404
    assert raw_path not in metrics.text
    assert 'path="unmatched"' in metrics.text
