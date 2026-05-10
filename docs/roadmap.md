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

Statut actuel: **`v0.11.0` en validation**.

Cap cible: rendre le projet credible pour une trajectoire **AI DevOps / Infrastructure / Optimisation**. Le projet ne pretend pas remplacer une experience production a grande echelle, mais il doit prouver une methode: concevoir, deployer, observer, automatiser, diagnostiquer et documenter une petite plateforme LLM Ops reproductible.

Ce que le projet prouve deja:

- Une API FastAPI demarre sans backend LLM externe.
- Le backend `mock` permet une demo stable.
- `/health`, `/chat` et `/metrics` existent.
- Les tests pytest passent.
- Ruff passe.
- Docker Compose est configure pour API, Prometheus et Grafana.
- Des commandes de preuve et runbooks operationnels existent.
- La documentation API est generee depuis OpenAPI.
- Ollama est branche comme backend local optionnel.
- Des manifests Kubernetes minimaux existent.
- Une pipeline GitLab CI sobre existe.
- Une structure GitOps Flux locale existe.
- Des overlays Kubernetes permettent de choisir le backend sans modifier la base.
- Un mode vLLM preparatoire existe.
- Un serveur vLLM reel a ete valide en Docker avec GPU NVIDIA local.
- Un exporter GPU local expose des metriques `nvidia-smi` pour Prometheus.
- Un dashboard Grafana GPU local existe.
- Une CI GitHub Actions est configuree.
- Une strategie de miroir GitLab CI est documentee.
- La documentation de base existe.

Ce que le projet ne prouve pas encore:

- Deploiement Kubernetes production.
- Serving vLLM GPU dans Kubernetes.
- Monitoring GPU Kubernetes/DCGM.
- CI distante executee sur une vraie forge.
- Flux CD reellement installe et connecte a un depot distant.
- Rollback automatise ou procedure GitOps testee.
- Autoscaling, scheduling GPU ou quotas.
- Alerting operationnel.
- Scenario incident/runbook complet.
- Scenarios de robustesse ou chaos engineering controles.

## Lecture cible Infomaniak

Cette section traduit la roadmap en competences proches du poste vise.

| Axe du poste | Etat actuel | Direction |
| --- | --- | --- |
| Serving LLM | Ollama reel valide, vLLM reel valide en Docker GPU | Stabiliser image/runtime vLLM puis tester chemin Kubernetes |
| Kubernetes | API deployee localement, overlays backend | Tester chemin GPU et rollback |
| CI/CD | GitHub Actions configuree, GitLab CI conservee pour miroir | Executer les pipelines apres publication distante |
| GitOps Flux | Manifests Flux prepares | Installer Flux et reconciler depuis GitHub/GitLab |
| Observabilite | Prometheus/Grafana API + GPU local | Ajouter alerting et monitoring Kubernetes/DCGM |
| Performance | Mini benchmark mock/Ollama/vLLM indicatif | Ajouter mesures tokens/sec et charge simple |
| Fiabilite | Tests, runbooks, health, metrics | Scenarios incident + recovery |
| Securite/ethique | Confidentialite logs/metriques documentee | Maintenir cette exigence sur GPU/GitOps |

Priorite: convertir les briques preparees en preuves runtime avant d'ajouter de nouveaux frameworks.

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

## `v0.3.1` - Documentation API generee

Objectif: permettre a un lecteur junior externe de comprendre l'API sans devoir lire tout le code ni lancer le service.

| Statut | Tache | Preuve attendue |
| --- | --- | --- |
| Fait | Enrichir OpenAPI FastAPI | Tags, descriptions, schemas et reponses documentees |
| Fait | Ajouter export OpenAPI | `docs/generated/openapi.json` |
| Fait | Ajouter resume Markdown API | `docs/generated/api.md` |
| Fait | Ajouter verification automatique | `python scripts/export_api_docs.py --check` dans `scripts/check.py` |
| Fait | Documenter la generation API | README |

## Definition of done `v0.3.1`

`v0.3.1` sera consideree complete quand:

- `python scripts/check.py` passe.
- `docs/generated/openapi.json` est a jour.
- `docs/generated/api.md` est a jour.
- Le README explique comment regenerer et verifier la documentation API.
- `docs/validation-v0.3.1.md` documente les preuves.
- Le tag Git `v0.3.1` existe.

