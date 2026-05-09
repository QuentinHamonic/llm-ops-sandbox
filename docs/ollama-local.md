# Ollama local

## Objectif

`v0.4.0` valide que l'API peut utiliser un vrai modele local via Ollama, sans casser le backend `mock` par defaut.

Le mode `mock` reste le comportement par defaut pour les tests, les demos rapides et la reproductibilite.

## Mode valide

Validation locale effectuee avec:

```env
LLM_BACKEND=ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=mistral:latest
```

Modele disponible localement:

```txt
mistral:latest
```

Un modele plus lourd est aussi present localement:

```txt
qwen3:32b
```

Il n'est pas utilise comme modele de validation par defaut, car il est plus couteux pour une demo courte.

## Commandes

Verifier Ollama directement:

```powershell
ollama list
```

Tester Ollama directement:

```powershell
$body = @{ model = "mistral:latest"; prompt = "Reply with exactly: OK"; stream = $false } | ConvertTo-Json
Invoke-RestMethod -Method Post http://localhost:11434/api/generate -ContentType "application/json" -Body $body
```

Lancer l'API avec Ollama:

```powershell
$env:LLM_BACKEND = "ollama"
$env:OLLAMA_BASE_URL = "http://localhost:11434"
$env:OLLAMA_MODEL = "mistral:latest"
uvicorn app.main:app --reload
```

Verifier le statut backend:

```powershell
curl http://localhost:8000/backend/status
```

Tester `/chat`:

```powershell
curl -X POST http://localhost:8000/chat -H "Content-Type: application/json" -d "{\"message\":\"Reply with exactly: OK\"}"
```

## Test d'integration

Le test reel Ollama est separe des tests rapides.

```powershell
$env:OLLAMA_INTEGRATION = "1"
$env:OLLAMA_BASE_URL = "http://localhost:11434"
$env:OLLAMA_MODEL = "mistral:latest"
pytest -m integration
```

## Pourquoi pas un service Ollama dans Docker Compose maintenant?

`v0.4.0` valide Ollama depuis l'hote parce que c'est le chemin le plus simple et le plus explicable sur la machine locale.

Un service Ollama dans Docker Compose demanderait aussi de gerer:

- le volume des modeles;
- le pull du modele;
- le temps de demarrage;
- les differences CPU/GPU selon les machines.

Ce sera reconsidere plus tard si le projet a besoin d'une demo Compose totalement autonome.

## Limites

- Pas encore de vLLM.
- Pas encore de GPU monitoring.
- Pas encore de benchmark automatise.
- Le prompt de test reste synthetique et non sensible.
