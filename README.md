# LLM Ops Sandbox

Demonstrateur minimal pour explorer l'exploitation d'un service LLM auto-heberge:
API FastAPI, backend mock par defaut, Ollama optionnel, metriques Prometheus et dashboard Grafana.

Le but de `v0.9.0` n'est pas de prouver une infrastructure production complete. Le but est de poser une base fiable, observable, testable, validable en CI, explicable en GitOps, et capable d'appeler un serveur vLLM reel sur GPU local.

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
curl http://localhost:8000/backend/status
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
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=mistral:latest
VLLM_BASE_URL=http://localhost:8001/v1
VLLM_MODEL=TinyLlama/TinyLlama-1.1B-Chat-v1.0
```

Dans Docker Compose, le backend reste `mock` par defaut. Si l'API conteneurisee doit joindre Ollama sur l'hote Docker Desktop, utiliser `OLLAMA_BASE_URL=http://host.docker.internal:11434`.

Pour tester Ollama depuis la machine hote, utiliser par exemple:

```powershell
$env:LLM_BACKEND = "ollama"
$env:OLLAMA_BASE_URL = "http://localhost:11434"
$env:OLLAMA_MODEL = "mistral:latest"
uvicorn app.main:app --reload
```

Verifier le backend configure:

```powershell
curl http://localhost:8000/backend/status
```

Lancer le test d'integration Ollama reel:

```powershell
$env:OLLAMA_INTEGRATION = "1"
$env:OLLAMA_BASE_URL = "http://localhost:11434"
$env:OLLAMA_MODEL = "mistral:latest"
pytest -m integration
```

Ce test est separe du `pytest` standard pour garder la validation quotidienne rapide et independante d'Ollama.

Pour preparer un backend vLLM OpenAI-compatible:

```powershell
$env:LLM_BACKEND = "vllm"
$env:VLLM_BASE_URL = "http://localhost:8001/v1"
$env:VLLM_MODEL = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
uvicorn app.main:app --reload
```

Ce mode suppose qu'un serveur vLLM compatible OpenAI tourne deja. Le projet ne lance pas vLLM automatiquement.

## Endpoints

- `GET /health`: statut simple pour humain, Docker et futurs probes Kubernetes.
- `GET /backend/status`: statut non-generatif du backend LLM configure.
- `POST /chat`: entree `{ "message": "..." }`, sortie `{ "reply": "...", "backend": "mock|ollama|vllm" }`.
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
- `python scripts/export_api_docs.py --check`
- `python scripts/check_gitlab_ci.py`
- `python scripts/check_gitops_manifests.py`
- `python scripts/check_vllm_manifests.py`
- `python scripts/check_k8s_overlays.py`
- `docker compose config` avec une configuration Docker temporaire.
- `python scripts/check_k8s_manifests.py`

## Kubernetes local

`v0.5.0` ajoute des manifests Kubernetes minimaux dans `k8s/base/`.

Valider les manifests dans la commande de check:

```powershell
python scripts/check_k8s_manifests.py
```

Rendre les manifests avec Kustomize, sans cluster actif:

```powershell
kubectl kustomize k8s/base
```

Construire l'image locale pour un cluster Docker Desktop Kubernetes:

```powershell
docker build -t llm-ops-sandbox-api:0.9.0 .
```

Appliquer les manifests:

```powershell
kubectl apply -k k8s/base
kubectl port-forward svc/llm-ops-sandbox-api 8000:8000
```

Choisir un backend Kubernetes sans modifier `k8s/base/configmap.yaml`:

```powershell
kubectl apply -k k8s/overlays/mock
kubectl apply -k k8s/overlays/ollama
kubectl apply -k k8s/overlays/vllm
```

Les overlays changent aussi une annotation du Deployment pour declencher un nouveau rollout du Pod.

Documentation detaillee: `docs/kubernetes-local.md`.

## GitOps local

`v0.7.0` ajoute une structure GitOps Flux dans `gitops/local/`.

Elle contient:

- une source Git Flux;
- une Kustomization Flux vers `./k8s/base`;
- un exemple HelmRepository;
- un exemple HelmRelease monitoring.

Validation:

```powershell
python scripts/check_gitops_manifests.py
```

Cette couche est pedagogique et statique: elle ne deploie pas encore Flux dans un cluster.

