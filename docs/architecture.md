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

Le backend `mock` garantit que la demo fonctionne toujours. C'est volontaire: avant d'ajouter vLLM ou Kubernetes, le socle doit etre stable et testable.

Ollama est optionnel. Il sert a brancher un vrai modele local sans changer l'interface HTTP de l'API.

Prometheus scrape `/metrics` sur l'API. Grafana lit Prometheus et affiche les signaux de base: volume de requetes, latence p95, erreurs et appels backend.

Kubernetes est documente par des manifests minimaux dans `k8s/base/`: `ConfigMap`, `Deployment` et `Service`. Cette couche montre la logique de deploiement, les probes et les resources, mais ne represente pas encore une production.

GitLab CI automatise les controles locaux principaux: lint, format, tests, documentation API generee, validation Docker Compose, validation statique Kubernetes et build Docker. Cette couche verifie le projet, mais ne deploie pas encore.

## Limites connues

- Kubernetes minimal seulement, sans production hardening.
- GitLab CI sans deploiement automatique.
- Pas encore de Flux CD.
- Pas encore de vLLM.
- Pas d'authentification: ce projet est un sandbox local.

Ces limites sont intentionnelles pour la V1.
