# Runbook - latence API

## Objectif

Diagnostiquer une API lente sans supposer immediatement que le backend LLM est responsable.

## Symptomes

- `/chat` repond lentement.
- Grafana montre une hausse de latence.
- Prometheus expose une hausse de `http_request_duration_seconds`.

## Commandes rapides

Verifier que l'API repond:

```powershell
curl http://localhost:8000/health
```

Tester un appel chat simple:

```powershell
curl -X POST http://localhost:8000/chat -H "Content-Type: application/json" -d "{\"message\":\"test latence\"}"
```

Consulter les metriques:

```powershell
curl http://localhost:8000/metrics
```

Voir les conteneurs:

```powershell
docker compose ps
```

Lire les logs API:

```powershell
docker compose logs api
```

## Questions de diagnostic

1. Est-ce que `/health` est lent aussi?
2. Est-ce que seul `/chat` est lent?
3. Est-ce que le backend configure est `mock` ou `ollama`?
4. Est-ce que Prometheus scrape encore l'API?
5. Est-ce que les logs API montrent des erreurs backend?

## Interpretation

Si `/health` est rapide mais `/chat` est lent:

- le probleme est probablement dans le chemin backend LLM;
- verifier `LLM_BACKEND`;
- si `ollama` est active, verifier Ollama separement.

Si `/health` et `/chat` sont lents:

- verifier la charge locale;
- verifier les logs du conteneur API;
- redemarrer la stack locale si necessaire.

## Retour a l'etat sain

Redemarrer la stack locale:

```powershell
docker compose down
docker compose up -d --build
```

Puis verifier:

```powershell
curl http://localhost:8000/health
curl http://localhost:9090/-/ready
```

## Limites

En `v0.3.0`, il n'y a pas encore de tracing distribue ni de profilage applicatif. Le diagnostic repose sur les endpoints, les logs Docker, Prometheus et Grafana.
