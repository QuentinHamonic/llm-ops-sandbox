from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
GITLAB_CI = ROOT / ".gitlab-ci.yml"


def load_gitlab_ci() -> dict[str, Any]:
    with GITLAB_CI.open(encoding="utf-8-sig") as yaml_file:
        data = yaml.safe_load(yaml_file)
    if not isinstance(data, dict):
        raise ValueError(".gitlab-ci.yml does not contain a YAML object")
    return data


def assert_job_script_contains(config: dict[str, Any], job: str, command: str) -> None:
    job_config = config.get(job)
    if not isinstance(job_config, dict):
        raise AssertionError(f"missing GitLab CI job: {job}")

    script = job_config.get("script")
    if not isinstance(script, list):
        raise AssertionError(f"job {job} has no script list")

    if command not in script:
        raise AssertionError(f"job {job} does not run {command!r}")


def main() -> int:
    if not GITLAB_CI.exists():
        raise FileNotFoundError(GITLAB_CI)

    config = load_gitlab_ci()
    expected_stages = ["lint", "test", "validate", "build"]
    if config.get("stages") != expected_stages:
        raise AssertionError(f"unexpected GitLab CI stages: {config.get('stages')!r}")

    assert_job_script_contains(config, "lint", "ruff check .")
    assert_job_script_contains(config, "lint", "ruff format --check .")
    assert_job_script_contains(config, "test", "pytest")
    assert_job_script_contains(
        config,
        "api-docs-check",
        "python scripts/export_api_docs.py --check",
    )
    assert_job_script_contains(config, "compose-config", "docker compose config")
    assert_job_script_contains(config, "k8s-static-check", "python scripts/check_k8s_manifests.py")
    assert_job_script_contains(
        config,
        "gitops-static-check",
        "python scripts/check_gitops_manifests.py",
    )
    assert_job_script_contains(
        config,
        "docker-build",
        "docker build -t llm-ops-sandbox-api:$CI_COMMIT_SHORT_SHA .",
    )

    print("GitLab CI static checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
