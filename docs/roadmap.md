# Roadmap

Cette roadmap est le fil directeur du projet. Elle doit rester courte, vivante et honnete.

Objectif: savoir quoi faire ensuite, ce qui est deja fait, pourquoi on le fait, et ce que le mainteneur doit pouvoir expliquer.

## Regles de suivi

- Une tache terminee doit avoir une preuve: test, commande, capture, doc ou commit.
- Une tache trop grosse doit etre decoupee.
- Les choix importants doivent etre notes dans "Comment je pense".
- Le journal technique garde les details de session; la roadmap garde la trajectoire.
- Ne pas ajouter une nouvelle brique tant que la precedente n'est pas validable.
- Le projet utilise une seule convention de progression: les versions SemVer decrites dans `docs/versioning.md`.

## Etat global

Statut actuel: **`v0.3.0` validee localement**.

Ce que le projet prouve deja:

- Une API FastAPI demarre sans backend LLM externe.
- Le backend `mock` permet une demo stable.
- `/health`, `/chat` et `/metrics` existent.
- Les tests pytest passent.
- Ruff passe.
- Docker Compose est configure pour API, Prometheus et Grafana.
- Des commandes de preuve et runbooks operationnels existent.
- La documentation de base existe.

Ce que le projet ne prouve pas encore:

- Deploiement Kubernetes.
- CI GitLab.
- GitOps Flux CD.
- Serving vLLM.
- Monitoring GPU.
- Scenario incident/runbook complet.
- Scenarios de robustesse ou chaos engineering controles.

## `v0.1.0` - Socle local fiable

Objectif: avoir une base simple, testable et explicable.

| Statut | Tache | Preuve attendue |
| --- | --- | --- |
| Fait | Creer `AGENTS.md` | Instructions racine presentes |
| Fait | Creer API FastAPI minimale | `/health`, `/chat`, `/metrics` |
| Fait | Ajouter backend `mock` | Test `/chat` sans Ollama |
| Fait | Ajouter backend Ollama optionnel | Variables documentees |
| Fait | Ajouter metriques Prometheus | Test `/metrics` |
| Fait | Ajouter Docker Compose | `docker compose config` valide |
| Fait | Ajouter dashboard Grafana minimal | JSON provisionne |
| Fait | Ajouter docs initiales | README, architecture, roadmap, versioning |
| Fait | Definir docs publiques/privees | `.gitignore` exclut journal et notes entretien |
| Fait | Definir standard commentaires/contribution | `docs/contributing.md` et `AGENTS.md` |
| Fait | Ajouter licence open source | Apache-2.0 |
| Fait | Ajouter politique securite | `SECURITY.md` |
| Fait | Ajouter politique confidentialite/ethique | `docs/privacy-and-ethics.md` |
| Fait | Appliquer confidentialite aux metriques | Tests anti-fuite prompt/path dans `/metrics` |
| Fait | Ajouter commande unique de validation | `python scripts/check.py` |
| Fait | Documenter observabilite | `docs/observability.md` |
| Fait | Isoler la validation Docker | `scripts/check.py` utilise un `DOCKER_CONFIG` temporaire |
| Fait | Expliquer les bonnes pratiques | Public dans `contributing`, prive dans `interview-notes` |
| Fait | Decouper les tests unitaires | health, chat, config, metrics |
| Fait | Ajouter pre-commit local | Hook `project-check` vers `scripts/check.py` |
| Fait | Ajouter regle workaround vs fix perenne | `AGENTS.md` |
| Fait | Initialiser Git dans `llm-ops-sandbox/` | Commit `2407ab2` |

## `v0.2.0` - Observabilite locale validee

Objectif: prouver que la stack Docker Compose tourne vraiment avec API, Prometheus et Grafana.

