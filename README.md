# Saxo Bank OpenAPI MCP Server

A specialized [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) server acting as a **reference manual and knowledge base** for the Saxo Bank OpenAPI.

**Version:** 0.3.1 · **Spec snapshot:** 2026-07-08

## Purpose

This server is **not an execution client**. It does NOT execute trades, place orders, or modify portfolios.

It helps AI agents generate Saxo Bank API code by combining:

1. **Rich endpoint specs** from crawled `spec/json` (nested parameters, request/response samples).
2. **Critical warnings** on dangerous endpoints (`/orders`, `/positions`).
3. **`saxo://docs/pitfalls.md`** — survival guide for Saxo-specific quirks.

## Tools

| Tool | Description |
|------|-------------|
| `search_saxo_endpoints(query)` | Discover endpoints by keyword. |
| `get_saxo_endpoint_spec(method, path, depth?)` | Parameters, samples, warnings. |
| `get_saxo_schema_spec(schema_name, depth?)` | Drill into nested schemas. |
| `get_saxo_workflow_guide(use_case)` | `close_position` or `if_done_oco` workflows. |

## Resources

| URI | Description |
|-----|-------------|
| `saxo://docs/pitfalls.md` | Netting, Stop/StopIfTraded, IsForceOpen, UIC, Precheck. |

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

### CLI fallback

```bash
uvx --from mcp-server-saxo-openapi saxo-doc-helper search-endpoints orders
uvx --from mcp-server-saxo-openapi saxo-doc-helper get-endpoint POST /trade/v2/orders --depth 1
```

## What changed in 0.3.0

0.2.0 mistakenly used a single `saxo_openapi.json` for lookup (shallow schemas). **0.3.0 restores the rich `spec/json` index** while keeping pitfalls and warnings from 0.2.0.

See [CHANGELOG.md](https://github.com/nohikomiso/mcp-server-saxo-openapi/blob/main/CHANGELOG.md).

## Known limitations

- Warnings are advisory; agents may skip `pitfalls.md`.
- `response_parameters` trees are sparse in some crawled specs; `response_sample` JSON is more reliable.
- Pitfalls reflect practical experience; not a substitute for Saxo's official docs.

## License

MIT — see [LICENSE](https://github.com/nohikomiso/mcp-server-saxo-openapi/blob/main/LICENSE).