## `v0.4.0` - Mode LLM local

Objectif: brancher un vrai modele local sans casser la stabilite du mock.

| Statut | Tache | Preuve attendue |
| --- | --- | --- |
| Fait | Tester Ollama depuis l'hote | `/chat` repond avec `backend=ollama` |
| Fait | Documenter le modele utilise | `docs/ollama-local.md` |
| Fait | Ajouter un compose profile Ollama si utile | Decision documentee: host Ollama en `v0.4.0` |
| Fait | Mesurer latence mock vs Ollama | `docs/benchmark-v0.4.0.md` |
| Fait | Ajouter un mini benchmark manuel | Commande + resultat |
| Fait | Ajouter statut backend non-generatif | `GET /backend/status` |

## Definition of done `v0.4.0`

`v0.4.0` sera consideree complete quand:

- `python scripts/check.py` passe.
- Le backend `mock` reste le comportement par defaut.
- Ollama repond localement avec `mistral:latest`.
- `POST /chat` repond avec `backend=ollama` quand `LLM_BACKEND=ollama`.
- `GET /backend/status` indique l'etat du backend configure sans envoyer de prompt.
- Le test d'integration Ollama passe quand `OLLAMA_INTEGRATION=1`.
- Le modele et les limites sont documentes.
- `docs/validation-v0.4.0.md` documente les preuves.
- Le tag Git `v0.4.0` existe.

## `v0.5.0` - Kubernetes minimal

Objectif: montrer la logique de deploiement sans viser une production reelle.

| Statut | Tache | Preuve attendue |
| --- | --- | --- |
| Fait | Choisir outil local: Docker Desktop Kubernetes | Decision documentee dans `docs/kubernetes-local.md` |
| Fait | Ajouter manifests API | `k8s/base/` avec Deployment, Service, ConfigMap |
| Fait | Ajouter probes | Liveness et readiness sur `/health` |
| Fait | Ajouter resources requests/limits | Manifests valides |
| Fait | Ajouter Prometheus scrape en cluster | Annotations Prometheus sur Pod et Service |
| Fait | Documenter commandes kubectl | README et `docs/kubernetes-local.md` |

## Definition of done `v0.5.0`

`v0.5.0` sera consideree complete quand:

- `python scripts/check.py` passe.
- `python scripts/check_k8s_manifests.py` passe.
- `kubectl kustomize k8s/base` rend les manifests hors sandbox.
- Le Deployment declare probes liveness/readiness sur `/health`.
- Le Deployment declare requests/limits CPU et memoire.
- Le Service expose l'API sur le port `8000`.
- Les manifests contiennent une indication de scrape Prometheus.
- Le README et `docs/kubernetes-local.md` documentent les commandes.
- `docs/validation-v0.5.0.md` documente les preuves.
- Le tag Git `v0.5.0` existe.

## `v0.6.0` - CI/CD

Objectif: montrer une pipeline sobre et credible.

GitLab CI ne remplace pas Git. Git sert d'abord a garder un historique clair du projet; GitLab CI servira ensuite a verifier automatiquement chaque changement pousse.

| Statut | Tache | Preuve attendue |
| --- | --- | --- |
| Fait | Ajouter `.gitlab-ci.yml` | Stages lint, test, validate, build |
| Fait | Ajouter validation Docker build | Job `docker-build` |
| Fait | Ajouter validation manifests Kubernetes | Job `k8s-static-check` |
| Fait | Ajouter validation Docker Compose | Job `compose-config` |
| Fait | Ajouter validation statique GitLab CI | `python scripts/check_gitlab_ci.py` |
| Fait | Documenter strategie de secrets | `docs/gitlab-ci.md` |
| Fait | Documenter rollback attendu | `docs/gitlab-ci.md` |

## Definition of done `v0.6.0`

`v0.6.0` sera consideree complete quand:

- `python scripts/check.py` passe.
- `.gitlab-ci.yml` contient lint, test, validations et build Docker.
- `python scripts/check_gitlab_ci.py` passe.
- La CI verifie Ruff, Pytest, documentation API generee, Docker Compose et manifests Kubernetes.
- Le build Docker est present dans la pipeline.
- La strategie de secrets est documentee.
- Le rollback attendu est documente.
- `docs/validation-v0.6.0.md` documente les preuves.
- Le tag Git `v0.6.0` existe.

