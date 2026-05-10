from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPORTER_PATH = ROOT / "scripts" / "gpu_metrics_exporter.py"


def load_exporter():
    spec = importlib.util.spec_from_file_location("gpu_metrics_exporter", EXPORTER_PATH)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules["gpu_metrics_exporter"] = module
    spec.loader.exec_module(module)
    return module


def test_parse_nvidia_smi_csv_output():
    exporter = load_exporter()
    output = "0, NVIDIA GeForce RTX 5090, 32607, 1024, 31583, 42, 55, 120.50, 600.00\n"

    samples = exporter.parse_nvidia_smi_csv(output)

    assert len(samples) == 1
    assert samples[0].index == "0"
    assert samples[0].name == "NVIDIA GeForce RTX 5090"
    assert samples[0].memory_total_mib == 32607
    assert samples[0].utilization_percent == 42
    assert samples[0].power_draw_watts == 120.50


def test_render_prometheus_metrics_keeps_labels_bounded():
    exporter = load_exporter()
    sample = exporter.GpuSample(
        index="0",
        name="NVIDIA GeForce RTX 5090",
        memory_total_mib=32607,
        memory_used_mib=1024,
        memory_free_mib=31583,
        utilization_percent=42,
        temperature_celsius=55,
        power_draw_watts=120.5,
        power_limit_watts=600,
    )

    metrics = exporter.render_prometheus([sample], exporter_up=True)

    assert "gpu_exporter_up 1" in metrics
    assert 'gpu_memory_total_bytes{gpu="0",name="NVIDIA GeForce RTX 5090"}' in metrics
    assert "gpu_utilization_ratio" in metrics
    assert "gpu_temperature_celsius" in metrics
    assert "gpu_power_draw_watts" in metrics


def test_render_prometheus_failure_does_not_expose_command_errors():
    exporter = load_exporter()

    metrics = exporter.render_prometheus([], exporter_up=False)

    assert "gpu_exporter_up 0" in metrics
    assert "No such file" not in metrics
    assert "Permission denied" not in metrics
    assert "Traceback" not in metrics
