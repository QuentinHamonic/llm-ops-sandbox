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

## Ce que la V0.1.0 ne mesure pas encore

- tokens par seconde;
- duree de generation LLM separee de la latence HTTP;
- saturation CPU/RAM/GPU;
- disponibilite Prometheus/Grafana;
- metriques vLLM natives.

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
