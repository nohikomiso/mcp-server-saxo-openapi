# Maintainer guide (this repository)

For people who release **mcp-server-saxo-openapi** from a clone of *this* public repository.

End users do not need this file. Spec JSON is generated elsewhere and committed into `spec/json/`; this guide covers packaging that data and publishing.

## What lives where

| Location | Role |
|----------|------|
| `spec/json/` | Source of truth for endpoint specs in this repo |
| `src/saxo_doc_helper/data/json/` | Copy shipped inside the installable package (must match `spec/json/` before build) |
| `SPEC_FRESHNESS.md` + `__init__.py` constants | Snapshot date and Saxo Release Notes heading shown to users |

Refreshing specs from the Saxo Developer Portal uses a **separate private toolchain** (not shipped here). If you only have this repo, update specs by reviewing PRs / Issues, or ask a maintainer who has that toolchain.

## Before every release

### 1. Refresh markers (when specs changed)

Update **both** so they stay in sync:

1. [`SPEC_FRESHNESS.md`](../SPEC_FRESHNESS.md) — `snapshot_date` and `saxo_release_notes_through`
2. `src/saxo_doc_helper/__init__.py` — `SPEC_SNAPSHOT_DATE` and `SAXO_RELEASE_NOTES_THROUGH`

Bump `version` in `pyproject.toml` (PyPI does not allow re-uploading the same version).

### 2. Copy specs into package data

From the repository root:

```bash
rm -rf src/saxo_doc_helper/data/json
cp -a spec/json src/saxo_doc_helper/data/json
```

### 3. Tests

```bash
uv sync
uv run python -m unittest discover -s tests -v
uv run saxo-doc-helper --version
uv run saxo-doc-helper search-endpoints orders
```

### 4. Local wheel check

```bash
rm -rf dist
uv build
uvx --from ./dist/mcp_server_saxo_openapi-*.whl saxo-doc-helper --version
```

### 5. Commit

```bash
git add spec/json/ src/saxo_doc_helper/data/json/ SPEC_FRESHNESS.md src/saxo_doc_helper/__init__.py pyproject.toml
git commit -m "chore: refresh spec JSON"
```

## Publishing

### TestPyPI

Requires `~/.pypirc` with a `[testpypi]` token.

```bash
rm -rf dist
uv build
uv publish --publish-url https://test.pypi.org/legacy/
```

### PyPI

```bash
uv publish
```

Then tag a GitHub Release matching the package version.

## Notes

- Override the spec directory at runtime with `SAXO_OPENAPI_SPEC_DIR` if needed.
- Do not commit `__pycache__/`, `.venv/`, or `dist/`.
