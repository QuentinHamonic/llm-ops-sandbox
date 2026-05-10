# GitOps local

`v0.7.0` ajoute une couche GitOps minimale avec Flux CD.

L'objectif n'est pas de deployer automatiquement en production. L'objectif est de montrer comment le depot Git peut devenir la source de verite pour Kubernetes.

## Idee generale

GitOps repose sur une boucle simple:

```txt
Git
  -> Flux observe le depot
  -> Flux rend les manifests Kubernetes
  -> Flux applique l'etat voulu dans le cluster
```

Dans ce projet:

- `k8s/base/` contient l'etat applicatif Kubernetes;
- `gitops/local/` contient les objets Flux qui disent quoi synchroniser;
- `scripts/check_gitops_manifests.py` verifie les invariants importants sans cluster.

## Fichiers

| Fichier | Role |
| --- | --- |
| `gitops/local/source.yaml` | Declare le depot Git observe par Flux |
| `gitops/local/kustomization.yaml` | Demande a Flux d'appliquer `./k8s/base` |
| `gitops/local/helmrepository-monitoring-example.yaml` | Exemple de repository Helm monitoring |
| `gitops/local/helmrelease-monitoring-example.yaml` | Exemple de HelmRelease monitoring |

## Commandes de validation

```powershell
python scripts/check_gitops_manifests.py
python scripts/check.py
```

Ces commandes ne contactent pas de cluster. Elles verifient que les fichiers attendus existent, que les objets Flux principaux sont coherents et qu'aucun terme evident de secret n'est present dans les YAML GitOps.

## Strategie secrets

Les manifests GitOps publics ne doivent pas contenir de secrets.

Pour une vraie installation Flux, les secrets doivent etre geres avec une solution dediee, par exemple:

- variables protegees GitLab CI;
- Sealed Secrets;
- SOPS;
- External Secrets Operator;
- secret Kubernetes cree hors repo public.

Ce projet ne choisit pas encore une solution de secret management pour eviter une complexite prematuree.

## Rollback GitOps

Le rollback GitOps attendu est:

1. Identifier le dernier commit ou tag sain.
2. Revenir a cet etat dans Git.
3. Laisser Flux reconciler le cluster.
4. Verifier `/health`, `/metrics` et les signaux Prometheus.

En `v0.7.0`, ce rollback reste documente mais non execute, car aucun cluster Flux reel n'est branche.

## Limites

- Flux CD n'est pas installe par ce projet.
- Les CRD Flux ne sont pas appliquees localement.
- L'URL Git dans `source.yaml` est un placeholder neutre.
- Le HelmRelease monitoring est un exemple pedagogique, pas une installation validee.
- La validation est statique et ne remplace pas une reconciliation Flux reelle.
