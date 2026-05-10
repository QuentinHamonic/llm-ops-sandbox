from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
K8S_BASE = ROOT / "k8s" / "base"


def load_yaml(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as yaml_file:
        data = yaml.safe_load(yaml_file)
    if not isinstance(data, dict):
        raise ValueError(f"{path} does not contain a YAML object")
    return data


def assert_equal(actual: Any, expected: Any, message: str) -> None:
    if actual != expected:
        raise AssertionError(f"{message}: expected {expected!r}, got {actual!r}")


def assert_in(key: str, value: dict[str, Any], message: str) -> None:
    if key not in value:
        raise AssertionError(f"{message}: missing {key!r}")


def check_configmap(configmap: dict[str, Any]) -> None:
    assert_equal(configmap.get("kind"), "ConfigMap", "configmap kind")
    data = configmap.get("data", {})
    assert_equal(data.get("LLM_BACKEND"), "mock", "default backend")
    assert_equal(data.get("OLLAMA_MODEL"), "mistral:latest", "default Ollama model")


def check_deployment(deployment: dict[str, Any]) -> None:
    assert_equal(deployment.get("kind"), "Deployment", "deployment kind")
    spec = deployment["spec"]
    template = spec["template"]
    pod_metadata = template["metadata"]
    annotations = pod_metadata.get("annotations", {})
    assert_equal(annotations.get("prometheus.io/scrape"), "true", "pod scrape annotation")

    container = template["spec"]["containers"][0]
    assert_equal(container.get("image"), "llm-ops-sandbox-api:0.6.0", "deployment image")
    assert_in("livenessProbe", container, "deployment container")
    assert_in("readinessProbe", container, "deployment container")
    assert_equal(
        container["livenessProbe"]["httpGet"]["path"],
        "/health",
        "liveness probe path",
    )
    assert_equal(
        container["readinessProbe"]["httpGet"]["path"],
        "/health",
        "readiness probe path",
    )

    resources = container.get("resources", {})
    assert_in("requests", resources, "deployment resources")
    assert_in("limits", resources, "deployment resources")
    assert_equal(resources["requests"].get("cpu"), "100m", "cpu request")
    assert_equal(resources["limits"].get("memory"), "512Mi", "memory limit")


def check_service(service: dict[str, Any]) -> None:
    assert_equal(service.get("kind"), "Service", "service kind")
    annotations = service["metadata"].get("annotations", {})
    assert_equal(annotations.get("prometheus.io/scrape"), "true", "service scrape annotation")
    ports = service["spec"]["ports"]
    assert_equal(ports[0].get("port"), 8000, "service port")
    assert_equal(ports[0].get("targetPort"), "http", "service target port")


def main() -> int:
    required_files = [
        K8S_BASE / "kustomization.yaml",
        K8S_BASE / "configmap.yaml",
        K8S_BASE / "deployment.yaml",
        K8S_BASE / "service.yaml",
    ]
    for path in required_files:
        if not path.exists():
            raise FileNotFoundError(path)

    check_configmap(load_yaml(K8S_BASE / "configmap.yaml"))
    check_deployment(load_yaml(K8S_BASE / "deployment.yaml"))
    check_service(load_yaml(K8S_BASE / "service.yaml"))
    print("Kubernetes manifests static checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
