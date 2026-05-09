# Decision - statut backend LLM

## Contexte

`v0.3.0` ajoute des runbooks et des tests d'erreur, mais le backend reel reste optionnel. Le backend par defaut est toujours `mock`.

La question est: faut-il ajouter maintenant un endpoint ou une metrique de statut backend?

## Decision

Ne pas ajouter de nouvel endpoint dedie en `v0.3.0`.

Pour cette version:

- `GET /health` indique deja le backend configure via `llm_backend`;
- `POST /chat` prouve le comportement reel du backend utilise;
- `llm_requests_total{backend,status}` expose les succes et erreurs backend;
- le runbook backend down documente le diagnostic quand Ollama est indisponible.

## Pourquoi

Un endpoint de readiness backend serait trompeur tant que le backend `mock` est le mode par defaut et qu'Ollama reste optionnel.

Ajouter un vrai check actif d'Ollama maintenant aurait deux risques:

- ralentir ou fragiliser `/health`;
- creer une dependance reseau dans une version dont l'objectif principal est la methode et la reproductibilite.

## Evolution `v0.4.0`

`v0.4.0` ajoute `GET /backend/status`.

Ce endpoint reste separe de `/health` pour eviter de rendre le healthcheck principal dependant d'un service LLM externe. Pour Ollama, il interroge `/api/tags` et ne transmet aucun prompt au modele.

Le choix reste compatible avec la confidentialite: aucun prompt, reponse, token, IP ou identifiant utilisateur n'est ajoute dans les metriques.