| Statut | Tache | Preuve attendue |
| --- | --- | --- |
| Fait | Lancer vraiment `docker compose up --build` | API, Prometheus et Grafana accessibles |
| Fait | Verifier scrape Prometheus | Target API `UP` dans Prometheus |
| Fait | Faire une capture ou note Grafana | `docs/validation-v0.2.0.md` |

## Definition of done `v0.2.0`

`v0.2.0` sera consideree complete quand:

- `python scripts/check.py` passe.
- `docker compose up -d --build` lance API, Prometheus et Grafana.
- `GET /health` retourne `status=ok`.
- `POST /chat` fonctionne avec `backend=mock`.
- `GET /metrics` expose les metriques HTTP.
- Prometheus voit la target API en `up`.
- Grafana repond et charge le dashboard `LLM Ops Sandbox`.
- `docs/validation-v0.2.0.md` documente les preuves.
- Le tag Git `v0.2.0` existe.

## `v0.3.0` - Qualite et comprehension

Objectif: transformer le socle en preuve de methode.

| Statut | Tache | Preuve attendue |
| --- | --- | --- |
| Fait | Ajouter une section "Commandes de preuve" au README | Commandes curl et resultats attendus |
| Fait | Ajouter un runbook latence API | `docs/runbook-latency.md` |
| Fait | Ajouter un runbook backend LLM down | `docs/runbook-llm-backend-down.md` |
| Fait | Ajouter tests d'erreur `/chat` | Cas message vide et backend Ollama down |
| Fait | Ajouter un endpoint ou metrique backend status | Decision dans `docs/backend-status.md` |
| Fait | Noter une entree de journal locale | `docs/journal.md`, ignore par Git |

## Definition of done `v0.3.0`

`v0.3.0` sera consideree complete quand:

- `python scripts/check.py` passe.
- Le README contient des commandes de preuve avec resultats attendus.
- Les runbooks latence et backend LLM down existent.
- `/chat` couvre les erreurs de validation et d'indisponibilite backend.
- La decision sur le statut backend est documentee.
- `docs/validation-v0.3.0.md` documente les preuves.
- Le journal local garde une note de session.
- Le tag Git `v0.3.0` existe.

## `v0.4.0` - Mode LLM local

Objectif: brancher un vrai modele local sans casser la stabilite du mock.

| Statut | Tache | Preuve attendue |
| --- | --- | --- |
| A faire | Tester Ollama depuis l'hote | `/chat` repond avec `backend=ollama` |
| A faire | Documenter le modele utilise | Taille, raison du choix, limites |
| A faire | Ajouter un compose profile Ollama si utile | Lancement documente |
| A faire | Mesurer latence mock vs Ollama | Note courte dans docs |
| A faire | Ajouter un mini benchmark manuel | Commande + resultat |

## `v0.5.0` - Kubernetes minimal

Objectif: montrer la logique de deploiement sans viser une production reelle.

| Statut | Tache | Preuve attendue |
| --- | --- | --- |
| A faire | Choisir outil local: kind, k3d ou minikube | Decision documentee |
| A faire | Ajouter manifests API | Deployment, Service, ConfigMap |
| A faire | Ajouter probes | Liveness et readiness sur `/health` |
| A faire | Ajouter resources requests/limits | Manifests valides |
| A faire | Ajouter Prometheus scrape en cluster | Note ou manifest |
| A faire | Documenter commandes kubectl | README ou doc Kubernetes |

## `v0.6.0` - CI/CD

Objectif: montrer une pipeline sobre et credible.

GitLab CI ne remplace pas Git. Git sert d'abord a garder un historique clair du projet; GitLab CI servira ensuite a verifier automatiquement chaque changement pousse.

| Statut | Tache | Preuve attendue |
| --- | --- | --- |
| A faire | Ajouter `.gitlab-ci.yml` | Stages lint, test, build |
| A faire | Ajouter validation Docker build | Job CI ou commande locale |
| A faire | Ajouter validation manifests Kubernetes | `kubectl dry-run` ou kubeconform |
| A faire | Documenter strategie de secrets | Note courte |
| A faire | Documenter rollback attendu | Note courte |