Documentation detaillee: `docs/gitops.md`.

## vLLM

`v0.9.0` valide le passage du mode vLLM preparatoire a un serveur vLLM reel sur GPU local:

- backend applicatif `LLM_BACKEND=vllm`;
- appels OpenAI-compatible vers `/chat/completions` et `/models`;
- manifests exemples dans `k8s/vllm/`;
- validation statique avec `python scripts/check_vllm_manifests.py`;
- notes GPU/DCGM dans `docs/vllm.md`.
- preuve runtime Docker avec `vllm/vllm-openai`.

Le projet ne lance pas vLLM automatiquement quand l'API demarre. Il faut demarrer le serveur vLLM separement, puis configurer l'API avec `LLM_BACKEND=vllm`.

Exemple local GPU Docker:

```powershell
docker run --rm -d --name llm-ops-vllm-runtime --gpus all -p 8001:8000 --ipc=host vllm/vllm-openai:latest --model TinyLlama/TinyLlama-1.1B-Chat-v1.0 --gpu-memory-utilization 0.60
$env:LLM_BACKEND = "vllm"
$env:VLLM_BASE_URL = "http://localhost:8001/v1"
$env:VLLM_MODEL = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
uvicorn app.main:app --reload
```

Documentation detaillee: `docs/vllm-runtime.md`.

## GitLab CI

`v0.6.0` ajoute une pipeline GitLab CI dans `.gitlab-ci.yml`.

La pipeline verifie:

- Ruff lint et format.
- Pytest.
- Documentation API generee.
- Configuration Docker Compose.
- Manifests Kubernetes par validation statique.
- Overlays Kubernetes backend par validation statique.
- Manifests GitOps Flux par validation statique.
- Manifests vLLM par validation statique.
- Build Docker de l'API.

La CI ne deploie rien automatiquement et n'utilise aucun secret.

Documentation detaillee: `docs/gitlab-ci.md`.

## Documentation API generee

FastAPI expose deja la documentation interactive quand l'API tourne:

- Swagger UI: http://localhost:8000/docs
- OpenAPI JSON: http://localhost:8000/openapi.json

Pour aider un lecteur externe a comprendre l'API sans lancer le service, le contrat API est aussi exporte dans le repo:

- `docs/generated/openapi.json`: contrat OpenAPI complet.
- `docs/generated/api.md`: resume Markdown lisible des endpoints.

Regenerer la documentation API:

```powershell
python scripts/export_api_docs.py
```

Verifier que la documentation generee est a jour:

```powershell
python scripts/export_api_docs.py --check
```

## Commandes de preuve

Ces commandes permettent de prouver rapidement que le socle local fonctionne.

Verifier l'API:

```powershell
curl http://localhost:8000/health
```

Resultat attendu: `status` vaut `ok` et `llm_backend` vaut `mock` par defaut.

Tester le chat mock:

```powershell
curl -X POST http://localhost:8000/chat -H "Content-Type: application/json" -d "{\"message\":\"Bonjour\"}"
```

Resultat attendu: la reponse contient `backend: "mock"` et un champ `reply`.

Verifier la validation d'entree:

```powershell
curl -X POST http://localhost:8000/chat -H "Content-Type: application/json" -d "{\"message\":\"\"}"
```

Resultat attendu: FastAPI retourne une erreur `422`.

Verifier les metriques:

```powershell
curl http://localhost:8000/metrics
```

Resultat attendu: la sortie contient au moins `http_requests_total` et `http_request_duration_seconds`.

Verifier la stack d'observabilite:

```powershell
docker compose up -d --build
```

Puis ouvrir:

- Prometheus targets: http://localhost:9090/targets
- Grafana: http://localhost:3000 avec `admin` / `admin`

Resultat attendu: Prometheus voit la target API en `UP` et Grafana charge le dashboard `LLM Ops Sandbox`.

## Ce que `v0.9.0` prouve

