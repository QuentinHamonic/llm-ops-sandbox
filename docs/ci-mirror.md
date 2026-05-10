# Strategie CI GitHub et miroir GitLab

`v0.11.0` prepare deux chemins CI:

- GitHub Actions pour la validation publique principale;
- GitLab CI pour montrer la compatibilite avec la stack cible du poste.

## Decision

GitHub est choisi comme forge publique principale car le compte GitHub est disponible.

GitLab CI reste dans le repo via:

```txt
.gitlab-ci.yml
```

Le miroir GitLab doit recevoir le meme code pour executer la pipeline GitLab sans maintenir deux projets differents.

## Mode recommande

Le mode recommande est:

```txt
GitHub = source principale
GitLab = miroir aval pour executer GitLab CI
```

Flux:

```txt
developpement local
  -> push GitHub
  -> miroir GitLab
  -> pipeline GitLab CI
```

## Pourquoi pas deux sources principales ?

Deux sources principales creent vite des divergences:

- commits presents seulement d'un cote;
- tags differents;
- pipelines qui ne valident pas le meme code;
- confusion pendant un rollback.

Le projet doit garder une seule source de verite Git.

## Commandes locales apres creation des repos

Exemple avec GitHub comme `origin`:

```powershell
git remote add origin https://github.com/QuentinHamonic/llm-ops-sandbox.git
git push -u origin main --tags
```

Exemple avec GitLab comme remote secondaire manuel:

```powershell
git remote add gitlab https://gitlab.com/QuentinHamonic/llm-ops-sandbox.git
git push gitlab main --tags
```

Ces commandes supposent que les repos existent deja et que l'authentification Git est configuree.

## Miroir GitLab

Option 1: miroir configure dans GitLab.

Dans GitLab:

```txt
Settings -> Repository -> Mirroring repositories
```

Configurer GitLab pour recuperer le repo GitHub.

Regles:

- ne pas committer de token dans le repo;
- utiliser les secrets/variables de la forge si un token est necessaire;
- ne pas pousser directement dans le miroir GitLab sauf decision explicite;
- garder `main` et les tags comme references de validation.

Option 2: push manuel vers GitLab.

Cette option est plus simple en local, mais moins automatique:

```powershell
git push gitlab main --tags
```

Elle est acceptable pour une demo, mais moins proche d'un vrai flux industriel.

## Secrets

Aucun secret n'est requis en `v0.11.0`.

Futurs secrets possibles:

| Secret | Usage possible | Forge |
| --- | --- | --- |
| `GHCR_TOKEN` | Publier une image dans GitHub Container Registry | GitHub |
| `CI_REGISTRY_PASSWORD` | Publier une image dans GitLab Registry | GitLab |
| `KUBECONFIG` | Deployer vers un cluster | GitHub ou GitLab |

Ces secrets devront rester dans les variables de CI/CD, jamais dans Git.

## Rollback

Rollback simple:

1. Identifier le dernier tag sain.
2. Revenir au tag ou creer un commit correctif.
3. Pousser sur GitHub.
4. Laisser le miroir GitLab recuperer le meme historique.
5. Verifier GitHub Actions et GitLab CI.

Le point important: le rollback doit partir de la source principale, pas du miroir.

## Limites actuelles

- Aucun remote n'etait configure pendant la creation de `v0.11.0`.
- `gh` n'etait pas installe dans l'environnement local.
- La CI distante doit etre observee apres creation du repo GitHub.
- Le miroir GitLab doit etre cree cote GitLab ou pousse manuellement.

Cette version prepare le projet pour l'execution distante, mais la preuve finale sera le premier run vert sur GitHub et, si possible, sur GitLab.
