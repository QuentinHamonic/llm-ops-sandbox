# Validation v0.8.0

Objectif: prouver que le mode vLLM est prepare, documente et validable sans GPU local.

## Commandes locales

```powershell
python scripts/check_vllm_manifests.py
python scripts/check.py
```

Preuve attendue:

- Le backend applicatif accepte `LLM_BACKEND=vllm`.
- Le backend `mock` reste le comportement par defaut.
- Les tests rapides ne dependent pas de vLLM, GPU ou reseau externe.
- `k8s/vllm/` contient ConfigMap, Deployment, Service et Kustomization.
- Le Deployment vLLM demande `nvidia.com/gpu: "1"`.
- L'image vLLM reste un placeholder a remplacer par une version testee.
- La CI contient le job `vllm-static-check`.

## Build Docker local

```powershell
docker build -t llm-ops-sandbox-api:0.8.0 .
```

Preuve attendue:

- l'image API est construite;
- le package installe dans l'image est `llm-ops-sandbox==0.8.0`.

Resultat:

- La commande passe.
- L'image `llm-ops-sandbox-api:0.8.0` est construite.

## Limites connues

- Aucun serveur vLLM reel n'est lance.
- Aucun GPU n'est teste.
- DCGM Exporter est documente mais pas installe.
- Les performances vLLM ne sont pas mesurees.
- Le manifest `k8s/vllm/` est un exemple de structure, pas un deploiement production.
