# Benchmark manuel v0.9.0

## Objectif

Comparer rapidement les backends `mock`, `ollama` et `vllm`.

Ce benchmark est indicatif. Il sert a verifier le comportement local et a reperer les limites operationnelles, pas a publier une mesure de performance.

## Conditions

Machine locale Windows avec:

```txt
GPU: NVIDIA GeForce RTX 5090
vLLM: vllm/vllm-openai:latest, logs vLLM 0.20.2
Modele vLLM: TinyLlama/TinyLlama-1.1B-Chat-v1.0
Modele Ollama: mistral:latest
```

Prompt synthetique:

```txt
Reponds avec exactement OK.
```

## Resultats observes

| Backend | Statut | Latence observee | Note |
| --- | --- | ---: | --- |
| `mock` | OK | 19 ms | Reponse deterministe sans modele |
| `vllm` | OK | 323 ms | Reponse reelle via serveur vLLM Docker GPU |
| `ollama` | Erreur pendant vLLM actif | Non mesuree | Ollama a manque de memoire disponible pendant que vLLM occupait le GPU |

Erreur Ollama observee:

```txt
model requires more system memory (5.5 GiB) than is available (4.8 GiB)
```

Memoire GPU observee pendant vLLM:

```txt
NVIDIA GeForce RTX 5090, 32607 MiB total, 25945 MiB used, 6243 MiB free
```

## Interpretation

Le backend `mock` reste le backend de securite: il permet de tester l'API sans dependance externe.

Le backend `vllm` prouve que l'API peut appeler un serveur de serving LLM OpenAI-compatible qui utilise le GPU local.

L'erreur Ollama est un signal important: sur une machine locale, deux runtimes LLM peuvent entrer en concurrence pour la memoire GPU ou systeme. En environnement industriel, ce probleme doit etre gere par:

- scheduling GPU;
- requests/limits Kubernetes;
- monitoring GPU;
- quotas;
- choix de modele;
- isolation des workloads.

## Limites

- Une seule requete mesuree par backend.
- Pas de p50/p95/p99.
- Pas de charge concurrente.
- Pas de mesure tokens/seconde.
- Pas de redemarrage propre entre chaque runtime GPU.
- Ollama doit etre re-teste seul si on veut une comparaison latence stricte.
