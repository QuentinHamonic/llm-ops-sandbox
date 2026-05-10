# Kubernetes local

## Objectif

`v0.5.0` ajoute des manifests Kubernetes minimaux pour comprendre la logique de deploiement de l'API.

Cette version ne pretend pas etre une production Kubernetes. Elle montre:

- `ConfigMap` pour la configuration;
- `Deployment` pour faire tourner l'API;
- `Service` pour exposer l'API dans le cluster;
- probes HTTP sur `/health`;
- resources requests/limits;
- annotations Prometheus pour un futur scrape en cluster.

## Choix local

Outil cible: Kubernetes local via Docker Desktop.

Pourquoi:

- `kubectl` est deja disponible via Docker Desktop;
- `kind`, `k3d` et `minikube` ne sont pas installes localement;
- Docker Desktop est coherent avec le socle Docker Compose deja utilise.

## Structure

```txt
k8s/base/
  kustomization.yaml
  configmap.yaml
  deployment.yaml
  service.yaml
```

## Construire l'image locale

```powershell
docker build -t llm-ops-sandbox-api:0.8.1 .
```

## Valider les manifests dans le projet

```powershell
python scripts/check_k8s_manifests.py
```

Cette commande verifie les invariants attendus par le projet: image, probes, resources, Service et annotations Prometheus.

Les overlays backend sont valides par:

```powershell
python scripts/check_k8s_overlays.py
```

## Rendre les manifests sans cluster actif

```powershell
kubectl kustomize k8s/base
```

Cette commande verifie que la base Kustomize peut etre rendue par `kubectl`. Elle ne prouve pas qu'un cluster tourne.

## Appliquer sur Docker Desktop Kubernetes

Activer Kubernetes dans Docker Desktop, puis:

```powershell
kubectl config current-context
kubectl apply -k k8s/base
kubectl get pods
kubectl get svc
```

## Choisir le backend

`k8s/base/` reste le socle stable en `mock`.

Pour changer de backend sans modifier `k8s/base/configmap.yaml`, utiliser les overlays:

```powershell
kubectl apply -k k8s/overlays/mock
kubectl apply -k k8s/overlays/ollama
kubectl apply -k k8s/overlays/vllm
```

Chaque overlay:

- repart de `k8s/base/`;
- applique un patch de ConfigMap;
- applique un patch d'annotation sur le Deployment.

L'annotation `llm-ops-sandbox.io/backend` force Kubernetes a creer un nouveau Pod quand le backend change. Cela evite de modifier le ConfigMap puis d'oublier `kubectl rollout restart`.

Verifier le backend actif:

```powershell
kubectl rollout status deploy/llm-ops-sandbox-api
kubectl port-forward svc/llm-ops-sandbox-api 8000:8000
Invoke-RestMethod http://localhost:8000/backend/status
```

## Tester l'API dans le cluster

Port-forward:

```powershell
kubectl port-forward svc/llm-ops-sandbox-api 8000:8000
```

Puis dans un autre terminal:

```powershell
curl http://localhost:8000/health
curl http://localhost:8000/backend/status
curl http://localhost:8000/metrics
```

## Nettoyer

```powershell
kubectl delete -k k8s/base
kubectl delete -k k8s/overlays/vllm
```

## Limites

- Pas encore de namespace dedie.
- Pas encore de Helm.
- Pas encore de Prometheus Operator ou ServiceMonitor.
- Pas encore de secrets Kubernetes.
- L'image est locale et doit etre construite sur la machine avant application.
