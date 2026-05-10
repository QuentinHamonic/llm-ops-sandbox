# Validation v0.8.1

Objectif: eviter de modifier `k8s/base/configmap.yaml` a la main pour changer de backend Kubernetes.

## Commandes locales

```powershell
python scripts/check_k8s_overlays.py
python scripts/check.py
kubectl kustomize k8s/overlays/mock
kubectl kustomize k8s/overlays/ollama
kubectl kustomize k8s/overlays/vllm
```

Preuve attendue:

- `k8s/base/` reste en backend `mock`.
- `k8s/overlays/mock` configure `LLM_BACKEND=mock`.
- `k8s/overlays/ollama` configure `LLM_BACKEND=ollama`.
- `k8s/overlays/vllm` configure `LLM_BACKEND=vllm` et inclut `k8s/vllm`.
- Chaque overlay change l'annotation `llm-ops-sandbox.io/backend` du Deployment pour declencher un rollout.
- La CI contient `k8s-overlays-static-check`.
- Les trois overlays sont rendus correctement par `kubectl kustomize`.

## Commandes Kubernetes utiles

```powershell
kubectl apply -k k8s/overlays/mock
kubectl apply -k k8s/overlays/ollama
kubectl apply -k k8s/overlays/vllm
```

Verifier le backend actif:

```powershell
kubectl rollout status deploy/llm-ops-sandbox-api
Invoke-RestMethod http://localhost:8000/backend/status
```

## Build Docker local

```powershell
docker build -t llm-ops-sandbox-api:0.8.1 .
```

Preuve attendue:

- l'image API est construite;
- le package installe dans l'image est `llm-ops-sandbox==0.8.1`.

Resultat:

- La commande passe.
- L'image `llm-ops-sandbox-api:0.8.1` est construite.

## Limites connues

- Les overlays ne synchronisent pas Docker Compose; ils concernent seulement Kubernetes.
- L'overlay vLLM reste dependant de l'image vLLM placeholder tant qu'une version reelle n'est pas testee.
- Les secrets restent hors scope: aucun secret ne doit etre stocke dans les overlays.
