# Maintainer guide — regenerating `spec/json/` and releasing

This document is for **maintainers** who update the machine-readable Saxo OpenAPI database and publish packages. End users do not need these steps.

## Overview

```text
Saxo Developer Portal (HTML)
        │
        ▼
flat_doc_generator/crawler.py   ← private dev workspace only
        │
        ▼
flat_doc_generator/output/json/
        │
        ▼
scripts/sync_saxo_agent_brain_spec.py
        │
        ▼
mcp-server-saxo-openapi/spec/json/          ← maintainer SoT
        │
        ▼  (required before build/publish)
src/saxo_doc_helper/data/json/              ← wheel package data
```

The crawler and sync script live in the private integration workspace (`saxso_option_trader_claude`), not in this public package.

## Prerequisites

- Python 3.14+ with `uv` in the parent workspace (for crawler/sync)
- A local clone of this repository (often at `docs/mcp-server-saxo-openapi/` inside the parent workspace)

## Step 1: Regenerate JSON from Saxo portal

From the parent workspace root:

```bash
cd docs/flat_doc_generator
# Run the crawler per flat_doc_generator/README.md
uv run python generator/crawler.py
```

Output lands in `docs/flat_doc_generator/output/json/`.

## Step 2: Sync into this repository

From the parent workspace root:

```bash
uv run python scripts/sync_saxo_agent_brain_spec.py --summary
```

Review the summary (`+new`, `~updated`, `=unchanged`).

## Step 3: Sync package data (required before release)

```bash
cd docs/mcp-server-saxo-openapi
rm -rf src/saxo_doc_helper/data/json
cp -a spec/json src/saxo_doc_helper/data/json
```

`spec/json/` and `src/saxo_doc_helper/data/json/` must match before `uv build` / publish.

## Step 4: Verify helper and tests

```bash
cd docs/mcp-server-saxo-openapi
uv sync
uv run python -m unittest discover -s tests -v
uv run saxo-doc-helper search-endpoints orders
```

## Step 5: Local wheel / uvx check

```bash
rm -rf dist
uv build
uvx --from ./dist/mcp_server_saxo_openapi-*.whl saxo-doc-helper search-endpoints orders
```

## Step 6: Commit in this repository

```bash
cd docs/mcp-server-saxo-openapi
git add spec/json/ src/saxo_doc_helper/data/json/
git commit -m "chore: refresh spec JSON from Saxo portal"
```

## Publishing

### TestPyPI (current Phase C gate)

Requires `~/.pypirc` with a `[testpypi]` token section.

```bash
rm -rf dist
uv build
uv publish --publish-url https://test.pypi.org/legacy/
```

Verify:

```bash
uvx --index-url https://test.pypi.org/simple/ \
    --index https://pypi.org/simple/ \
    saxo-doc-helper search-endpoints orders
```

### Production PyPI (next gate)

Accounts and `[pypi]` in `~/.pypirc` may already be ready. Do **not** run until TestPyPI verification is accepted:

```bash
uv publish
# or: twine upload dist/*
```

Same version cannot be re-uploaded; bump `version` in `pyproject.toml` if needed.

## Notes

- Legacy flat files `orders.json` and `orders_recursive.json` at the crawler output root are excluded from sync.
- Do not commit `__pycache__/`, `.venv/`, or `dist/` unless intentional.
- Override spec location at runtime with `SAXO_OPENAPI_SPEC_DIR` if needed.
