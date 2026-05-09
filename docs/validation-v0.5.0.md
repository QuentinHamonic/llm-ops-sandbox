# Validation v0.5.0

Date: 2026-05-09

Objectif: prouver que le projet contient une base Kubernetes minimale, validable localement, sans pretendre a une production.

## Commandes

Validation standard:

```powershell
.\.venv\Scripts\python.exe scripts\check.py
```

Validation Kubernetes seule:

```powershell
python scripts/check_k8s_manifests.py
```

Rendu Kustomize:

```powershell
kubectl kustomize k8s/base
```

Version kubectl:

```powershell
kubectl version --client=true --output=yaml
```

## Resultats attendus

| Verification | Resultat |
| --- | --- |
| `python scripts/check.py` | Ruff, format, pytest, API docs check, Compose config et Kubernetes static checks OK |
| `kubectl kustomize k8s/base` | Rendu YAML OK hors sandbox |
| `kubectl` client | Disponible via Docker Desktop |
| `k8s/base/configmap.yaml` | Variables `LLM_BACKEND`, `OLLAMA_BASE_URL`, `OLLAMA_MODEL` |
| `k8s/base/deployment.yaml` | Deployment API avec probes et resources |
| `k8s/base/service.yaml` | Service ClusterIP sur le port `8000` |
| Prometheus | Annotations de scrape sur Pod et Service |

## Notes

- `kind`, `k3d` et `minikube` ne sont pas installes localement.
- Le choix documente est Kubernetes local via Docker Desktop.
- `kubectl apply --dry-run=client` demande un API server avec cette version de kubectl; le rendu `kubectl kustomize` est donc utilise comme validation sans cluster actif.
- L'image attendue par les manifests est `llm-ops-sandbox-api:0.5.0`.
- Avant un vrai apply local, construire l'image avec `docker build -t llm-ops-sandbox-api:0.5.0 .`.
