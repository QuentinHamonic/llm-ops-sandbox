from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
OVERLAYS = ROOT / "k8s" / "overlays"


def load_yaml(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as yaml_file:
        data = yaml.safe_load(yaml_file)
    if not isinstance(data, dict):
        raise ValueError(f"{path} does not contain a YAML object")
    return data


def assert_equal(actual: Any, expected: Any, message: str) -> None:
    if actual != expected:
        raise AssertionError(f"{message}: expected {expected!r}, got {actual!r}")


def check_overlay(name: str, backend: str, extra_resource: str | None = None) -> None:
    overlay_dir = OVERLAYS / name
    kustomization = load_yaml(overlay_dir / "kustomization.yaml")
    configmap_patch = load_yaml(overlay_dir / "configmap-patch.yaml")
    deployment_patch = load_yaml(overlay_dir / "deployment-patch.yaml")

    resources = kustomization.get("resources", [])
    assert_equal("../../base" in resources, True, f"{name} overlay includes base")
    if extra_resource is not None:
        assert_equal(extra_resource in resources, True, f"{name} overlay includes {extra_resource}")

    patches = [item.get("path") for item in kustomization.get("patches", [])]
    assert_equal("configmap-patch.yaml" in patches, True, f"{name} overlay config patch")
    assert_equal("deployment-patch.yaml" in patches, True, f"{name} overlay deployment patch")

    assert_equal(configmap_patch["data"].get("LLM_BACKEND"), backend, f"{name} backend")
    annotation = deployment_patch["spec"]["template"]["metadata"]["annotations"]
    assert_equal(annotation.get("llm-ops-sandbox.io/backend"), backend, f"{name} rollout marker")


def main() -> int:
    check_overlay("mock", "mock")
    check_overlay("ollama", "ollama")
    check_overlay("vllm", "vllm", "../../vllm")
    print("Kubernetes backend overlays static checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