## `v0.7.0` - GitOps Flux local

Objectif: aligner le projet avec le poste vise, apres le socle stable.

| Statut | Tache | Preuve attendue |
| --- | --- | --- |
| Fait | Ajouter structure GitOps | `gitops/local/` |
| Fait | Ajouter exemple Flux GitRepository | `gitops/local/source.yaml` |
| Fait | Ajouter exemple Flux Kustomization | `gitops/local/kustomization.yaml` |
| Fait | Ajouter exemple HelmRelease | `gitops/local/helmrelease-monitoring-example.yaml` |
| Fait | Ajouter validation statique GitOps | `python scripts/check_gitops_manifests.py` |
| Fait | Ajouter job CI GitOps | `gitops-static-check` |
| Fait | Documenter secrets et rollback GitOps | `docs/gitops.md` |

## Definition of done `v0.7.0`

`v0.7.0` sera consideree complete quand:

- `python scripts/check.py` passe.
- `python scripts/check_gitops_manifests.py` passe.
- `gitops/local/` contient une source Git Flux et une Kustomization vers `./k8s/base`.
- Un exemple HelmRepository/HelmRelease existe et reste documente comme exemple.
- `.gitlab-ci.yml` contient `gitops-static-check`.
- `docs/gitops.md` explique la strategie GitOps, secrets, rollback et limites.
- `docs/validation-v0.7.0.md` documente les preuves.
- Le tag Git `v0.7.0` existe.

## `v0.8.0` - vLLM mode candidature

Objectif: documenter et preparer un mode de serving vLLM sans pretendre a un test GPU local si le materiel n'est pas disponible.

| Statut | Tache | Preuve attendue |
| --- | --- | --- |
| Fait | Ajouter mode vLLM | `LLM_BACKEND=vllm` |
| Fait | Ajouter exemple de deploiement vLLM | `k8s/vllm/` |
| Fait | Ajouter notes GPU/DCGM | `docs/vllm.md` |
| Fait | Documenter variables vLLM | README et `docs/vllm.md` |
| Fait | Ajouter validation statique vLLM | `python scripts/check_vllm_manifests.py` |
| Fait | Ajouter job CI vLLM | `vllm-static-check` |

## Definition of done `v0.8.0`

`v0.8.0` sera consideree complete quand:

- `python scripts/check.py` passe.
- `LLM_BACKEND=vllm` est accepte par la configuration.
- Le backend vLLM utilise une API OpenAI-compatible sans dependency runtime lourde.
- Les tests rapides couvrent les erreurs vLLM sans appeler un vrai serveur.
- `k8s/vllm/` contient des manifests exemples avec demande GPU.
- `python scripts/check_vllm_manifests.py` passe.
- `.gitlab-ci.yml` contient `vllm-static-check`.
- `docs/vllm.md` documente variables, GPU, DCGM, confidentialite et limites.
- `docs/validation-v0.8.0.md` documente les preuves.
- Le tag Git `v0.8.0` existe.

## `v0.8.1` - Overlays Kubernetes backend

Objectif: rendre le switch Kubernetes `mock` / `ollama` / `vllm` reproductible sans modifier `k8s/base/configmap.yaml` a la main.

| Statut | Tache | Preuve attendue |
| --- | --- | --- |
| Fait | Garder `k8s/base` en mock stable | `LLM_BACKEND=mock` |
| Fait | Ajouter overlay mock | `k8s/overlays/mock` |
| Fait | Ajouter overlay Ollama | `k8s/overlays/ollama` |
| Fait | Ajouter overlay vLLM | `k8s/overlays/vllm` |
| Fait | Declencher rollout par overlay | Annotation Deployment par backend |
| Fait | Ajouter validation statique overlays | `python scripts/check_k8s_overlays.py` |
| Fait | Ajouter job CI overlays | `k8s-overlays-static-check` |

## Definition of done `v0.8.1`

`v0.8.1` sera consideree complete quand:

- `python scripts/check.py` passe.
- `python scripts/check_k8s_overlays.py` passe.
- Les overlays `mock`, `ollama` et `vllm` existent.
- `docs/kubernetes-local.md` documente les commandes d'application.
- `docs/validation-v0.8.1.md` documente les preuves.
- Le tag Git `v0.8.1` existe.

