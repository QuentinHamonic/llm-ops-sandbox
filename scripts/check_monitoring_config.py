from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
PROMETHEUS_CONFIG = ROOT / "monitoring" / "prometheus" / "prometheus.yml"
GPU_DASHBOARD = ROOT / "monitoring" / "grafana" / "dashboards" / "llm-ops-gpu.json"


def load_yaml(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as yaml_file:
        data = yaml.safe_load(yaml_file)
    if not isinstance(data, dict):
        raise ValueError(f"{path} does not contain a YAML object")
    return data


def load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as json_file:
        data = json.load(json_file)
    if not isinstance(data, dict):
        raise ValueError(f"{path} does not contain a JSON object")
    return data


def assert_condition(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def check_prometheus_gpu_job(config: dict[str, Any]) -> None:
    scrape_configs = config.get("scrape_configs", [])
    gpu_jobs = [job for job in scrape_configs if job.get("job_name") == "llm-ops-sandbox-gpu"]
    assert_condition(len(gpu_jobs) == 1, "Prometheus must define one GPU scrape job")

    static_configs = gpu_jobs[0].get("static_configs", [])
    targets = [target for item in static_configs for target in item.get("targets", [])]
    assert_condition(
        "host.docker.internal:9101" in targets,
        "GPU scrape job must target host.docker.internal:9101",
    )


def check_gpu_dashboard(dashboard: dict[str, Any]) -> None:
    assert_condition(dashboard.get("uid") == "llm-ops-gpu", "GPU dashboard uid mismatch")
    panels = dashboard.get("panels", [])
    expressions = {
        target.get("expr")
        for panel in panels
        for target in panel.get("targets", [])
        if isinstance(target, dict)
    }
    expected = {
        "gpu_exporter_up",
        "gpu_utilization_ratio",
        "gpu_memory_used_bytes",
        "gpu_memory_total_bytes",
        "gpu_temperature_celsius",
        "gpu_power_draw_watts",
        "gpu_power_limit_watts",
    }
    missing = expected - expressions
    assert_condition(not missing, f"GPU dashboard missing expressions: {sorted(missing)}")


def main() -> int:
    check_prometheus_gpu_job(load_yaml(PROMETHEUS_CONFIG))
    check_gpu_dashboard(load_json(GPU_DASHBOARD))
    print("Monitoring config static checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
