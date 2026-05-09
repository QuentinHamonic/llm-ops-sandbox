# LLM Ops Sandbox

Demonstrateur minimal pour explorer l'exploitation d'un service LLM auto-heberge:
API FastAPI, backend mock par defaut, Ollama optionnel, metriques Prometheus et dashboard Grafana.

Le but de `v0.1.0` n'est pas de prouver une infrastructure production complete. Le but est de poser une base fiable, observable, testable et facile a expliquer.

## Demarrage local

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
python scripts/check.py
uvicorn app.main:app --reload
```

Optionnel apres initialisation Git:

```powershell
.\.venv\Scripts\Activate.ps1
pre-commit install
pre-commit run --all-files
```

API locale:

```powershell
curl http://localhost:8000/health
curl -X POST http://localhost:8000/chat -H "Content-Type: application/json" -d "{\"message\":\"Bonjour\"}"
curl http://localhost:8000/metrics
```

## Docker Compose

```powershell
docker compose up --build
```

La commande de validation `python scripts/check.py` utilise une configuration Docker temporaire pour verifier `docker compose config` sans lire les credentials/configs Docker de l'utilisateur.

Services:

- API: http://localhost:8000
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000

Identifiants Grafana locaux: `admin` / `admin`.

## Backends LLM

Par defaut, l'API utilise le backend `mock`, donc elle fonctionne sans modele local.

Variables disponibles:

```env
LLM_BACKEND=mock
OLLAMA_BASE_URL=http://ollama:11434
OLLAMA_MODEL=llama3.2:3b
```

Pour tester Ollama depuis la machine hote, utiliser par exemple:

```powershell
$env:LLM_BACKEND = "ollama"
$env:OLLAMA_BASE_URL = "http://localhost:11434"
$env:OLLAMA_MODEL = "llama3.2:3b"
uvicorn app.main:app --reload
```

## Endpoints

- `GET /health`: statut simple pour humain, Docker et futurs probes Kubernetes.
- `POST /chat`: entree `{ "message": "..." }`, sortie `{ "reply": "...", "backend": "mock|ollama" }`.
- `GET /metrics`: metriques Prometheus.

## Qualite locale

La commande principale est:

```powershell
python scripts/check.py
```

Elle lance:

- `ruff check .`
- `ruff format --check .`
- `pytest`
- `docker compose config` avec une configuration Docker temporaire.

## Ce que `v0.1.0` prouve

- Une API IA peut demarrer meme sans backend LLM reel.
- Les comportements principaux sont testes.
- Les metriques sont exposees pour Prometheus.
- Le projet est reproductible par commandes courtes.

## Documentation projet

- `docs/roadmap.md`: trajectoire, statut des taches et raisonnement.
- `docs/architecture.md`: vue logique de la stack.
- `docs/observability.md`: metriques exposees et questions operationnelles.
- `docs/versioning.md`: convention de versions et tags Git.
- `docs/contributing.md`: style de contribution, commentaires, tests et Git.
- `docs/privacy-and-ethics.md`: regles de confidentialite, donnees, logs, metriques et usage responsable.
- `SECURITY.md`: politique de securite, signalement et limites de deploiement.
- `LICENSE`: licence Apache-2.0.

Les notes de journal et de preparation entretien sont conservees localement, mais ne font pas partie de la documentation publique par defaut.

## Prochaines etapes

- Ajouter un backend vLLM en mode candidature.
- Ajouter manifests Kubernetes minimaux.
- Ajouter pipeline GitLab CI.
- Ajouter Flux CD / GitOps apres stabilisation Kubernetes.
