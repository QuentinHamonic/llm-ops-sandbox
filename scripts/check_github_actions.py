from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
GITHUB_ACTIONS_CI = ROOT / ".github" / "workflows" / "ci.yml"


def load_workflow() -> dict[str, Any]:
    with GITHUB_ACTIONS_CI.open(encoding="utf-8") as yaml_file:
        data = yaml.safe_load(yaml_file)
    if not isinstance(data, dict):
        raise ValueError(".github/workflows/ci.yml does not contain a YAML object")
    return data


def assert_condition(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def step_runs(job: dict[str, Any], command: str) -> bool:
    steps = job.get("steps", [])
    return any(isinstance(step, dict) and step.get("run") == command for step in steps)


def step_uses(job: dict[str, Any], action: str) -> bool:
    steps = job.get("steps", [])
    return any(isinstance(step, dict) and step.get("uses") == action for step in steps)


def check_quality_job(jobs: dict[str, Any]) -> None:
    quality = jobs.get("quality")
    assert_condition(isinstance(quality, dict), "missing quality job")
    assert_condition(quality.get("runs-on") == "ubuntu-latest", "quality job must use Ubuntu")
    assert_condition(step_uses(quality, "actions/checkout@v6"), "quality job must checkout code")
    assert_condition(step_uses(quality, "actions/setup-python@v6"), "quality job must setup Python")

    expected_commands = [
        "ruff check .",
        "ruff format --check .",
        "pytest",
        "python scripts/export_api_docs.py --check",
        "python scripts/check_github_actions.py",
        "python scripts/check_gitlab_ci.py",
        "python scripts/check_gitops_manifests.py",
        "python scripts/check_monitoring_config.py",
        "python scripts/check_vllm_manifests.py",
        "python scripts/check_k8s_overlays.py",
        "python scripts/check_k8s_manifests.py",
    ]
    for command in expected_commands:
        assert_condition(step_runs(quality, command), f"quality job must run {command!r}")


def check_docker_job(jobs: dict[str, Any]) -> None:
    docker = jobs.get("docker")
    assert_condition(isinstance(docker, dict), "missing docker job")
    assert_condition(docker.get("needs") == "quality", "docker job must depend on quality")
    assert_condition(step_runs(docker, "docker version"), "docker job must show Docker version")
    assert_condition(step_runs(docker, "docker compose config"), "docker job must validate compose")
    assert_condition(
        step_runs(docker, "docker build -t llm-ops-sandbox-api:${{ github.sha }} ."),
        "docker job must build the API image",
    )


def main() -> int:
    if not GITHUB_ACTIONS_CI.exists():
        raise FileNotFoundError(GITHUB_ACTIONS_CI)

    workflow = load_workflow()
    assert_condition(workflow.get("name") == "CI", "workflow name must be CI")
    assert_condition(
        workflow.get("permissions") == {"contents": "read"},
        "permissions must be minimal",
    )

    triggers = workflow.get("on") or workflow.get(True)
    assert_condition(isinstance(triggers, dict), "workflow must define triggers")
    assert_condition("push" in triggers, "workflow must run on push")
    assert_condition("pull_request" in triggers, "workflow must run on pull_request")

    jobs = workflow.get("jobs")
    assert_condition(isinstance(jobs, dict), "workflow must define jobs")
    check_quality_job(jobs)
    check_docker_job(jobs)

    print("GitHub Actions static checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
