# GitHub Actions

`v0.11.0` ajoute une CI GitHub Actions pour rendre le projet validable sur une forge publique.

GitHub devient la forge publique principale du projet. GitLab reste conserve comme competence cible grace au fichier `.gitlab-ci.yml` et a une strategie de miroir documentee.

## Workflow

Le workflow est defini dans:

```txt
.github/workflows/ci.yml
```

Il se lance sur:

- push vers `main`;
- tags `v*`;
- pull requests vers `main`.

## Jobs

| Job | Role |
| --- | --- |
| `quality` | Lint, format, tests, docs API, validations statiques |
| `docker` | Validation Docker Compose et build image |

## Job `quality`

Ce job installe le projet avec:

```bash
pip install -e ".[dev]"
```

Puis lance:

```bash
ruff check .
ruff format --check .
pytest
python scripts/export_api_docs.py --check
python scripts/check_github_actions.py
python scripts/check_gitlab_ci.py
python scripts/check_gitops_manifests.py
python scripts/check_monitoring_config.py
python scripts/check_vllm_manifests.py
python scripts/check_k8s_overlays.py
python scripts/check_k8s_manifests.py
```

Le but est de prouver que le projet reste propre sans dependance a Ollama, vLLM, GPU ou secrets.

## Job `docker`

Ce job lance:

```bash
docker version
docker compose config
docker build -t llm-ops-sandbox-api:${{ github.sha }} .
```

Il ne publie pas encore d'image dans un registry. Cela evite d'introduire des secrets avant d'avoir une raison claire.

## Permissions

Le workflow utilise:

```yaml
permissions:
  contents: read
```

La CI n'a donc pas de droit d'ecriture par defaut.

## Validation locale

La structure du workflow est verifiee par:

```powershell
python scripts/check_github_actions.py
```

Cette verification est aussi lancee dans:

```powershell
python scripts/check.py
```

## Limites

- La CI GitHub ne teste pas Ollama reel.
- La CI GitHub ne teste pas vLLM reel.
- La CI GitHub ne teste pas le GPU.
- La CI GitHub ne deploie rien.
- La CI GitHub ne publie pas encore d'image.

Ces choix sont volontaires: le but est d'abord une CI publique stable, rapide et sans secret.
