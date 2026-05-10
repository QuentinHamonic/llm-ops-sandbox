# GitOps local

Ce dossier contient des exemples Flux CD pour relier le depot Git aux manifests Kubernetes de `k8s/base/`.

Ces fichiers sont pedagogiques et validables statiquement. Ils ne sont pas appliques automatiquement en `v0.7.0`.

## Contenu

- `source.yaml`: source Git Flux qui pointe vers le depot applicatif.
- `kustomization.yaml`: reconciliation Flux vers `./k8s/base`.
- `helmrepository-monitoring-example.yaml`: exemple de source Helm pour une stack monitoring.
- `helmrelease-monitoring-example.yaml`: exemple de HelmRelease, non active par defaut.

## Limites

- L'URL Git est un placeholder neutre.
- Aucun secret n'est declare dans ce dossier.
- Aucun cluster Flux reel n'est requis pour la validation locale.
- Le HelmRelease monitoring est un exemple d'architecture, pas une installation testee.
