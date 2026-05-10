# Validation v0.11.0

Objectif: ajouter une CI GitHub Actions et documenter une strategie de miroir GitLab CI.

## Branche

```txt
ci/github-actions-mirror
```

## GitHub Actions

Workflow ajoute:

```txt
.github/workflows/ci.yml
```

Jobs:

- `quality`;
- `docker`.

Validation locale:

```powershell
python scripts/check_github_actions.py
```

Preuve attendue:

- le workflow se lance sur push, tag et pull request;
- les permissions restent limitees a `contents: read`;
- les checks Python, docs, GitOps, monitoring, vLLM et Kubernetes sont presents;
- Docker Compose et Docker build sont verifies dans un job separe.

## GitLab CI conservee

Fichier conserve:

```txt
.gitlab-ci.yml
```

Ajout:

```txt
github-actions-static-check
```

Objectif:

- GitLab CI verifie aussi la structure GitHub Actions;
- les deux CI restent coherentes.

## Strategie miroir

Documentation ajoutee:

```txt
docs/ci-mirror.md
```

Decision:

```txt
GitHub = source principale
GitLab = miroir aval pour executer GitLab CI
```

## Validation automatique

Commandes:

```powershell
python scripts/check_github_actions.py
python scripts/check_gitlab_ci.py
python scripts/check.py
```

Preuve attendue:

- workflow GitHub valide localement;
- pipeline GitLab valide localement;
- validation projet complete.

Resultat observe:

```txt
GitHub Actions static checks passed.
GitLab CI static checks passed.
19 passed, 1 skipped
All validation steps passed.
```

## Image API

Commande:

```powershell
docker build -t llm-ops-sandbox-api:0.11.0 .
```

Resultat observe:

- l'image `llm-ops-sandbox-api:0.11.0` est construite;
- le package installe dans l'image est `llm-ops-sandbox==0.11.0`.

## Limites connues

- Aucun remote Git n'etait configure pendant cette session.
- `gh` n'etait pas installe.
- La CI GitHub distante doit etre verifiee apres creation du repo GitHub.
- La CI GitLab distante doit etre verifiee apres creation/configuration du miroir.
- Aucun secret n'est utilise.
- Aucun deploiement automatique n'est ajoute.
