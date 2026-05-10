# Validation v0.7.0

Objectif: prouver que la couche GitOps Flux est presente, documentee et validable sans cluster.

## Commandes locales

```powershell
python scripts/check_gitops_manifests.py
python scripts/check.py
```

Preuve attendue:

- `gitops/local/source.yaml` existe.
- `gitops/local/kustomization.yaml` pointe vers `./k8s/base`.
- L'exemple HelmRepository existe.
- L'exemple HelmRelease existe.
- Aucun secret n'est present dans les YAML GitOps.
- La validation globale du projet passe.

## Verification CI

`.gitlab-ci.yml` contient le job:

```txt
gitops-static-check
```

Ce job lance:

```powershell
python scripts/check_gitops_manifests.py
```

## Build Docker local

```powershell
docker build -t llm-ops-sandbox-api:0.7.0 .
```

Resultat:

- La commande passe.
- L'image `llm-ops-sandbox-api:0.7.0` est construite.
- Le package installe dans l'image est `llm-ops-sandbox==0.7.0`.

## Limites connues

- La validation ne lance pas Flux CD.
- Aucun cluster Kubernetes n'est modifie.
- L'URL Git Flux est un placeholder.
- Le HelmRelease monitoring reste un exemple pedagogique.
- Les secrets GitOps ne sont pas encore implementes avec SOPS, Sealed Secrets ou External Secrets.