## `v0.7.0` et `v0.8.0` - GitOps et vLLM

Objectif: aligner le projet avec le poste vise, apres le socle stable.

| Statut | Tache | Preuve attendue |
| --- | --- | --- |
| A faire | Ajouter structure GitOps | `gitops/` avec env local |
| A faire | Ajouter exemple Flux Kustomization | YAML documente |
| A faire | Ajouter exemple HelmRelease | Meme si non applique en prod |
| A faire | Ajouter mode vLLM | Doc + config separee |
| A faire | Ajouter notes GPU/DCGM | Limites honnetes si pas de test GPU |

## `v0.9.0` - Robustesse et chaos engineering local

Objectif: verifier que le service est observable et diagnostiquable quand une brique casse volontairement.

Cette phase doit rester locale, reversible et documentee. Elle ne doit pas ralentir le chemin critique des versions precedentes.

| Statut | Tache | Preuve attendue |
| --- | --- | --- |
| A faire | Definir une methode de scenario chaos local | Doc courte avec hypothese, action, signal, rollback |
| A faire | Simuler backend LLM indisponible | Runbook backend down + metrique/erreur visible |
| A faire | Simuler API arretee | Prometheus target `down` + procedure de recovery |
| A faire | Simuler mauvais scrape Prometheus | Diagnostic documente |
| A faire | Simuler latence API simple | Runbook latence enrichi |
| A faire | Ajouter un cours prive associe | `docs/cours/chaos-engineering-local.md` |

## Comment je pense

Cette section sert a montrer le raisonnement, pas seulement la liste de taches.

### Principe 1 - Stabilite avant ambition

Je commence par un backend `mock` parce qu'un service observable doit rester testable meme quand le backend LLM est absent. Cela evite de confondre bugs applicatifs et problemes de modele, GPU ou dependances locales.

### Principe 2 - Une brique, une preuve

Chaque nouvelle brique doit produire une preuve simple: test, commande, dashboard, doc ou runbook. Si je ne peux pas prouver qu'une brique marche, elle n'est pas terminee.

### Principe 3 - Comprendre par couches

Je ne cherche pas a memoriser tout Kubernetes, Prometheus ou vLLM d'un coup. Je construis une couche, je la valide, puis j'ecris ce que je dois pouvoir expliquer.

### Principe 4 - IA assistee, responsabilite humaine

L'IA peut aider a produire du code et du boilerplate, mais je reste responsable de la direction technique: architecture, tests, validation, documentation, limites et explication.

### Principe 5 - Projet public neutre

Ce projet ne doit pas exposer Mnemis, Evelynn ou mes donnees personnelles. Il sert a demontrer une competence LLM Ops generique et professionnelle.

### Principe 6 - Confidentialite par defaut

Les prompts, reponses, logs et metriques doivent etre traites comme des surfaces de fuite potentielles. Le projet doit mesurer le comportement du service sans exposer le contenu utilisateur.

### Principe 7 - Apprentissage asynchrone

Le projet public avance sur son chemin critique. Les exercices personnels, repetitions et manipulations de code servent a renforcer la competence, mais ne doivent pas bloquer une version. Quand une manipulation casse volontairement quelque chose, elle doit etre traitee comme un lab controle ou un futur scenario de robustesse.

## Definition of done `v0.1.0`

`v0.1.0` sera consideree complete quand:

- `pytest` passe.
- `ruff check .` passe.
- `ruff format --check .` passe.
- `python scripts/check.py` passe.
- `docker compose config` est valide.
- Le README permet a quelqu'un de relancer le projet.
- Les docs publiques expliquent les choix principaux.
- La licence, la securite et la confidentialite/ethique sont documentees.
- Les docs privees locales sont exclues du repo public.
- Git est initialise dans `llm-ops-sandbox/`.
- Un premier commit propre existe.
