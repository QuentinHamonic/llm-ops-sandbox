# Observability

Cette page explique les metriques exposees par l'API et la question operationnelle a laquelle chaque metrique repond.

Objectif: mesurer le comportement du service sans exposer de contenu utilisateur.

## Principes

- Les metriques decrivent le service, pas les prompts.
- Les labels Prometheus doivent rester bornes et bas-cardinalite.
- Les routes sont exposees sous forme de templates FastAPI, par exemple `/chat`.
- Les chemins non reconnus sont regroupes sous `unmatched`.
- Aucun prompt, reponse, email, token, IP ou identifiant utilisateur ne doit apparaitre dans `/metrics`.

## Metriques exposees

| Metrique | Type | Labels | Question operationnelle |
| --- | --- | --- | --- |
| `http_requests_total` | Counter | `method`, `path`, `status` | Combien de requetes arrivent, sur quelles routes, avec quels statuts ? |
| `http_request_duration_seconds` | Histogram | `method`, `path` | Est-ce que la latence HTTP augmente ? |
| `llm_requests_total` | Counter | `backend`, `status` | Est-ce que les appels au backend LLM reussissent ou echouent ? |
| `gpu_exporter_up` | Gauge | Aucun | Est-ce que l'exporter GPU local arrive a lire `nvidia-smi` ? |
| `gpu_memory_total_bytes` | Gauge | `gpu`, `name` | Quelle est la memoire GPU totale visible ? |
| `gpu_memory_used_bytes` | Gauge | `gpu`, `name` | Est-ce que la memoire GPU se remplit ? |
| `gpu_memory_free_bytes` | Gauge | `gpu`, `name` | Reste-t-il assez de memoire GPU pour charger un modele ? |
| `gpu_utilization_ratio` | Gauge | `gpu`, `name` | Le GPU travaille-t-il pendant le serving LLM ? |
| `gpu_temperature_celsius` | Gauge | `gpu`, `name` | La temperature GPU reste-t-elle dans une zone saine ? |
| `gpu_power_draw_watts` | Gauge | `gpu`, `name` | Quelle puissance le GPU consomme-t-il ? |
| `gpu_power_limit_watts` | Gauge | `gpu`, `name` | Quelle est la limite de puissance observee ? |

## Ce que la V0.1.0 ne mesure pas encore

- tokens par seconde;
- duree de generation LLM separee de la latence HTTP;
- disponibilite Prometheus/Grafana;
- metriques vLLM natives.

## Monitoring GPU local

`v0.10.0` ajoute un exporter local dans `scripts/gpu_metrics_exporter.py`.

Il est volontairement simple:

- il lit `nvidia-smi`;
- il expose `/metrics` sur `localhost:9101`;
- Prometheus le scrape depuis Docker via `host.docker.internal:9101`;
- les labels restent bornes: index GPU et nom materiel.

Ce choix est adapte au lab local Windows. Pour une plateforme Kubernetes GPU plus industrielle, DCGM Exporter reste une piste a valider dans une version future.

Ces metriques arriveront plus tard, quand elles repondront a une question operationnelle claire.

## Garde technique deja en place

Les tests verifient que:

- un prompt contenant email ou token ne fuit pas dans `/metrics`;
- un chemin arbitraire non reconnu ne devient pas un label Prometheus libre;
- les metriques de base restent exposees.

Ces tests protegent la confidentialite et la stabilite de Prometheus.

## Regle pour ajouter une metrique

Avant d'ajouter une metrique, documenter:

- la question operationnelle;
- le type de metrique;
- les labels;
- le risque de fuite de donnee;
- le risque de cardinalite.

Si cette justification n'est pas claire, ne pas ajouter la metrique.
