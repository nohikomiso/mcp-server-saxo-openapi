"""Spec index and path resolution for Saxo OpenAPI JSON database."""

from __future__ import annotations

import json
import os
import sys
from contextlib import ExitStack
from importlib import resources
from pathlib import Path

_RESOURCE_STACK: ExitStack | None = None
_PACKAGED_SPEC_DIR: str | None = None


def normalize_method(method: str) -> str:
    return method.strip().upper()


def normalize_path(path: str) -> str:
    path = path.strip()
    for prefix in (
        "https://gateway.saxobank.com/sim/openapi",
        "https://gateway.saxobank.com/openapi",
        "/sim/openapi",
        "/openapi",
    ):
        if path.startswith(prefix):
            path = path[len(prefix) :]
    if not path.startswith("/"):
        path = "/" + path
    return path.rstrip("/")


def normalize_schema_name(name: str) -> str:
    return name.strip().lower()


def _packaged_spec_dir() -> str | None:
    global _RESOURCE_STACK, _PACKAGED_SPEC_DIR
    if _PACKAGED_SPEC_DIR and os.path.isdir(_PACKAGED_SPEC_DIR):
        return _PACKAGED_SPEC_DIR
    try:
        data_root = resources.files("mcp_server_saxo_openapi").joinpath("data", "json")
    except (ModuleNotFoundError, TypeError, FileNotFoundError):
        return None
    if not data_root.is_dir():
        return None
    if _RESOURCE_STACK is None:
        _RESOURCE_STACK = ExitStack()
    path = _RESOURCE_STACK.enter_context(resources.as_file(data_root))
    _PACKAGED_SPEC_DIR = str(path)
    return _PACKAGED_SPEC_DIR


def resolve_spec_dir() -> str:
    env = os.environ.get("SAXO_OPENAPI_SPEC_DIR")
    if env:
        return os.path.abspath(env)

    packaged = _packaged_spec_dir()
    if packaged:
        return packaged

    here = Path(__file__).resolve()
    candidates = [
        here.parent / "data" / "json",
        here.parents[2] / "src" / "mcp_server_saxo_openapi" / "data" / "json",
        Path.cwd() / "spec" / "json",
    ]
    for cand in candidates:
        if cand.is_dir():
            return str(cand)

    return str(here.parent / "data" / "json")


class SaxoDocIndex:
    def __init__(self, spec_dir: str | None = None) -> None:
        self.spec_dir = spec_dir if spec_dir is not None else resolve_spec_dir()
        self.endpoints: list[dict] = []
        self.schemas: dict[str, dict] = {}
        self._load()

    def _load(self) -> None:
        if not os.path.isdir(self.spec_dir):
            print(f"ERROR: spec directory not found: {self.spec_dir}", file=sys.stderr)
            return

        for root, _dirs, files in os.walk(self.spec_dir):
            for fname in sorted(files):
                if not fname.endswith(".json"):
                    continue
                fpath = os.path.join(root, fname)
                try:
                    with open(fpath, encoding="utf-8") as handle:
                        data = json.load(handle)
                except Exception as exc:
                    print(f"WARN: Could not load {fpath}: {exc}", file=sys.stderr)
                    continue
                self._ingest_file(data)

    def _ingest_file(self, data: object) -> None:
        if not isinstance(data, dict) or "endpoints" not in data:
            return
        service = data.get("service", "")
        category = data.get("category", "")
        for ep in data["endpoints"]:
            self.endpoints.append(
                {
                    "service": service,
                    "category": category,
                    "name": ep.get("name", ""),
                    "method": ep.get("method", ""),
                    "path": ep.get("path", ""),
                    "url": ep.get("url", ""),
                    "parameters": ep.get("parameters", []),
                    "response_parameters": ep.get("response_parameters", []),
                    "request_sample": ep.get("request_sample"),
                    "response_sample": ep.get("response_sample"),
                }
            )
            self._extract_schemas(ep.get("parameters", []))
            self._extract_schemas(ep.get("response_parameters", []))

    def _extract_schemas(self, params: list) -> None:
        for param in params:
            link = param.get("link") or ""
            if "/schema-" in link:
                key = normalize_schema_name(link.split("/schema-")[-1])
                if key not in self.schemas and param.get("children"):
                    self.schemas[key] = {
                        "type_name": param.get("type", ""),
                        "description": param.get("description", ""),
                        "parameters": param.get("children", []),
                    }
            self._extract_schemas(param.get("children", []))