- Une API IA peut demarrer meme sans backend LLM reel.
- Les comportements principaux sont testes.
- Les metriques sont exposees pour Prometheus.
- Le projet est reproductible par commandes courtes.
- Docker Compose lance API, Prometheus et Grafana.
- Prometheus scrape l'API et Grafana charge le dashboard provisionne.
- Les erreurs importantes sont documentees par des runbooks.
- `/chat` couvre les erreurs de validation et d'indisponibilite backend.
- La documentation API est generee depuis le contrat OpenAPI FastAPI.
- Ollama peut etre utilise comme backend local reel sans casser le backend `mock`.
- Le statut backend peut etre verifie sans envoyer de prompt au modele.
- Les manifests Kubernetes minimaux de l'API sont presents et validables.
- La qualite locale est traduite en pipeline GitLab CI sobre.
- Les strategies de secrets et rollback sont documentees avant tout deploiement automatique.
- Le projet montre la logique GitOps Flux sans pretendre a une production.
- Les manifests GitOps sont validates statiquement et integres a la CI.
- Le projet prepare un backend vLLM OpenAI-compatible sans casser le mock.
- Les limites GPU, image vLLM et DCGM sont documentees honnetement.
- Kubernetes peut changer de backend avec des overlays `mock`, `ollama` et `vllm`.
- Docker voit le GPU NVIDIA local.
- Un serveur vLLM OpenAI-compatible repond sur la machine locale.
- L'API FastAPI peut router `/chat` vers `backend=vllm`.
- La contention GPU avec Ollama est identifiee comme limite operationnelle locale.

## Documentation projet

- `docs/roadmap.md`: trajectoire, statut des taches et raisonnement.
- `docs/architecture.md`: vue logique de la stack.
- `docs/generated/api.md`: documentation API generee en Markdown.
- `docs/generated/openapi.json`: contrat OpenAPI exporte.
- `docs/gitlab-ci.md`: pipeline CI, strategie de secrets, rollback et limites.
- `docs/gitops.md`: structure Flux locale, secrets, rollback et limites.
- `docs/vllm.md`: mode vLLM, manifests GPU, DCGM et limites.
- `docs/vllm-runtime.md`: execution vLLM reelle sur GPU local, commandes et limites.
- `docs/benchmark-v0.9.0.md`: mesures indicatives mock/Ollama/vLLM.
- `docs/kubernetes-local.md`: manifests Kubernetes locaux, commandes et limites.
- `docs/ollama-local.md`: mode Ollama local, modele valide et limites.
- `docs/benchmark-v0.4.0.md`: comparaison manuelle mock vs Ollama.
- `docs/observability.md`: metriques exposees et questions operationnelles.
- `docs/backend-status.md`: decision sur le statut backend en `v0.3.0`.
- `docs/runbook-latency.md`: diagnostic d'une latence API.
- `docs/runbook-llm-backend-down.md`: diagnostic d'un backend LLM indisponible.
- `docs/validation-v0.3.0.md`: preuves de validation de `v0.3.0`.
- `docs/validation-v0.3.1.md`: preuves de validation de la documentation API generee.
- `docs/validation-v0.4.0.md`: preuves de validation du mode Ollama local.
- `docs/validation-v0.5.0.md`: preuves de validation Kubernetes minimal.
- `docs/validation-v0.6.0.md`: preuves de validation CI/CD.
- `docs/validation-v0.7.0.md`: preuves de validation GitOps Flux.
- `docs/validation-v0.8.0.md`: preuves de validation vLLM mode candidature.
- `docs/validation-v0.8.1.md`: preuves de validation des overlays Kubernetes backend.
- `docs/validation-v0.9.0.md`: preuves de validation vLLM runtime GPU local.
- `docs/validation-v0.2.0.md`: preuves de validation Docker Compose, Prometheus et Grafana.
- `docs/versioning.md`: convention de versions et tags Git.
- `docs/contributing.md`: style de contribution, commentaires, tests et Git.
- `docs/privacy-and-ethics.md`: regles de confidentialite, donnees, logs, metriques et usage responsable.
- `SECURITY.md`: politique de securite, signalement et limites de deploiement.
- `LICENSE`: licence Apache-2.0.

Les notes de journal et de preparation entretien sont conservees localement, mais ne font pas partie de la documentation publique par defaut.

## Prochaines etapes

- Ajouter monitoring GPU avec DCGM Exporter ou alternative locale.
- Executer une CI distante sur GitHub ou GitLab.
- Installer Flux CD reellement dans un cluster local.
- Ajouter scenarios de robustesse et chaos engineering local.
