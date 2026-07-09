"""Resolve bundled or override OpenAPI JSON for offline spec lookup."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any


def resolve_openapi_json_path() -> Path | None:
    bundled = Path(__file__).parent / "data" / "saxo_openapi.json"
    if bundled.is_file():
        return bundled

    env_path = os.environ.get("SAXO_OPENAPI_JSON_PATH")
    if env_path:
        override = Path(env_path)
        if override.is_file():
            return override

    # Monorepo dev fallback (parent tools/saxo_openapi_generator)
    dev_path = (
        Path(__file__).resolve().parents[3]
        / "saxo_openapi_generator"
        / "output"
        / "saxo_openapi.json"
    )
    if dev_path.is_file():
        return dev_path

    return None


def load_openapi_spec() -> dict[str, Any]:
    json_path = resolve_openapi_json_path()
    if json_path is None:
        return {}
    with json_path.open(encoding="utf-8") as handle:
        loaded: dict[str, Any] = json.load(handle)
        return loaded


def normalize_path(path: str) -> str:
    cleaned = path.strip()
    if not cleaned.startswith("/"):
        cleaned = f"/{cleaned}"
    if cleaned.startswith("/openapi/"):
        cleaned = cleaned[len("/openapi") :]
    return cleaned
