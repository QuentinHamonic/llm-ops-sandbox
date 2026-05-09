# API generee

> Fichier genere par `python scripts/export_api_docs.py`. Ne pas modifier a la main.

Version API: `0.3.1`

LLM Ops Sandbox expose une API FastAPI minimale avec un backend LLM mock par defaut, un backend Ollama optionnel et des metriques Prometheus. Le projet privilegie la reproductibilite, l'observabilite et la confidentialite.

## Endpoints

| Methode | Chemin | Resume |
| --- | --- | --- |
| POST | `/chat` | Envoyer un message au backend LLM configure |
| GET | `/health` | Verifier que l'API est vivante |
| GET | `/metrics` | Exposer les metriques Prometheus |

## Details

## POST `/chat`

Utilise le backend `mock` par defaut pour garantir une demo stable. Si `LLM_BACKEND=ollama`, l'API appelle Ollama et retourne `502` si le backend ne repond pas correctement.

Tags: `Chat`

Reponses documentees:

- `200`: Successful Response
- `422`: Requete invalide, par exemple message vide ou absent.
- `502`: Backend LLM configure indisponible ou reponse inutilisable.

## GET `/health`

Retourne un statut simple pour les humains, Docker Compose et les futurs probes Kubernetes. Ce endpoint ne contacte pas activement un backend LLM externe.

Tags: `Health`

Reponses documentees:

- `200`: Successful Response

## GET `/metrics`

Expose les compteurs et histogrammes Prometheus. Les labels doivent rester bornes et ne jamais contenir les prompts, reponses, secrets ou identifiants utilisateur.

Tags: `Observability`

Reponses documentees:

- `200`: Metriques Prometheus au format texte.
