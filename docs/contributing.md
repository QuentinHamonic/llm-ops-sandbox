# Contributing

Ce projet est construit comme un laboratoire LLM Ops lisible et reproductible.

Le standard attendu est simple: petits changements, intention claire, tests verts, documentation utile.

## Style de code

- Code, modules, variables et endpoints en anglais.
- Documentation projet en francais par defaut.
- Preferer une implementation simple et explicable a une abstraction prematuree.
- Garder les fonctions courtes quand c'est naturel.
- Nommer clairement les concepts metier: backend, health, metrics, request, latency.
- Eviter les changements cosmetiques sans lien avec la tache.

## Commentaires dans le code

Les commentaires sont bienvenus quand ils aident un futur lecteur a comprendre l'intention.

Commenter:

- un compromis technique;
- une limite volontaire;
- un comportement non evident;
- une integration avec un outil externe;
- une decision qui sera utile en entretien ou en exploitation.

Eviter de commenter:

- ce que le code dit deja clairement;
- les affectations triviales;
- les commentaires longs qui devraient etre dans la documentation;
- les commentaires devenus faux apres refactor.

Exemple utile:

```python
# Keep the mock backend as the default so the API remains testable without a local model.
backend = MockBackend()
```

Exemple inutile:

```python
# Assign backend to MockBackend.
backend = MockBackend()
```

## Tests et validation

Avant de considerer une tache terminee:

```powershell
python scripts/check.py
```

Cette commande lance:

```powershell
ruff check .
ruff format --check .
pytest
docker compose config
```

Pour l'etape Docker, `scripts/check.py` utilise un `DOCKER_CONFIG` temporaire et vide. Cela evite que la validation depende de credentials ou de fichiers Docker personnels.

Pour une future tache Kubernetes, ajouter une commande de validation dans la doc de la tache.

## Documentation

Une nouvelle brique doit etre accompagnee au minimum de:

- une commande de preuve;
- une limite connue si le comportement est simplifie;
- une note dans la roadmap si elle change la trajectoire;
- un runbook si elle introduit un mode de panne exploitable.

## Confidentialite et securite

- Utiliser des donnees synthetiques dans les tests et exemples.
- Ne pas ajouter de prompt, reponse ou identifiant utilisateur dans les logs ou metriques.
- Ne pas ajouter d'appel a un service tiers sans le documenter clairement.
- Toute nouvelle integration d'observabilite doit respecter `docs/privacy-and-ethics.md`.
- Toute modification touchant secrets, logs, reseau ou dependances doit tenir compte de `SECURITY.md`.

## Git

- Commits petits et lisibles.
- Un commit doit correspondre a une intention claire.
- Les docs privees locales restent hors repo public.
- Avant toute commande Git construite, l'agent annonce la commande exacte et son intention.

## Pourquoi ces pratiques existent

Ces regles ne sont pas la pour alourdir le projet. Elles rendent le travail verifiable:

- architecture simple: un recruteur ou mainteneur peut comprendre vite;
- tests: le code genere ou modifie reste controlable;
- validation unique: on sait rapidement si le projet est propre;
- confidentialite: les metriques et logs ne deviennent pas des fuites de donnees;
- Git propre: l'historique raconte une progression professionnelle.

## Pre-commit

`pre-commit` est optionnel mais recommande une fois Git initialise.

```powershell
.\.venv\Scripts\Activate.ps1
pre-commit install
pre-commit run --all-files
```

Le hook local lance `python scripts/check.py`. Il doit etre installe et lance depuis la venv active pour trouver les dependances dev comme Ruff et pytest. Cela evite d'oublier lint, format, tests ou validation Compose avant un commit.
