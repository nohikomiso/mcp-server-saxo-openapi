# Maintainer guide (0.2.0+)

For releasing **mcp-server-saxo-openapi** from this repository.

## Layout

| Path | Role |
|------|------|
| `src/mcp_server_saxo_openapi/server.py` | FastMCP server (tools + pitfalls resource) |
| `src/mcp_server_saxo_openapi/data/saxo_openapi.json` | Bundled OpenAPI spec (shipped in wheel) |
| `SPEC_FRESHNESS.md` | Snapshot date markers |

Spec JSON is generated in the parent monorepo via `tools/saxo_openapi_generator` and copied into `data/` before release.

## Before every release

1. Refresh `src/mcp_server_saxo_openapi/data/saxo_openapi.json` if specs changed.
2. Update `SPEC_FRESHNESS.md` and `src/mcp_server_saxo_openapi/__init__.py` (`SPEC_SNAPSHOT_DATE`).
3. Bump `version` in `pyproject.toml`.
4. Update `CHANGELOG.md`.

## Tests

```bash
uv sync
uv run python -m unittest discover -s tests -v
```

## Build

```bash
rm -rf dist
uv build
```

## Publish

### TestPyPI (optional)

```bash
uv publish --publish-url https://test.pypi.org/legacy/
```

### PyPI

```bash
uv publish
```

Then tag and create a GitHub Release matching the version.

```bash
git tag v0.2.0
git push origin v0.2.0
gh release create v0.2.0 --title "v0.2.0" --notes-file CHANGELOG.md
```
