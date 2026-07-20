# Maintainer guide (0.3.0+)

## Layout

| Path | Role |
|------|------|
| `src/mcp_server_saxo_openapi/server.py` | FastMCP (4 tools + pitfalls resource) |
| `src/mcp_server_saxo_openapi/index.py` | `SaxoDocIndex` over `data/json` |
| `src/mcp_server_saxo_openapi/data/json/` | Bundled crawled spec (shipped in wheel) |

## Before every release

1. Sync spec from parent monorepo: `uv run python scripts/sync_saxo_agent_brain_spec.py`
2. Update `SPEC_FRESHNESS.md` and `__init__.py` snapshot constants.
3. Bump `version` in `pyproject.toml` and `CHANGELOG.md`.

## Tests

```bash
cd tools/mcp-server-saxo-openapi
uv sync
uv run python -m unittest discover -s tests -v
uv build
```

## Publish gate (TestPyPI first)

親 monorepo では Cursor スキル **`pypi-publish`**（`.cursor/skills/pypi-publish/SKILL.md`）とルール `70-pypi-publish.mdc` が正本。認証は `~/.pypirc` + `uvx twine`。

### 1. TestPyPI

```bash
uvx twine upload --repository testpypi dist/*
```

### 2. Verify from TestPyPI

```bash
uvx --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ \
  --from mcp-server-saxo-openapi==0.3.0 saxo-doc-helper --version
uvx --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ \
  --from mcp-server-saxo-openapi==0.3.0 saxo-doc-helper search-endpoints orders
```

GO checklist: search non-empty, samples + CRITICAL WARNING on orders, schema/workflow tools work.

### 3. Production PyPI (GO only)

```bash
uvx twine upload dist/*
git tag v0.3.0 && git push origin v0.3.0
gh release create v0.3.0 --title "v0.3.0" --notes-file CHANGELOG.md
```
