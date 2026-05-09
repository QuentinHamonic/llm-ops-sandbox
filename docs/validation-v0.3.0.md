# Validation v0.3.0

Date: 2026-05-09

Objectif: prouver que `v0.3.0` ajoute des commandes de preuve, des runbooks et des erreurs testees sans fragiliser le socle local.

## Commandes

```powershell
.\.venv\Scripts\python.exe scripts\check.py
docker compose up -d --build
```

Checks HTTP effectues:

```powershell
GET http://localhost:8000/health
POST http://localhost:8000/chat
POST http://localhost:8000/chat avec message vide
GET http://localhost:8000/metrics
GET http://localhost:8000/openapi.json
GET http://localhost:9090/api/v1/targets
GET http://localhost:3000/api/health
GET http://localhost:3000/api/search?query=LLM%20Ops%20Sandbox
```

## Resultats

| Verification | Resultat |
| --- | --- |
| `python scripts/check.py` | Ruff, format, pytest et Compose config OK |
| Tests pytest | `10 passed` |
| Image API | package `llm-ops-sandbox==0.3.0` installe |
| API `/health` | `status=ok`, `llm_backend=mock` |
| API OpenAPI | version `0.3.0` |
| API `/chat` | `backend=mock` |
| API `/chat` message vide | `422` |
| API `/metrics` | contient `http_requests_total` |
| Confidentialite metriques | le prompt de test n'apparait pas dans `/metrics` |
| Prometheus target API | `up` |
| Grafana health | `database=ok` |
| Grafana dashboard | `LLM Ops Sandbox` provisionne |

## Notes

- `v0.3.0` ne change pas l'architecture principale.
- La version renforce la methode: preuves, runbooks, decision documentee et tests d'erreur.
- Le test de backend down est automatise sans appeler Ollama, pour rester rapide et deterministe.
