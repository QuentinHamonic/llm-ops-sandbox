from __future__ import annotations

import os
import subprocess
import sys
import tempfile
from collections.abc import Mapping, Sequence
from pathlib import Path


def run_step(name: str, command: Sequence[str], env: Mapping[str, str] | None = None) -> int:
    print(f"\n==> {name}", flush=True)
    print(" ".join(command), flush=True)
    completed = subprocess.run(command, check=False, env=env)
    return completed.returncode


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="llm-ops-docker-config-") as docker_config:
        docker_config_path = Path(docker_config)
        (docker_config_path / "config.json").write_text("{}\n", encoding="utf-8")
        docker_env = os.environ.copy()
        # Keep validation independent from the user's Docker credentials/config.
        docker_env["DOCKER_CONFIG"] = str(docker_config_path)

        steps = [
            ("ruff", [sys.executable, "-m", "ruff", "check", "."], None),
            ("ruff format", [sys.executable, "-m", "ruff", "format", "--check", "."], None),
            ("pytest", [sys.executable, "-m", "pytest"], None),
            ("api docs", [sys.executable, "scripts/export_api_docs.py", "--check"], None),
            ("gitlab ci", [sys.executable, "scripts/check_gitlab_ci.py"], None),
            ("gitops manifests", [sys.executable, "scripts/check_gitops_manifests.py"], None),
            ("vllm manifests", [sys.executable, "scripts/check_vllm_manifests.py"], None),
            ("kubernetes overlays", [sys.executable, "scripts/check_k8s_overlays.py"], None),
            ("docker compose config", ["docker", "compose", "config"], docker_env),
            ("kubernetes manifests", [sys.executable, "scripts/check_k8s_manifests.py"], None),
        ]

        for name, command, env in steps:
            return_code = run_step(name, command, env)
            if return_code != 0:
                print(f"\n{name} failed with exit code {return_code}.", flush=True)
                return return_code

    print("\nAll validation steps passed.", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
