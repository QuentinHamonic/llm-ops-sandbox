from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
GITOPS_LOCAL = ROOT / "gitops" / "local"


def load_yaml(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as yaml_file:
        data = yaml.safe_load(yaml_file)
    if not isinstance(data, dict):
        raise ValueError(f"{path} does not contain a YAML object")
    return data


def assert_equal(actual: Any, expected: Any, message: str) -> None:
    if actual != expected:
        raise AssertionError(f"{message}: expected {expected!r}, got {actual!r}")


def assert_no_secret_like_values(path: Path) -> None:
    forbidden_terms = ["password", "token", "secret", "private_key", "api_key"]
    content = path.read_text(encoding="utf-8").lower()
    for term in forbidden_terms:
        if term in content:
            raise AssertionError(f"{path} contains secret-like term {term!r}")


def check_source(source: dict[str, Any]) -> None:
    assert_equal(source.get("kind"), "GitRepository", "source kind")
    assert_equal(source["metadata"].get("namespace"), "flux-system", "source namespace")
    spec = source["spec"]
    assert_equal(spec.get("interval"), "1m", "source interval")
    assert_equal(spec["ref"].get("branch"), "main", "source branch")


def check_kustomization(kustomization: dict[str, Any]) -> None:
    assert_equal(kustomization.get("kind"), "Kustomization", "kustomization kind")
    spec = kustomization["spec"]
    assert_equal(spec.get("path"), "./k8s/base", "kustomization path")
    assert_equal(spec.get("prune"), True, "kustomization prune")
    assert_equal(spec.get("wait"), True, "kustomization wait")
    assert_equal(spec["sourceRef"].get("kind"), "GitRepository", "sourceRef kind")
    assert_equal(spec["sourceRef"].get("name"), "llm-ops-sandbox", "sourceRef name")


def check_helm_repository(repository: dict[str, Any]) -> None:
    assert_equal(repository.get("kind"), "HelmRepository", "helm repository kind")
    assert_equal(
        repository["metadata"].get("namespace"),
        "flux-system",
        "helm repository namespace",
    )
    assert_equal(
        repository["spec"].get("url"),
        "https://prometheus-community.github.io/helm-charts",
        "helm repository url",
    )


def check_helm_release(release: dict[str, Any]) -> None:
    assert_equal(release.get("kind"), "HelmRelease", "helm release kind")
    assert_equal(release["metadata"].get("namespace"), "flux-system", "helm release namespace")
    chart_spec = release["spec"]["chart"]["spec"]
    assert_equal(chart_spec.get("chart"), "kube-prometheus-stack", "helm chart")
    assert_equal(chart_spec["sourceRef"].get("kind"), "HelmRepository", "helm source kind")
    assert_equal(chart_spec["sourceRef"].get("name"), "prometheus-community", "helm source name")


def main() -> int:
    expected_files = [
        GITOPS_LOCAL / "source.yaml",
        GITOPS_LOCAL / "kustomization.yaml",
        GITOPS_LOCAL / "helmrepository-monitoring-example.yaml",
        GITOPS_LOCAL / "helmrelease-monitoring-example.yaml",
        GITOPS_LOCAL / "README.md",
    ]

    for path in expected_files:
        if not path.exists():
            raise FileNotFoundError(path)
        if path.suffix in {".yaml", ".yml"}:
            assert_no_secret_like_values(path)

    check_source(load_yaml(GITOPS_LOCAL / "source.yaml"))
    check_kustomization(load_yaml(GITOPS_LOCAL / "kustomization.yaml"))
    check_helm_repository(load_yaml(GITOPS_LOCAL / "helmrepository-monitoring-example.yaml"))
    check_helm_release(load_yaml(GITOPS_LOCAL / "helmrelease-monitoring-example.yaml"))

    print("GitOps manifests static checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
