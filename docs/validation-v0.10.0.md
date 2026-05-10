# Validation v0.10.0

Objectif: prouver une premiere observabilite GPU locale.

## Branche

```txt
ops/gpu-monitoring
```

## Exporter GPU

Commande:

```powershell
python scripts/gpu_metrics_exporter.py
```

Endpoints:

```txt
http://localhost:9101/health
http://localhost:9101/metrics
```

Preuve attendue:

- `/health` retourne `ok`;
- `/metrics` contient `gpu_exporter_up`;
- si `nvidia-smi` est disponible, les metriques GPU sont exposees.

Resultat observe:

```txt
gpu_exporter_up 1
gpu_memory_total_bytes{gpu="0",name="NVIDIA GeForce RTX 5090"} 34190917632
```

## Prometheus

Configuration:

```txt
monitoring/prometheus/prometheus.yml
```

Job ajoute:

```txt
llm-ops-sandbox-gpu -> host.docker.internal:9101
```

Preuve attendue:

- Prometheus peut scraper l'exporter GPU local quand il tourne sur l'hote.

Resultat observe via l'API Prometheus:

```txt
health: up
scrapeUrl: http://host.docker.internal:9101/metrics
lastError: ""
```

## Grafana

Dashboard ajoute:

```txt
monitoring/grafana/dashboards/llm-ops-gpu.json
```

Panels:

- GPU utilization;
- GPU memory;
- GPU temperature;
- GPU power;
- GPU exporter up.

## Validation automatique

Commandes:

```powershell
pytest tests/test_gpu_metrics_exporter.py
python scripts/check_monitoring_config.py
python scripts/check.py
```

Preuve attendue:

- parsing `nvidia-smi` teste sans GPU;
- rendu Prometheus teste;
- configuration Prometheus et dashboard GPU verifies statiquement;
- validation projet complete.

Resultat observe:

```txt
19 passed, 1 skipped
All validation steps passed.
```

## Image API

Commande:

```powershell
docker build -t llm-ops-sandbox-api:0.10.0 .
```

Preuve attendue:

- l'image `llm-ops-sandbox-api:0.10.0` est construite;
- le package installe dans l'image est `llm-ops-sandbox==0.10.0`.

## Limites connues

- Ce n'est pas encore DCGM Exporter.
- Ce n'est pas encore un monitoring Kubernetes GPU.
- Les metriques GPU dependent de `nvidia-smi`.
- Le dashboard ne prouve pas encore une charge vLLM en continu.
- Les tokens/seconde et metriques natives vLLM restent hors scope.
