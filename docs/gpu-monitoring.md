# Monitoring GPU local

`v0.10.0` ajoute une premiere couche de monitoring GPU.

Objectif: voir si le GPU local est disponible, utilise, sature en memoire, chaud ou limite en puissance pendant les tests Ollama/vLLM.

## Choix technique

Le projet utilise un exporter local base sur `nvidia-smi`:

```txt
scripts/gpu_metrics_exporter.py
```

Ce choix est volontairement simple:

- pas de dependance Python supplementaire;
- compatible avec la machine Windows locale;
- testable avec une sortie `nvidia-smi` synthetique;
- comprehensible pour un lecteur junior.

DCGM Exporter est une option plus industrielle pour Kubernetes GPU, mais elle est gardee pour une version future afin d'eviter de melanger runtime local Windows, Docker Desktop et monitoring cluster avance.

## Demarrage

Lancer l'exporter depuis l'hote:

```powershell
python scripts/gpu_metrics_exporter.py
```

Par defaut, il ecoute sur:

```txt
http://localhost:9101/metrics
```

Verifier:

```powershell
Invoke-RestMethod http://localhost:9101/health
Invoke-RestMethod http://localhost:9101/metrics
```

## Prometheus

Prometheus tourne dans Docker Compose. Depuis un conteneur Docker Desktop, `localhost` designe le conteneur lui-meme, pas Windows.

Pour joindre l'exporter lance sur l'hote Windows, Prometheus utilise:

```txt
host.docker.internal:9101
```

La configuration est dans:

```txt
monitoring/prometheus/prometheus.yml
```

Job ajoute:

```yaml
job_name: llm-ops-sandbox-gpu
targets:
  - host.docker.internal:9101
```

## Grafana

Dashboard ajoute:

```txt
monitoring/grafana/dashboards/llm-ops-gpu.json
```

Il affiche:

- disponibilite de l'exporter;
- utilisation GPU;
- memoire GPU utilisee et totale;
- temperature GPU;
- puissance consommee et limite.

## Metriques

| Metrique | Question operationnelle |
| --- | --- |
| `gpu_exporter_up` | Est-ce que l'exporter lit correctement `nvidia-smi` ? |
| `gpu_utilization_ratio` | Le GPU travaille-t-il pendant une generation ? |
| `gpu_memory_used_bytes` | Est-ce que la memoire GPU se remplit ? |
| `gpu_memory_total_bytes` | Quelle capacite GPU est visible ? |
| `gpu_memory_free_bytes` | Peut-on charger un autre modele ? |
| `gpu_temperature_celsius` | Le GPU chauffe-t-il trop ? |
| `gpu_power_draw_watts` | Quelle puissance est consommee ? |
| `gpu_power_limit_watts` | Quelle est la limite de puissance observee ? |

## Confidentialite

Ces metriques ne contiennent pas de prompt, reponse, IP, email, token ou identifiant utilisateur.

Labels utilises:

- `gpu`: index local du GPU;
- `name`: nom materiel de la carte.

Ces labels sont bornes et bas-cardinalite.

## Limites

- L'exporter depend de `nvidia-smi` sur l'hote.
- Le dashboard est local et pedagogique.
- Ce n'est pas encore DCGM Exporter.
- Ce n'est pas encore un monitoring GPU Kubernetes.
- Les metriques vLLM natives, tokens/seconde et latence de generation separee restent a ajouter.

## Validation

Validation rapide:

```powershell
python scripts/check_monitoring_config.py
pytest tests/test_gpu_metrics_exporter.py
```

Validation runtime:

```powershell
python scripts/gpu_metrics_exporter.py
docker compose up -d --build
```

Puis ouvrir:

- Prometheus targets: http://localhost:9090/targets
- Grafana GPU: http://localhost:3000
