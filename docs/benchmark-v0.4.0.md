# Benchmark manuel v0.4.0

## Objectif

Comparer rapidement le comportement du backend `mock` et du backend `ollama`.

Ce n'est pas un benchmark scientifique. C'est une preuve de fonctionnement et un ordre de grandeur local.

## Conditions

Machine locale Windows.

Modele Ollama:

```txt
mistral:latest
```

Prompt synthetique:

```txt
Reply with exactly: OK
```

## Commandes

Backend mock:

```powershell
$env:LLM_BACKEND = "mock"
uvicorn app.main:app --reload
curl -X POST http://localhost:8000/chat -H "Content-Type: application/json" -d "{\"message\":\"Reply with exactly: OK\"}"
```

Backend Ollama:

```powershell
$env:LLM_BACKEND = "ollama"
$env:OLLAMA_BASE_URL = "http://localhost:11434"
$env:OLLAMA_MODEL = "mistral:latest"
uvicorn app.main:app --reload
curl -X POST http://localhost:8000/chat -H "Content-Type: application/json" -d "{\"message\":\"Reply with exactly: OK\"}"
```

## Resultats observes

| Backend | Resultat attendu | Observation |
| --- | --- | --- |
| `mock` | Reponse immediate et deterministe | Valide par tests automatises |
| `ollama` | Reponse reelle du modele local | Valide avec `mistral:latest` |

## Interpretation

Le backend `mock` sert a garder un socle toujours testable.

Le backend `ollama` prouve que l'interface backend peut brancher un vrai modele local sans changer le contrat HTTP de `/chat`.

## Limites

- Pas de mesure p95 automatisee.
- Pas de charge concurrente.
- Pas de comparaison GPU/CPU.
- Pas de stockage des prompts ou reponses dans les metriques.
