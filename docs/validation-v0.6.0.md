# Validation v0.6.0

Objectif: prouver que la pipeline GitLab CI est coherente avec la validation locale du projet.

## Commandes locales

```powershell
python scripts/check.py
```

Preuve attendue:

- Ruff passe.
- Ruff format passe.
- Pytest passe: `14 passed, 1 skipped`.
- La documentation API generee est a jour.
- `.gitlab-ci.yml` passe la validation statique locale.
- `docker compose config` est valide.
- Les manifests Kubernetes passent la validation statique.

## Verification GitLab CI

```powershell
Get-Content .gitlab-ci.yml
```

La pipeline contient:

- `lint`: `ruff check .` et `ruff format --check .`;
- `test`: `pytest`;
- `api-docs-check`: verification OpenAPI/Markdown genere;
- `compose-config`: validation `docker compose config`;
- `k8s-static-check`: validation statique des manifests Kubernetes;
- `docker-build`: construction de l'image Docker API.

## Build Docker local

```powershell
docker build -t llm-ops-sandbox-api:0.6.0 .
```

Resultat de session:

- La commande passe.
- L'image `llm-ops-sandbox-api:0.6.0` est construite.
- Le package installe dans l'image est `llm-ops-sandbox==0.6.0`.

Point de vigilance:

Docker Desktop doit etre demarre pour reproduire cette preuve localement.

## Strategie secrets

`v0.6.0` ne demande aucun secret CI.

Les futurs secrets devront etre declares dans GitLab CI/CD variables, jamais dans le repo. Voir `docs/gitlab-ci.md`.

## Rollback

`v0.6.0` ne deploie rien automatiquement. Le rollback consiste donc a revenir a un commit ou tag sain, puis a relancer la validation locale.

## Limites connues

- La CI n'est pas encore executee sur une instance GitLab dans cette validation locale.
- Le build Docker CI ne pousse pas encore l'image vers un registry.
- Le controle Kubernetes reste statique et ne remplace pas un test sur cluster.
- Les tests Ollama restent optionnels et locaux.
