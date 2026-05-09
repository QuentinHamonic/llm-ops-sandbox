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

## Evolution prevue

En `v0.4.0`, quand Ollama sera teste comme backend local reel, on pourra ajouter un statut plus precis:

- soit un endpoint `GET /backend/status`;
- soit une metrique basse cardinalite de disponibilite backend;
- soit un check separe qui ne bloque pas `/health`.

Le choix devra rester compatible avec la confidentialite: aucun prompt, reponse, token, IP ou identifiant utilisateur dans les metriques.
