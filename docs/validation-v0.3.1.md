# Validation v0.3.1

Date: 2026-05-09

Objectif: prouver que la documentation API generee est disponible, lisible et synchronisee avec le contrat OpenAPI FastAPI.

## Commandes

```powershell
python scripts/export_api_docs.py
python scripts/export_api_docs.py --check
.\.venv\Scripts\python.exe scripts\check.py
docker compose up -d --build
```

Checks HTTP effectues:

```powershell
GET http://localhost:8000/docs
GET http://localhost:8000/openapi.json
```

## Resultats

| Verification | Resultat |
| --- | --- |
| `python scripts/check.py` | Ruff, format, pytest, API docs check et Compose config OK |
| Tests pytest | `12 passed` |
| Image API | package `llm-ops-sandbox==0.3.1` installe |
| API OpenAPI runtime | version `0.3.1` |
| Swagger UI | `/docs` repond `200` |
| Documentation JSON | `docs/generated/openapi.json` genere |
| Documentation Markdown | `docs/generated/api.md` genere |
| Check documentation | `python scripts/export_api_docs.py --check` confirme que les fichiers sont a jour |

## Notes

- Le code FastAPI reste la source de verite.
- `docs/generated/openapi.json` sert de contrat API exporte.
- `docs/generated/api.md` sert de porte d'entree lisible pour un lecteur junior.
- La documentation generee est verifiee dans `scripts/check.py` pour eviter qu'elle devienne obsolete.
