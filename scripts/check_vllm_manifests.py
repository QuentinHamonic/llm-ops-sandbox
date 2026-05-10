from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
VLLM_DIR = ROOT / "k8s" / "vllm"


def load_yaml(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as yaml_file:
        data = yaml.safe_load(yaml_file)
    if not isinstance(data, dict):
        raise ValueError(f"{path} does not contain a YAML object")
    return data


def assert_equal(actual: Any, expected: Any, message: str) -> None:
    if actual != expected:
        raise AssertionError(f"{message}: expected {expected!r}, got {actual!r}")


def check_configmap(configmap: dict[str, Any]) -> None:
    assert_equal(configmap.get("kind"), "ConfigMap", "vLLM configmap kind")
    data = configmap["data"]
    assert_equal(
        data.get("VLLM_MODEL"),
        "TinyLlama/TinyLlama-1.1B-Chat-v1.0",
        "vLLM model",
    )
    assert_equal(data.get("VLLM_PORT"), "8000", "vLLM port")


def check_deployment(deployment: dict[str, Any]) -> None:
    assert_equal(deployment.get("kind"), "Deployment", "vLLM deployment kind")
    container = deployment["spec"]["template"]["spec"]["containers"][0]
    assert_equal(
        container.get("image"),
        "vllm/vllm-openai:REPLACE_WITH_TESTED_VERSION",
        "vLLM image placeholder",
    )
    assert_equal(container["ports"][0].get("containerPort"), 8000, "vLLM container port")
    assert_equal(
        container["readinessProbe"]["httpGet"].get("path"),
        "/health",
        "vLLM readiness path",
    )

    resources = container["resources"]
    assert_equal(resources["limits"].get("nvidia.com/gpu"), "1", "vLLM gpu limit")
    assert_equal(resources["requests"].get("nvidia.com/gpu"), "1", "vLLM gpu request")


def check_service(service: dict[str, Any]) -> None:
    assert_equal(service.get("kind"), "Service", "vLLM service kind")
    assert_equal(service["metadata"].get("name"), "vllm-openai", "vLLM service name")
    assert_equal(service["spec"]["ports"][0].get("port"), 8000, "vLLM service port")


def main() -> int:
    required_files = [
        VLLM_DIR / "kustomization.yaml",
        VLLM_DIR / "configmap.yaml",
        VLLM_DIR / "deployment.yaml",
        VLLM_DIR / "service.yaml",
    ]
    for path in required_files:
        if not path.exists():
            raise FileNotFoundError(path)

    check_configmap(load_yaml(VLLM_DIR / "configmap.yaml"))
    check_deployment(load_yaml(VLLM_DIR / "deployment.yaml"))
    check_service(load_yaml(VLLM_DIR / "service.yaml"))

    print("vLLM manifests static checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
