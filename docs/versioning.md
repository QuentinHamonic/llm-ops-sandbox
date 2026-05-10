# Versioning

Le projet utilise une seule convention de progression: les versions SemVer taguees dans Git.

Format:

```txt
vMAJOR.MINOR.PATCH
```

Exemple:

```txt
v0.1.0
```

## Regles

- Une version n'est annoncee que si sa definition of done est terminee.
- Une version taguee doit correspondre a un commit propre.
- `pyproject.toml` doit porter la meme version que le tag Git prevu.
- Avant un tag, lancer au minimum `pytest` et `ruff check .`.
- Les versions `0.x` indiquent un projet encore en construction.
- `v1.0.0` sera reservee a un projet suffisamment complet pour etre montre en candidature.

## Versions prevues

| Version | Objectif | Definition of done |
| --- | --- | --- |
| `v0.1.0` | Socle API local observable | FastAPI, mock backend, Ollama optionnel, `/health`, `/chat`, `/metrics`, tests, ruff, Docker Compose configure |
| `v0.2.0` | Observabilite locale validee | `docker compose up --build`, Prometheus target `UP`, dashboard Grafana verifie, image API runtime-only |
| `v0.3.0` | Documentation operationnelle | commandes de preuve, runbooks latence/backend down, test erreur `/chat`, decision backend status |
| `v0.3.1` | Documentation API generee | OpenAPI enrichi, export `docs/generated/openapi.json`, resume `docs/generated/api.md`, check automatique |
| `v0.4.0` | LLM local reel | Ollama teste avec `mistral:latest`, `/backend/status`, modele documente, integration test optionnel, mini benchmark |
| `v0.5.0` | Kubernetes minimal | manifests API, Service, ConfigMap, probes, resources, validation client-side, commandes kubectl |
| `v0.6.0` | CI GitLab | lint, tests, docs API, Docker Compose, Kubernetes statique, build Docker, secrets et rollback documentes |
| `v0.7.0` | GitOps | structure Flux locale, Kustomization, exemple HelmRelease, validation statique et limites documentees |
| `v0.8.0` | vLLM mode candidature | configuration vLLM, limites GPU documentees, chemin de demo clair |
| `v1.0.0` | Projet presentable en candidature | stack documentee, demos reproductibles, runbooks, tests, CI, Kubernetes/GitOps/vLLM coherents |

## Commits et tags

Les commits racontent le travail quotidien. Les tags racontent les versions stables.

Exemple de sequence:

```powershell
git status --short
git add README.md docs/roadmap.md docs/versioning.md
git commit -m "docs: define roadmap and versioning"
git tag v0.1.0
```

Avant d'executer ces commandes, l'agent doit annoncer la commande exacte et expliquer ce qu'elle inclut.
