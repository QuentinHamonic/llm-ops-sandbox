# Validation v0.2.0

Date: 2026-05-09

Objectif: prouver que la stack locale Docker Compose tourne vraiment avec API, Prometheus et Grafana.

## Commandes

```powershell
docker compose up -d --build
python scripts/check.py
```

Checks HTTP effectues:

```powershell
GET http://localhost:8000/health
POST http://localhost:8000/chat
GET http://localhost:8000/metrics
GET http://localhost:8000/openapi.json
GET http://localhost:9090/api/v1/targets
GET http://localhost:3000/api/health
GET http://localhost:3000/api/search?query=LLM%20Ops%20Sandbox
```

## Resultats

| Verification | Resultat |
| --- | --- |
| API `/health` | `status=ok`, `llm_backend=mock` |
| API OpenAPI | version `0.2.0` |
| API `/chat` | `backend=mock` |
| API `/metrics` | contient `http_requests_total` |
| Confidentialite metriques | le prompt de test n'apparait pas dans `/metrics` |
| Prometheus target API | `up` |
| Grafana health | `database=ok`, version `11.3.0` |
| Grafana dashboard | `LLM Ops Sandbox` provisionne, uid `llm-ops-sandbox` |

## Notes

- La validation Docker doit etre lancee avec Docker Desktop actif.
- Depuis cette session Codex, les commandes Docker necessitent une execution hors sandbox pour acceder au daemon.
- L'image API installe uniquement les dependances runtime, pas les dependances dev.
- Le dashboard est provisionne depuis `monitoring/grafana/dashboards/llm-ops-sandbox.json`.
