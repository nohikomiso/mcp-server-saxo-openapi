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

## Step 3: Update freshness markers (required before release)

After a successful crawl/sync, update **both**:

1. [`SPEC_FRESHNESS.md`](../SPEC_FRESHNESS.md) — `snapshot_date` (crawl day) and `saxo_release_notes_through` (newest Release Notes heading on the portal, e.g. `2025/05/15`)
2. `src/saxo_doc_helper/__init__.py` — `SPEC_SNAPSHOT_DATE` and `SAXO_RELEASE_NOTES_THROUGH` (must match)

Saxo does not publish a single OpenAPI docs semver; dated Release Notes are the portal’s change log. The private crawler’s `check_change_detection()` hashes Release Notes + Planned Changes pages to decide when to re-crawl.

Bump the **package** `version` in `pyproject.toml` when publishing refreshed data (PyPI forbids re-uploading the same version).

## Step 4: Sync package data (required before release)

```bash
cd docs/mcp-server-saxo-openapi
rm -rf src/saxo_doc_helper/data/json
cp -a spec/json src/saxo_doc_helper/data/json
```

`spec/json/` and `src/saxo_doc_helper/data/json/` must match before `uv build` / publish.

## Step 5: Verify helper and tests

```bash
cd docs/mcp-server-saxo-openapi
uv sync
uv run python -m unittest discover -s tests -v
uv run saxo-doc-helper --version
uv run saxo-doc-helper search-endpoints orders
```

## Step 6: Local wheel / uvx check

```bash
rm -rf dist
uv build
uvx --from ./dist/mcp_server_saxo_openapi-*.whl saxo-doc-helper --version
uvx --from ./dist/mcp_server_saxo_openapi-*.whl saxo-doc-helper search-endpoints orders
```

## Step 7: Commit in this repository

```bash
cd docs/mcp-server-saxo-openapi
git add spec/json/ src/saxo_doc_helper/data/json/ SPEC_FRESHNESS.md src/saxo_doc_helper/__init__.py
git commit -m "chore: refresh spec JSON from Saxo portal"
```

## Publishing

### TestPyPI

Requires `~/.pypirc` with a `[testpypi]` token section.

```bash
rm -rf dist
uv build
uv publish --publish-url https://test.pypi.org/legacy/
```

### Production PyPI

```bash
uv publish
# or: twine upload dist/*
```

Same version cannot be re-uploaded; bump `version` in `pyproject.toml` if needed.

## Notes

- Legacy flat files `orders.json` and `orders_recursive.json` at the crawler output root are excluded from sync.
- Do not commit `__pycache__/`, `.venv/`, or `dist/` unless intentional.
- Override spec location at runtime with `SAXO_OPENAPI_SPEC_DIR` if needed.
