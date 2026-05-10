from __future__ import annotations

import argparse
import csv
import subprocess
from dataclasses import dataclass
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from io import StringIO

NVIDIA_SMI_QUERY = [
    "nvidia-smi",
    "--query-gpu=index,name,memory.total,memory.used,memory.free,utilization.gpu,temperature.gpu,power.draw,power.limit",
    "--format=csv,noheader,nounits",
]


@dataclass(frozen=True)
class GpuSample:
    index: str
    name: str
    memory_total_mib: float
    memory_used_mib: float
    memory_free_mib: float
    utilization_percent: float
    temperature_celsius: float | None
    power_draw_watts: float | None
    power_limit_watts: float | None


def parse_optional_float(value: str) -> float | None:
    value = value.strip()
    if not value or value.upper() in {"N/A", "[N/A]"}:
        return None
    return float(value)


def parse_nvidia_smi_csv(output: str) -> list[GpuSample]:
    samples: list[GpuSample] = []
    reader = csv.reader(StringIO(output))
    for row in reader:
        if len(row) != 9:
            raise ValueError(f"Expected 9 columns from nvidia-smi, got {len(row)}")
        samples.append(
            GpuSample(
                index=row[0].strip(),
                name=row[1].strip(),
                memory_total_mib=float(row[2].strip()),
                memory_used_mib=float(row[3].strip()),
                memory_free_mib=float(row[4].strip()),
                utilization_percent=float(row[5].strip()),
                temperature_celsius=parse_optional_float(row[6]),
                power_draw_watts=parse_optional_float(row[7]),
                power_limit_watts=parse_optional_float(row[8]),
            )
        )
    return samples


def prometheus_escape(value: str) -> str:
    return value.replace("\\", "\\\\").replace("\n", "\\n").replace('"', '\\"')


def gpu_labels(sample: GpuSample) -> str:
    return f'gpu="{prometheus_escape(sample.index)}",name="{prometheus_escape(sample.name)}"'


def mib_to_bytes(value: float) -> float:
    return value * 1024 * 1024


def metric_line(name: str, labels: str, value: float) -> str:
    return f"{name}{{{labels}}} {value:.6f}"


def render_prometheus(samples: list[GpuSample], exporter_up: bool) -> str:
    lines = [
        "# HELP gpu_exporter_up Whether the local GPU exporter can read nvidia-smi.",
        "# TYPE gpu_exporter_up gauge",
        f"gpu_exporter_up {1 if exporter_up else 0}",
        "# HELP gpu_memory_total_bytes Total GPU memory in bytes.",
        "# TYPE gpu_memory_total_bytes gauge",
        "# HELP gpu_memory_used_bytes Used GPU memory in bytes.",
        "# TYPE gpu_memory_used_bytes gauge",
        "# HELP gpu_memory_free_bytes Free GPU memory in bytes.",
        "# TYPE gpu_memory_free_bytes gauge",
        "# HELP gpu_utilization_ratio GPU utilization as a ratio from 0 to 1.",
        "# TYPE gpu_utilization_ratio gauge",
        "# HELP gpu_temperature_celsius GPU temperature in Celsius.",
        "# TYPE gpu_temperature_celsius gauge",
        "# HELP gpu_power_draw_watts GPU power draw in watts.",
        "# TYPE gpu_power_draw_watts gauge",
        "# HELP gpu_power_limit_watts GPU power limit in watts.",
        "# TYPE gpu_power_limit_watts gauge",
    ]

    for sample in samples:
        labels = gpu_labels(sample)
        lines.extend(
            [
                metric_line(
                    "gpu_memory_total_bytes",
                    labels,
                    mib_to_bytes(sample.memory_total_mib),
                ),
                metric_line("gpu_memory_used_bytes", labels, mib_to_bytes(sample.memory_used_mib)),
                metric_line("gpu_memory_free_bytes", labels, mib_to_bytes(sample.memory_free_mib)),
                metric_line("gpu_utilization_ratio", labels, sample.utilization_percent / 100),
            ]
        )
        if sample.temperature_celsius is not None:
            lines.append(metric_line("gpu_temperature_celsius", labels, sample.temperature_celsius))
        if sample.power_draw_watts is not None:
            lines.append(metric_line("gpu_power_draw_watts", labels, sample.power_draw_watts))
        if sample.power_limit_watts is not None:
            lines.append(metric_line("gpu_power_limit_watts", labels, sample.power_limit_watts))

    lines.append("")
    return "\n".join(lines)


def collect_metrics() -> str:
    try:
        completed = subprocess.run(
            NVIDIA_SMI_QUERY,
            check=True,
            capture_output=True,
            text=True,
            timeout=5,
        )
        samples = parse_nvidia_smi_csv(completed.stdout)
        return render_prometheus(samples, exporter_up=True)
    except (OSError, subprocess.SubprocessError, ValueError):
        # Do not expose local command errors as metric labels or content.
        return render_prometheus([], exporter_up=False)


class MetricsHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        if self.path == "/health":
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.end_headers()
            self.wfile.write(b"ok\n")
            return

        if self.path != "/metrics":
            self.send_response(404)
            self.end_headers()
            return

        body = collect_metrics().encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; version=0.0.4; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format: str, *args: object) -> None:
        return


def main() -> int:
    parser = argparse.ArgumentParser(description="Expose local NVIDIA GPU metrics for Prometheus.")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", default=9101, type=int)
    args = parser.parse_args()

    server = ThreadingHTTPServer((args.host, args.port), MetricsHandler)
    print(f"GPU metrics exporter listening on http://{args.host}:{args.port}/metrics", flush=True)
    server.serve_forever()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
