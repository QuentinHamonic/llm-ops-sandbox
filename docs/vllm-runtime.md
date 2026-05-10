# vLLM runtime GPU local

`v0.9.0` valide un serveur vLLM reel sur GPU NVIDIA local.

L'objectif n'est pas encore de faire du serving Kubernetes production. L'objectif est de prouver que la chaine suivante fonctionne:

```txt
client HTTP
  -> API FastAPI llm-ops-sandbox
  -> backend vLLM OpenAI-compatible
  -> conteneur Docker avec acces GPU
  -> modele TinyLlama localement servi
```

## Prerequis valides

Machine locale:

```txt
GPU: NVIDIA GeForce RTX 5090
VRAM: 32607 MiB
Driver: 591.86
CUDA visible hote: 13.1
```

Docker voit le GPU avec:

```powershell
docker run --rm --gpus all nvidia/cuda:13.0.2-base-ubuntu24.04 nvidia-smi
```

Cette commande lance un conteneur CUDA temporaire et execute `nvidia-smi` dedans. Si le GPU apparait, Docker peut transmettre le GPU au conteneur.

## Lancer vLLM

Commande utilisee en validation locale:

```powershell
docker run --rm -d --name llm-ops-vllm-runtime --gpus all -p 8001:8000 --ipc=host vllm/vllm-openai:latest --model TinyLlama/TinyLlama-1.1B-Chat-v1.0 --gpu-memory-utilization 0.60
```

Explication:

- `docker run`: demarre un conteneur.
- `--rm`: supprime le conteneur quand il s'arrete.
- `-d`: lance le conteneur en arriere-plan.
- `--name llm-ops-vllm-runtime`: donne un nom stable au conteneur.
- `--gpus all`: autorise l'acces aux GPU NVIDIA.
- `-p 8001:8000`: expose le port `8000` du conteneur sur `localhost:8001`.
- `--ipc=host`: partage l'IPC hote, option souvent utile pour PyTorch/vLLM.
- `vllm/vllm-openai:latest`: image vLLM OpenAI-compatible utilisee pour le lab.
- `--model TinyLlama/TinyLlama-1.1B-Chat-v1.0`: modele charge.
- `--gpu-memory-utilization 0.60`: limite la part de memoire GPU que vLLM peut utiliser.

Verifier les logs:

```powershell
docker logs --tail 120 llm-ops-vllm-runtime
```

Preuve observee:

- vLLM `0.20.2`;
- modele `TinyLlama/TinyLlama-1.1B-Chat-v1.0`;
- backend CUDA actif;
- FlashAttention utilise;
- serveur disponible sur `http://0.0.0.0:8000` dans le conteneur.

## Verifier l'API vLLM directe

Lister les modeles:

```powershell
Invoke-RestMethod -Uri "http://localhost:8001/v1/models"
```

Resultat attendu:

```txt
TinyLlama/TinyLlama-1.1B-Chat-v1.0
```

Tester une completion:

```powershell
$body = @{
  model = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
  messages = @(@{ role = "user"; content = "Reponds en une phrase courte: quel est le role de vLLM ?" })
  max_tokens = 80
} | ConvertTo-Json -Depth 5

Invoke-RestMethod -Uri "http://localhost:8001/v1/chat/completions" -Method Post -ContentType "application/json" -Body $body
```

Ce test prouve que vLLM repond au format OpenAI-compatible.

## Brancher l'API FastAPI sur vLLM

L'API doit etre configuree avec:

```powershell
$env:LLM_BACKEND = "vllm"
$env:VLLM_BASE_URL = "http://localhost:8001/v1"
$env:VLLM_MODEL = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
uvicorn app.main:app --reload
```

Verifier le backend actif:

```powershell
Invoke-RestMethod http://localhost:8000/backend/status
```

Resultat attendu:

```txt
backend: vllm
available: true
detail: Configured vLLM model is available.
```

Tester `/chat`:

```powershell
Invoke-RestMethod -Uri "http://localhost:8000/chat" -Method Post -ContentType "application/json" -Body '{"message":"Reponds avec exactement OK."}'
```

Resultat attendu:

```txt
backend: vllm
```

## Limites observees

La validation locale a montre une contention de ressources entre vLLM et Ollama.

Pendant que vLLM occupait le GPU, Ollama a retourne:

```txt
model requires more system memory (5.5 GiB) than is available (4.8 GiB)
```

Interpretation:

- lancer plusieurs serveurs de modeles sur la meme machine peut saturer la memoire GPU ou systeme;
- en contexte industriel, il faut piloter les ressources par quotas, scheduling GPU, limites memoire et monitoring;
- le fait que chaque backend soit configurable separement est utile, mais ne remplace pas une strategie de capacite.

## Limites restantes

- L'image vLLM utilisee est `latest`; une version reproductible devra etre pinnee.
- Le modele TinyLlama sert a valider l'infrastructure, pas la qualite de reponse.
- Le serving vLLM n'est pas encore deployee dans Kubernetes.
- Les metriques GPU ne sont pas encore scrapees par Prometheus.
- Pas encore de benchmark de charge, de tokens/seconde ni de p95.