## `v0.9.0` - vLLM reel sur GPU local

Objectif: passer de "vLLM prepare" a "vLLM reellement execute" sur la machine locale avec GPU NVIDIA.

Cette version doit rester honnete: si vLLM ne tourne pas dans Kubernetes, on documente le blocage et on valide d'abord le mode Docker. La priorite est une preuve runtime, pas une architecture parfaite.

| Statut | Tache | Preuve attendue |
| --- | --- | --- |
| Fait | Verifier que Docker voit le GPU | Commande NVIDIA/CUDA avec `--gpus all` |
| Fait | Lancer un serveur vLLM reel | Endpoint OpenAI-compatible disponible |
| Fait | Brancher l'API sur vLLM | `/chat` repond avec `backend=vllm` |
| Fait | Tester `/backend/status` vLLM | `/models` liste le modele configure |
| Fait | Mesurer latence vLLM | `docs/benchmark-v0.9.0.md` |
| Fait | Comparer mock / Ollama / vLLM | Tableau de resultats avec limite Ollama |
| Fait | Documenter limites GPU/modele | `docs/vllm-runtime.md` |
| Fait | Ajouter cours prive vLLM runtime | `docs/cours/v0.9.0.md` |

## Definition of done `v0.9.0`

`v0.9.0` sera consideree complete quand:

- `python scripts/check.py` passe.
- Le GPU est visible depuis Docker.
- Un serveur vLLM repond localement.
- L'API FastAPI peut utiliser `LLM_BACKEND=vllm`.
- Un appel `/chat` renvoie une reponse vLLM reelle.
- Les resultats et limites sont documentes.
- `docs/validation-v0.9.0.md` documente les preuves.
- Le tag Git `v0.9.0` existe.

## `v0.10.0` - Monitoring GPU

Objectif: ajouter une observabilite GPU exploitable, proche des besoins AI DevOps.

| Statut | Tache | Preuve attendue |
| --- | --- | --- |
| Fait | Choisir le mode GPU metrics | Exporter local `nvidia-smi`, DCGM documente comme suite |
| Fait | Exposer les metriques GPU | `scripts/gpu_metrics_exporter.py` sur `/metrics` |
| Fait | Ajouter scrape Prometheus | Job `llm-ops-sandbox-gpu` |
| Fait | Ajouter dashboard Grafana GPU | `monitoring/grafana/dashboards/llm-ops-gpu.json` |
| Fait | Ajouter note latence/tokens | `docs/gpu-monitoring.md` documente les limites |
| Fait | Documenter limites Windows/Docker/Kubernetes | `docs/gpu-monitoring.md` |
| Fait | Ajouter validation statique monitoring | `python scripts/check_monitoring_config.py` |
| Fait | Ajouter cours prive monitoring GPU | `docs/cours/v0.10.0.md` |

## Definition of done `v0.10.0`

`v0.10.0` sera consideree complete quand:

- Prometheus scrape au moins une source de metriques GPU ou une limite explicite est documentee.
- Grafana affiche un dashboard GPU ou une capture/note de validation existe.
- Les metriques utiles pour une plateforme LLM sont expliquees.
- Les limites locales sont honnetement documentees.
- `docs/validation-v0.10.0.md` documente les preuves.
- Le tag Git `v0.10.0` existe.

## `v0.11.0` - CI GitHub et miroir GitLab

Objectif: passer d'une CI uniquement locale a une configuration publiable sur GitHub, avec GitLab CI conservee pour un miroir.

Le poste cite GitLab CI. Le projet utilise GitHub comme forge publique principale, mais garde `.gitlab-ci.yml` pour montrer la competence cible et permettre un miroir GitLab.

| Statut | Tache | Preuve attendue |
| --- | --- | --- |
| Fait | Ajouter GitHub Actions | `.github/workflows/ci.yml` |
| Fait | Ajouter validation statique GitHub Actions | `python scripts/check_github_actions.py` |
| Fait | Conserver `.gitlab-ci.yml` comme competence cible | GitLab CI verifie aussi le workflow GitHub |
| Fait | Documenter strategie miroir | `docs/ci-mirror.md` |
| Fait | Documenter variables/secrets CI | Aucun secret commite |
| Fait | Documenter rollback CI | `docs/ci-mirror.md` |
| A faire hors repo | Publier le repo distant | URL GitHub documentee apres creation |
| A faire hors repo | Executer une pipeline reelle | Lien ou note de run vert apres push |

