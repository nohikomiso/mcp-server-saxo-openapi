# Changelog

## 0.3.1 — 2026-07-10

### Fixed

- **PyPI README links:** `CHANGELOG.md` and `LICENSE` now use absolute GitHub URLs (PyPI does not host relative link targets).

### Added

- `Changelog` entry in `[project.urls]` on PyPI.

## 0.3.0 — 2026-07-10

### Fixed (regression from 0.2.0)

- **Restore `spec/json` lookup engine** (`SaxoDocIndex`) instead of single `saxo_openapi.json`.
- Nested parameters, schema drill-down, and request/response samples are back.

### Added

- `get_saxo_schema_spec` and `get_saxo_workflow_guide` tools restored.
- `depth` parameter on endpoint and schema lookups.
- `saxo-doc-helper` CLI entry point restored.
- CRITICAL WARNING moved to **top** of endpoint output for `/orders` and `/positions`.

### Maintained from 0.2.0

- `saxo://docs/pitfalls.md` resource.
- FastMCP-based MCP server.

### Removed

- `saxo_openapi.json` as primary lookup data (no longer bundled in wheel).

## 0.2.0 — 2026-07-10

- FastMCP server with pitfalls and warnings.
- **Regression:** used shallow single-file OpenAPI lookup instead of `spec/json`.

## 0.1.1 — 2026-07-09

- Initial PyPI release: stdlib MCP, `saxo-doc-helper` CLI, crawled spec JSON.
