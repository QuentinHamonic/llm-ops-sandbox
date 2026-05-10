# Architecture

## Vue logique

```txt
User
  -> FastAPI API
  -> LLM backend
       - mock by default
       - Ollama optionally
  -> Prometheus metrics
  -> Grafana dashboard
```

## Role des briques

FastAPI expose les endpoints HTTP du service:

- `/health` pour verifier que l'API est vivante;
- `/chat` pour simuler une requete utilisateur vers un backend LLM;
- `/metrics` pour exposer les metriques au format Prometheus.

Le backend `mock` garantit que la demo fonctionne toujours. C'est volontaire: les backends reels peuvent dependre du GPU, d'un modele local ou d'un service separe, alors que le socle API doit rester stable et testable.

Ollama est optionnel. Il sert a brancher un vrai modele local sans changer l'interface HTTP de l'API.

vLLM est optionnel. Il est traite comme un backend OpenAI-compatible via HTTP, ce qui evite d'ajouter une dependance Python lourde dans l'API et garde les tests rapides independants du GPU.

Prometheus scrape `/metrics` sur l'API. Grafana lit Prometheus et affiche les signaux de base: volume de requetes, latence p95, erreurs et appels backend.

Kubernetes est documente par des manifests minimaux dans `k8s/base/`: `ConfigMap`, `Deployment` et `Service`. Cette couche montre la logique de deploiement, les probes et les resources, mais ne represente pas encore une production.

GitLab CI automatise les controles locaux principaux: lint, format, tests, documentation API generee, validation Docker Compose, validation statique Kubernetes et build Docker. Cette couche verifie le projet, mais ne deploie pas encore.

GitOps est represente par des exemples Flux CD dans `gitops/local/`. Flux observe un depot Git et reconcilie `k8s/base/` comme etat voulu. Cette couche est statique et pedagogique en `v0.7.0`: elle documente la logique sans installer Flux dans un cluster.

vLLM est represente par des manifests exemples dans `k8s/vllm/`. Depuis `v0.9.0`, le projet valide aussi un serving vLLM reel en Docker avec GPU NVIDIA local. Le chemin Kubernetes GPU reste une etape separee: il dependra d'une image pinnee, du runtime NVIDIA dans le cluster et d'une strategie de monitoring GPU.

## Limites connues

- Kubernetes minimal seulement, sans production hardening.
- GitLab CI sans deploiement automatique.
- Flux CD documente, mais pas installe ni reconcilie sur un cluster reel.
- vLLM teste en Docker sur GPU local, mais pas encore deploiement Kubernetes GPU complet.
- Pas d'authentification: ce projet est un sandbox local.

Ces limites sont intentionnelles pour la V1.
