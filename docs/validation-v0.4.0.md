# Validation v0.4.0

Date: 2026-05-09

Objectif: prouver que l'API peut utiliser Ollama comme backend local reel, tout en gardant le backend `mock` par defaut.

## Commandes

Validation standard:

```powershell
.\.venv\Scripts\python.exe scripts\check.py
```

Validation Ollama directe:

```powershell
$body = @{ model = "mistral:latest"; prompt = "Reply with exactly: OK"; stream = $false } | ConvertTo-Json
Invoke-RestMethod -Method Post http://localhost:11434/api/generate -ContentType "application/json" -Body $body
```

Test d'integration:

```powershell
$env:OLLAMA_INTEGRATION = "1"
$env:OLLAMA_BASE_URL = "http://localhost:11434"
$env:OLLAMA_MODEL = "mistral:latest"
.\.venv\Scripts\python.exe -m pytest -m integration -q
```

Validation Docker avec Ollama hote:

```powershell
$env:LLM_BACKEND = "ollama"
$env:OLLAMA_BASE_URL = "http://host.docker.internal:11434"
$env:OLLAMA_MODEL = "mistral:latest"
docker compose up -d --build api
```

Retour au mode stable:

```powershell
Remove-Item Env:\LLM_BACKEND -ErrorAction SilentlyContinue
Remove-Item Env:\OLLAMA_BASE_URL -ErrorAction SilentlyContinue
Remove-Item Env:\OLLAMA_MODEL -ErrorAction SilentlyContinue
docker compose up -d api
```

## Resultats

| Verification | Resultat |
| --- | --- |
| `python scripts/check.py` | Ruff, format, pytest, API docs check et Compose config OK |
| Tests rapides | `14 passed`, `1 skipped` |
| Test integration Ollama | `1 passed`, `14 deselected` |
| Ollama direct | `mistral:latest` repond `OK` |
| Image API | package `llm-ops-sandbox==0.4.0` installe |
| API Docker mode mock | `/health` indique `llm_backend=mock` |
| `/backend/status` mode mock | `available=true`, `model=mock` |
| API Docker mode Ollama | `/backend/status` indique `backend=ollama`, `available=true`, `model=mistral:latest` |
| `/chat` mode Ollama | repond avec `backend=ollama` |
| Retour etat stable | Docker Compose remis en `mock` |

## Notes

- `GET /backend/status` ne transmet pas de prompt au modele.
- Le prompt de validation est synthetique.
- Le backend `mock` reste le mode par defaut pour la reproductibilite.
- Le mode Ollama est maintenant valide comme backend local optionnel.
