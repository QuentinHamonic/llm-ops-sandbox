# Runbook - backend LLM indisponible

## Objectif

Diagnostiquer un echec du backend LLM, en particulier quand `LLM_BACKEND=ollama`.

## Symptomes

- `POST /chat` retourne `502`.
- La reponse contient un detail du type `Ollama request failed`.
- La metrique `llm_requests_total{backend="ollama",status="error"}` augmente.

## Commandes rapides

Verifier le backend configure:

```powershell
curl http://localhost:8000/health
```

Tester `/chat`:

```powershell
curl -X POST http://localhost:8000/chat -H "Content-Type: application/json" -d "{\"message\":\"test backend\"}"
```

Lire les metriques:

```powershell
curl http://localhost:8000/metrics
```

Lire les logs API:

```powershell
docker compose logs api
```

## Diagnostic

Si `llm_backend` vaut `mock`:

- le backend mock ne depend pas d'un service externe;
- une erreur `502` serait inattendue et doit etre traitee comme bug applicatif.

Si `llm_backend` vaut `ollama`:

- verifier qu'Ollama tourne;
- verifier `OLLAMA_BASE_URL`;
- verifier `OLLAMA_MODEL`;
- verifier que le modele est disponible localement.

## Retour a l'etat sain

Pour revenir a un mode demo stable:

```powershell
$env:LLM_BACKEND = "mock"
uvicorn app.main:app --reload
```

Avec Docker Compose, le backend par defaut est deja `mock` si aucune variable `LLM_BACKEND` n'est definie:

```powershell
docker compose down
docker compose up -d --build
```

## Limites

En `v0.3.0`, Ollama est un backend optionnel documente mais pas encore valide comme mode principal. La validation complete d'Ollama est prevue en `v0.4.0`.
