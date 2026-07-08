# Maintainer guide — regenerating `spec/json/`

This document is for **maintainers** who update the machine-readable Saxo OpenAPI database. End users of this repository do not need these steps.

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
saxo-openapi-agent-brain/spec/json/   ← this repository
```

The crawler and sync script live in the private integration workspace (`saxso_option_trader_claude`), not in this public package.

## Prerequisites

- Python 3.14+ with `uv` in the parent workspace
- Crawler dependencies installed in the parent workspace
- A local clone of this repository (often at `docs/saxo-openapi-agent-brain/` inside the parent workspace)

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

## Step 3: Verify helper and tests

```bash
cd docs/saxo-openapi-agent-brain
python tools/saxo_doc_helper.py search-endpoints orders
python tools/test_saxo_doc_helper.py -v
```

## Step 4: Commit in this repository

```bash
cd docs/saxo-openapi-agent-brain
git add spec/json/
git commit -m "chore: refresh spec JSON from Saxo portal"
```

Publish to GitHub only when the public repository is ready (see project release checklist).

## Notes

- Legacy flat files `orders.json` and `orders_recursive.json` at the output root are excluded from sync.
- Do not commit `__pycache__/` or local validation scratch files unless intentional.
