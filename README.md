# saxo-openapi-agent-brain

**Agent-First specification engine for Saxo Bank OpenAPI.**  
Machine-readable JSON specs + CLI/MCP tool — built for AI coding agents, not human readers.

---

## What is this?

This repository is **not a documentation site for humans**. It is a structured knowledge base designed to be consumed by AI coding agents (Claude, Gemini, GPT, Cursor, etc.) to:

- Instantly look up any Saxo OpenAPI endpoint spec (parameters, types, nesting)
- Get real request/response JSON examples for any endpoint
- Drill down into nested schema objects on demand

The JSON specs under `spec/json/` cover **all 17 Saxo OpenAPI service groups** (~260 endpoints total), with full recursive schema resolution and real request/response samples embedded.

---

## Quick Start (CLI)

No install required — just Python 3.x standard library.

```bash
# Search endpoints by keyword
python tools/saxo_doc_helper.py search-endpoints orders

# Get top-level parameters + JSON samples for a specific endpoint
python tools/saxo_doc_helper.py get-endpoint POST /trade/v2/orders

# Drill into a nested schema object referenced in the output above
python tools/saxo_doc_helper.py get-schema algorithmicorderdata

# Expand nested parameters (depth=1 shows one level of children)
python tools/saxo_doc_helper.py get-endpoint POST /trade/v2/orders --depth 1
```

### Input is AI-forgiving

The tool auto-normalizes common AI agent mistakes:
- Method case: `post` → `POST`
- Missing slash: `trade/v2/orders` → `/trade/v2/orders`
- Full URL: `https://gateway.saxobank.com/sim/openapi/trade/v2/orders` → `/trade/v2/orders`

If an exact match isn't found, `Did you mean?` suggestions are returned.

---

## MCP Server (for Claude Desktop / Cursor / any MCP client)

```bash
python tools/saxo_doc_helper.py --mcp
```

Add to your MCP client config:
```json
{
  "mcpServers": {
    "saxo-openapi-agent-brain": {
      "command": "python",
      "args": ["/path/to/docs/saxo-openapi-agent-brain/tools/saxo_doc_helper.py", "--mcp"]
    }
  }
}
```

Tools exposed:
- `search_saxo_endpoints(query)` — search by keyword
- `get_saxo_endpoint_spec(method, path, depth?)` — get parameters + samples
- `get_saxo_schema_spec(schema_name, depth?)` — drill into nested schemas

---

## Spec Structure

```
spec/json/
├── trade/
│   ├── orders.json       # POST/PATCH/DELETE /trade/v2/orders (with samples)
│   ├── prices.json
│   └── ...
├── port/
│   ├── balances.json
│   ├── positions.json
│   └── ...
├── hist/
├── ref/
└── ... (17 service groups total)
```

Each JSON file contains an array of endpoints with:
- `method`, `path`, `name`
- `parameters` — full recursive tree with type, description, origin (Body/Query/Path)
- `request_sample` / `response_sample` — real JSON objects from official docs

---

## Agent Usage Recommendation

Add this instruction to your agent rules (`.cursor/rules/`, `AGENTS.md`, etc.):

> When researching Saxo OpenAPI specs, do NOT read JSON files directly.  
> Use `python docs/saxo-openapi-agent-brain/tools/saxo_doc_helper.py` to query specs with minimal token usage.

---

## Data Source & Updates

Specs are auto-generated from the official [Saxo Developer Portal](https://www.developer.saxo/openapi/referencedocs) using the crawler in the parent repository. Updates are detected via MD5 hash of release notes pages.
