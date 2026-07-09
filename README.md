# Saxo Bank OpenAPI MCP Server

A specialized [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) server acting as a **reference manual and knowledge base** for the Saxo Bank OpenAPI.

**Version:** 0.2.0 · **Spec snapshot:** 2026-07-08

## Purpose

This server is **not an execution client**. It does NOT execute trades, place orders, or modify portfolios.

Instead, it serves as an interactive **dictionary and strategy guide** for AI agents tasked with generating Saxo Bank API code.

Saxo's OpenAPI is complex: account netting modes, asset-class restrictions, and hedging workflows are easy to hallucinate. This MCP server helps by:

1. Providing accurate OpenAPI endpoint schemas on demand (request **and response** structure).
2. Injecting **critical warnings** when dangerous endpoints (like `/orders` or `/positions`) are queried.
3. Exposing `saxo://docs/pitfalls.md` — a survival guide for Saxo-specific quirks.

## Tools

| Tool | Description |
|------|-------------|
| `search_saxo_endpoints(keyword)` | Discover endpoints by keyword (path, summary, operationId). |
| `get_saxo_endpoint_spec(method, path)` | Parameters, request body, **responses**, and dynamic warnings. |

## Resources

| URI | Description |
|-----|-------------|
| `saxo://docs/pitfalls.md` | Netting modes, Stop vs StopIfTraded, IsForceOpen, UIC dedup, Precheck. |

## Usage (AI agents)

When writing Saxo Bank integration code:

1. Call `search_saxo_endpoints` to find the endpoint.
2. Call `get_saxo_endpoint_spec` to understand parameters and responses.
3. If warned, read `saxo://docs/pitfalls.md` before writing execution code.
4. Implement using your language's HTTP client or Saxo SDK — not via this MCP.

## Installation

### MCP (Cursor / Claude Desktop)

```json
{
  "mcpServers": {
    "saxo-openapi": {
      "command": "uvx",
      "args": ["mcp-server-saxo-openapi"]
    }
  }
}
```

### uvx (one-shot)

```bash
uvx mcp-server-saxo-openapi
```

### Local development

```bash
cd tools/mcp-server-saxo-openapi
uv sync
uv run mcp-server-saxo-openapi
```

Override spec file (optional):

```bash
export SAXO_OPENAPI_JSON_PATH=/path/to/saxo_openapi.json
```

## What it does / does not do

| Does | Does not |
|------|----------|
| Offline OpenAPI lookup | Call live Saxo APIs |
| Pitfalls & workflow warnings | OAuth / token management |
| Request + response schemas | Place or modify orders |

## Known limitations (0.2.0)

- Warnings are soft hints; agents may still skip `pitfalls.md`.
- No `get_saxo_schema_spec` or `get_saxo_workflow_guide` tools yet (feedback welcome via Issues).
- Pitfalls reflect practical experience; not a substitute for Saxo's official docs.
- Spec snapshot may lag Saxo Release Notes; see `SPEC_FRESHNESS.md`.

## Changes from 0.1.1

See [CHANGELOG.md](CHANGELOG.md). **0.2.0 replaces the stdlib implementation** with a FastMCP-based server that adds pitfalls, warnings, and response schemas.

## License

MIT — see [LICENSE](LICENSE).
