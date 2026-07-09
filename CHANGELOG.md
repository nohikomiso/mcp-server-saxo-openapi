# Changelog

## 0.2.0 — 2026-07-10

### Added

- `saxo://docs/pitfalls.md` MCP resource (netting modes, Stop/StopIfTraded, IsForceOpen, UIC, Precheck).
- Dynamic **CRITICAL WARNING** when querying `/orders` or `/positions` endpoints.
- **Response schemas** in `get_saxo_endpoint_spec` output (missing in 0.1.1).
- Bundled `saxo_openapi.json` inside the wheel for PyPI/`uvx` installs.
- Path normalization (`/openapi/trade/...` → `/trade/...`).

### Changed

- **Breaking:** Replaced stdlib MCP + `saxo-doc-helper` CLI stack with FastMCP-based server.
- Entry point remains `mcp-server-saxo-openapi`; CLI subcommands from 0.1.1 are removed.
- Added runtime dependency on `mcp` package (0.1.1 had zero dependencies).

### Known limitations

- Warnings are advisory; agents may ignore them.
- Schema drill-down and workflow guide tools not included yet.

## 0.1.1 — 2026-07-09

- Initial PyPI release: stdlib MCP, `saxo-doc-helper` CLI, crawled spec JSON.
- No pitfalls resource, no response parameters in endpoint output.
