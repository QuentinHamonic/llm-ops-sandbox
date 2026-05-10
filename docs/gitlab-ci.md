# GitLab CI

`v0.6.0` ajoute une pipeline GitLab CI sobre pour automatiser les preuves deja lancees localement.

Cette CI ne remplace pas Git et ne pretend pas etre une chaine de production complete. Elle verifie que chaque changement pousse reste testable, formate, documente et construisible.

## Pipeline

La pipeline est definie dans `.gitlab-ci.yml`.

| Stage | Job | Objectif |
| --- | --- | --- |
| `lint` | `lint` | Verifier `ruff check .` et `ruff format --check .` |
| `test` | `test` | Lancer les tests rapides avec `pytest` |
| `validate` | `api-docs-check` | Verifier que la documentation API generee est a jour |
| `validate` | `compose-config` | Verifier que `compose.yml` est syntaxiquement coherent |
| `validate` | `k8s-static-check` | Verifier les invariants Kubernetes attendus par le projet |
| `validate` | `k8s-overlays-static-check` | Verifier les overlays backend Kubernetes |
| `validate` | `gitops-static-check` | Verifier les invariants GitOps Flux attendus |
| `validate` | `vllm-static-check` | Verifier les manifests vLLM exemples |
| `build` | `docker-build` | Construire l'image API dans la CI |

La structure de `.gitlab-ci.yml` est aussi verifiee localement par:

```powershell
python scripts/check_gitlab_ci.py
```

## Strategie choisie

La CI reste volontairement simple:

- pas de deploiement automatique;
- pas de secret requis en `v0.6.0`;
- pas de push d'image vers un registry;
- pas de cluster Kubernetes distant;
- pas de test Ollama obligatoire.

Les tests d'integration Ollama restent locaux et optionnels car ils dependent d'un service externe au job CI.

## Secrets

`v0.6.0` n'utilise aucun secret GitLab CI.

Regles pour les versions futures:

- stocker les secrets uniquement dans les variables CI/CD protegees de GitLab;
- ne jamais committer `.env`, token, cle API, kubeconfig ou credential Docker;
- masquer les variables sensibles quand GitLab le permet;
- limiter les variables de production aux branches/tags proteges;
- documenter tout nouveau secret: nom logique, usage, environnement, rotation, proprietaire.

Exemples de secrets possibles plus tard:

| Secret futur | Usage possible | Statut actuel |
| --- | --- | --- |
| `CI_REGISTRY_PASSWORD` | Push image Docker | Non utilise |
| `KUBECONFIG` | Acces cluster | Non utilise |
| `OLLAMA_AUTH_TOKEN` | Backend distant protege | Non utilise |

## Rollback attendu

En `v0.6.0`, la CI construit mais ne deploie rien. Le rollback est donc un rollback Git:

1. Identifier le dernier commit ou tag sain.
2. Revenir sur une branche propre depuis ce point.
3. Relancer `python scripts/check.py`.
4. Pousser un correctif ou revenir au tag stable selon le contexte.

Quand un deploiement automatique sera ajoute, le rollback devra etre documente avec:

- l'image precedente connue comme saine;
- la commande ou procedure de retour;
- les verifications post-rollback;
- les signaux Prometheus/Grafana a consulter.

## Limites

- Le job `k8s-static-check` ne remplace pas une validation par un vrai cluster.
- Le job `docker-build` ne publie pas encore d'image.
- La CI ne valide pas Ollama, vLLM, GPU, Flux CD ou secrets externes.
- La CI prouve une hygiene de projet, pas une production.
