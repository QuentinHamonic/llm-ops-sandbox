# vLLM

`v0.8.0` ajoute un mode vLLM preparatoire.

L'objectif initial etait de montrer comment l'API pourrait appeler un serveur vLLM OpenAI-compatible, et comment un deploiement Kubernetes GPU pourrait etre structure. Depuis `v0.9.0`, le projet valide aussi un serveur vLLM reel en Docker avec GPU NVIDIA local.

## Backend API

Le backend vLLM s'active avec:

```env
LLM_BACKEND=vllm
VLLM_BASE_URL=http://localhost:8001/v1
VLLM_MODEL=TinyLlama/TinyLlama-1.1B-Chat-v1.0
```

L'API appelle:

- `POST /chat/completions` pour generer une reponse;
- `GET /models` pour verifier le statut sans envoyer de prompt.

Le backend `mock` reste le comportement par defaut.

## Kubernetes

Les manifests exemples sont dans:

```txt
k8s/vllm/
```

Ils contiennent:

- `ConfigMap`: modele et port vLLM;
- `Deployment`: serveur vLLM OpenAI-compatible;
- `Service`: exposition interne du backend vLLM;
- `Kustomization`: rendu du dossier.

Le Deployment demande:

```yaml
nvidia.com/gpu: "1"
```

Cela montre le besoin GPU sans pretendre qu'un GPU est disponible localement.

## Image vLLM

Le manifest utilise volontairement:

```txt
vllm/vllm-openai:REPLACE_WITH_TESTED_VERSION
```

Avant un vrai deploiement, il faut remplacer ce placeholder par une version testee dans l'environnement cible.

Ne pas utiliser une image non pinnee en production.

En validation locale `v0.9.0`, l'image Docker `vllm/vllm-openai:latest` a ete utilisee pour prouver le runtime GPU. Ce choix est acceptable pour un lab local, mais il doit etre remplace par une version pinnee avant toute validation reproductible ou publication de procedure production.

La documentation runtime detaillee est dans `docs/vllm-runtime.md`.

## Observabilite GPU et DCGM

Pour une vraie plateforme GPU, les signaux a surveiller seraient notamment:

- utilisation GPU;
- memoire GPU utilisee;
- erreurs GPU;
- temperature;
- saturation de requetes;
- latence de generation;
- tokens par seconde;
- redemarrages du pod vLLM.

DCGM Exporter est une option classique pour exposer les metriques GPU NVIDIA a Prometheus, mais il n'est pas installe en `v0.8.0`.

## Confidentialite

Le backend vLLM peut recevoir des prompts utilisateur.

Regles a garder:

- ne pas logger les prompts;
- ne pas mettre les prompts dans les metriques;
- ne pas envoyer de prompt dans `/backend/status`;
- documenter tout backend distant avant usage;
- garder vLLM local ou explicitement opt-in.

## Validation

```powershell
python scripts/check_vllm_manifests.py
python scripts/check.py
```

Ces validations verifient:

- la presence des manifests vLLM;
- le port `8000`;
- le modele configure;
- la demande GPU;
- l'image volontairement placeholder.

## Limites

- vLLM n'est pas installe automatiquement par le projet.
- Le runtime GPU est valide en Docker local, pas encore dans Kubernetes.
- Les performances mesurees sont indicatives et non un benchmark de charge.
- DCGM Exporter n'est pas configure.
- Le manifest vLLM est un exemple a adapter avant usage reel.
