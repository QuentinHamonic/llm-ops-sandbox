# Validation v0.9.0

Objectif: prouver que vLLM ne reste plus seulement theorique. Le projet valide un serveur vLLM reel avec acces GPU local, puis branche l'API FastAPI dessus.

## Branche

```txt
feat/vllm-runtime
```

## GPU hote

Commande:

```powershell
nvidia-smi
```

Preuve observee:

```txt
NVIDIA GeForce RTX 5090
Driver 591.86
CUDA 13.1
VRAM 32607 MiB
```

## GPU visible depuis Docker

Commande:

```powershell
docker run --rm --gpus all nvidia/cuda:13.0.2-base-ubuntu24.04 nvidia-smi
```

Resultat:

- le conteneur CUDA demarre;
- `nvidia-smi` voit la RTX 5090 depuis Docker.

## Serveur vLLM

Commande:

```powershell
docker run --rm -d --name llm-ops-vllm-runtime --gpus all -p 8001:8000 --ipc=host vllm/vllm-openai:latest --model TinyLlama/TinyLlama-1.1B-Chat-v1.0 --gpu-memory-utilization 0.60
```

Validation:

```powershell
Invoke-RestMethod -Uri "http://localhost:8001/v1/models"
```

Resultat:

```txt
TinyLlama/TinyLlama-1.1B-Chat-v1.0
```

## API branchee sur vLLM

Commande de test sur port separe:

```powershell
$env:LLM_BACKEND = "vllm"
$env:VLLM_BASE_URL = "http://localhost:8001/v1"
$env:VLLM_MODEL = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
uvicorn app.main:app --host 127.0.0.1 --port 8010
```

Validation:

```powershell
Invoke-RestMethod http://localhost:8010/health
Invoke-RestMethod -Uri "http://localhost:8010/chat" -Method Post -ContentType "application/json" -Body '{"message":"Reponds en une phrase courte."}'
```

Resultat observe:

```txt
health.llm_backend = vllm
chat.backend = vllm
```

## Benchmark indicatif

Document:

```txt
docs/benchmark-v0.9.0.md
```

Resultats courts:

- `mock`: 19 ms;
- `vllm`: 323 ms;
- `ollama`: erreur memoire pendant que vLLM occupait le GPU.

## Image API

Commande:

```powershell
docker build -t llm-ops-sandbox-api:0.9.0 .
```

Resultat:

- l'image `llm-ops-sandbox-api:0.9.0` est construite;
- le package installe dans l'image est `llm-ops-sandbox==0.9.0`.

## Limites connues

- vLLM est valide en Docker local, pas encore dans Kubernetes.
- L'image vLLM utilise `latest`; une version pinnee reste a choisir.
- TinyLlama prouve le runtime, pas la qualite fonctionnelle du modele.
- Ollama et vLLM peuvent se concurrencer sur les ressources GPU/systeme locales.
- Les metriques GPU ne sont pas encore integrees a Prometheus.
- Pas encore de benchmark de charge.
