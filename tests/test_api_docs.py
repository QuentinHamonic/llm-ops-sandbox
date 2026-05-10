import json
import subprocess
import sys


def test_openapi_exposes_documented_contract(client):
    response = client.get("/openapi.json")

    assert response.status_code == 200
    schema = response.json()
    assert schema["info"]["version"] == "0.10.0"
    assert schema["paths"]["/health"]["get"]["tags"] == ["Health"]
    assert schema["paths"]["/chat"]["post"]["responses"]["502"]["description"]
    assert schema["paths"]["/backend/status"]["get"]["tags"] == ["Backend"]
    assert schema["paths"]["/metrics"]["get"]["tags"] == ["Observability"]


def test_export_api_docs_generates_openapi_and_markdown():
    result = subprocess.run(
        [sys.executable, "scripts/export_api_docs.py", "--check"],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stdout + result.stderr

    with open("docs/generated/openapi.json", encoding="utf-8") as openapi_file:
        schema = json.load(openapi_file)

    with open("docs/generated/api.md", encoding="utf-8") as markdown_file:
        markdown = markdown_file.read()

    assert schema["info"]["version"] == "0.10.0"
    assert "GET `/backend/status`" in markdown
    assert "POST `/chat`" in markdown
    assert "GET `/metrics`" in markdown
