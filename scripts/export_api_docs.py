from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

from app.main import app

ROOT = Path(__file__).resolve().parents[1]
GENERATED_DIR = ROOT / "docs" / "generated"
OPENAPI_PATH = GENERATED_DIR / "openapi.json"
MARKDOWN_PATH = GENERATED_DIR / "api.md"


def endpoint_rows(openapi_schema: dict[str, Any]) -> list[str]:
    rows = ["| Methode | Chemin | Resume |", "| --- | --- | --- |"]
    for path, methods in sorted(openapi_schema["paths"].items()):
        for method, operation in sorted(methods.items()):
            rows.append(
                "| {method} | `{path}` | {summary} |".format(
                    method=method.upper(),
                    path=path,
                    summary=operation.get("summary", ""),
                )
            )
    return rows


def operation_sections(openapi_schema: dict[str, Any]) -> list[str]:
    sections: list[str] = []
    for path, methods in sorted(openapi_schema["paths"].items()):
        for method, operation in sorted(methods.items()):
            sections.extend(
                [
                    f"## {method.upper()} `{path}`",
                    "",
                    operation.get("description") or operation.get("summary", ""),
                    "",
                    "Tags: " + ", ".join(f"`{tag}`" for tag in operation.get("tags", ["untagged"])),
                    "",
                    "Reponses documentees:",
                    "",
                ]
            )
            responses = operation.get("responses", {})
            for status_code, response in sorted(responses.items()):
                sections.append(f"- `{status_code}`: {response.get('description', '')}")
            sections.append("")
    return sections


def build_markdown(openapi_schema: dict[str, Any]) -> str:
    info = openapi_schema["info"]
    lines = [
        "# API generee",
        "",
        "> Fichier genere par `python scripts/export_api_docs.py`. Ne pas modifier a la main.",
        "",
        f"Version API: `{info['version']}`",
        "",
        info.get("description", ""),
        "",
        "## Endpoints",
        "",
        *endpoint_rows(openapi_schema),
        "",
        "## Details",
        "",
        *operation_sections(openapi_schema),
    ]
    return "\n".join(lines).rstrip() + "\n"


def check_file(path: Path, expected: str) -> bool:
    if not path.exists():
        print(f"Missing generated file: {path.relative_to(ROOT)}")
        return False
    current = path.read_text(encoding="utf-8")
    if current != expected:
        print(f"Outdated generated file: {path.relative_to(ROOT)}")
        return False
    return True


def main() -> int:
    check_only = "--check" in sys.argv[1:]
    GENERATED_DIR.mkdir(parents=True, exist_ok=True)
    openapi_schema = app.openapi()
    openapi_content = json.dumps(openapi_schema, indent=2, ensure_ascii=False) + "\n"
    markdown_content = build_markdown(openapi_schema)

    if check_only:
        openapi_ok = check_file(OPENAPI_PATH, openapi_content)
        markdown_ok = check_file(MARKDOWN_PATH, markdown_content)
        if openapi_ok and markdown_ok:
            print("Generated API docs are up to date.")
            return 0
        print("Run python scripts/export_api_docs.py to refresh generated API docs.")
        return 1

    OPENAPI_PATH.write_text(openapi_content, encoding="utf-8")
    MARKDOWN_PATH.write_text(markdown_content, encoding="utf-8")
    print(f"Wrote {OPENAPI_PATH.relative_to(ROOT)}")
    print(f"Wrote {MARKDOWN_PATH.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