## Definition of done `v0.11.0`

`v0.11.0` sera consideree complete cote repo quand:

- GitHub Actions est configure.
- La structure GitHub Actions est validee localement.
- GitLab CI reste disponible pour un miroir.
- La strategie GitHub/GitLab mirror est documentee.
- Le README indique comment lire les CI.
- Les secrets CI sont documentes sans etre exposes.
- Les limites d'execution distante sont explicites tant que le repo public n'est pas pousse.
- Le tag Git `v0.11.0` existe.

## `v0.12.0` - Flux CD reel

Objectif: installer Flux dans Kubernetes local et faire reconciler le cluster depuis un repo Git distant.

| Statut | Tache | Preuve attendue |
| --- | --- | --- |
| A faire | Installer Flux CLI | `flux --version` |
| A faire | Bootstrap Flux vers le repo distant | `flux-system` cree dans le cluster |
| A faire | Reconciler `k8s/overlays/mock` ou `ollama` | Flux applique l'overlay choisi |
| A faire | Verifier l'etat Flux | `flux get kustomizations` |
| A faire | Tester changement par Git | Commit config -> reconciliation observee |
| A faire | Documenter rollback GitOps | Revenir a un commit/tag sain |
| A faire | Documenter strategie secrets GitOps | SOPS/Sealed Secrets/External Secrets compares |

## Definition of done `v0.12.0`

`v0.12.0` sera consideree complete quand:

- Flux est installe dans le cluster local.
- Flux lit le repo distant.
- Une modification Git declenche une reconciliation.
- Le rollback GitOps est teste ou documente avec limites.
- Le tag Git `v0.12.0` existe.

## `v0.13.0` - Robustesse, incidents et chaos local

Objectif: verifier que le service est observable et diagnostiquable quand une brique casse volontairement.

Cette phase doit rester locale, reversible et documentee. Elle ne doit pas casser le chemin principal du projet.

| Statut | Tache | Preuve attendue |
| --- | --- | --- |
| A faire | Definir une methode de scenario chaos local | Doc courte avec hypothese, action, signal, rollback |
| A faire | Simuler backend LLM indisponible | Runbook backend down + metrique/erreur visible |
| A faire | Simuler API arretee | Prometheus target `down` + procedure de recovery |
| A faire | Simuler mauvais scrape Prometheus | Diagnostic documente |
| A faire | Simuler latence API simple | Runbook latence enrichi |
| A faire | Simuler echec vLLM si pertinent | Erreur visible et recovery documente |
| A faire | Ajouter alertes minimales | Regles ou doc d'alerting |
| A faire | Ajouter un cours prive associe | `docs/cours/chaos-engineering-local.md` |

## Definition of done `v0.13.0`

`v0.13.0` sera consideree complete quand:

- Au moins deux scenarios incident sont executes et documentes.
- Les signaux Prometheus/Grafana utiles sont identifies.
- Les procedures de retour a l'etat sain sont reproductibles.
- Le tag Git `v0.13.0` existe.

## `v1.0.0` - Dossier candidature

Objectif: transformer le sandbox en projet presentable en entretien, avec un parcours de demo clair et des limites honnetes.

| Statut | Tache | Preuve attendue |
| --- | --- | --- |
| A faire | Ecrire un scenario de demo 15 minutes | README ou `docs/demo.md` |
| A faire | Ajouter schema architecture final | Diagramme simple et lisible |
| A faire | Ajouter matrice poste/competences | `docs/interview-positioning.md` ou section README |
| A faire | Nettoyer la roadmap publique | Statut coherent |
| A faire | Verifier tags et historique Git | Tags jusqu'a `v1.0.0` |
| A faire | Verifier confidentialite publique | Pas de notes personnelles ni secrets |
| A faire | Preparer pitch entretien | Notes privees ignorees |

## Definition of done `v1.0.0`

`v1.0.0` sera consideree complete quand:

- Le projet peut etre clone, lance et compris par un lecteur externe.
- Une demo courte couvre API, observabilite, Kubernetes, backend reel et validation.
- Les limites sont explicites: pas de production reelle, mais une trajectoire claire.
- Le tag Git `v1.0.0` existe.

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
