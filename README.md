# saxo-openapi-agent-brain

**Saxo OpenAPI spec lookup — CLI tool and MCP server**

English | [日本語](./README.ja.md)

---

![License](https://img.shields.io/badge/license-MIT-green.svg)
![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![CLI](https://img.shields.io/badge/CLI-saxo__doc__helper-blue.svg)
![MCP](https://img.shields.io/badge/MCP-stdio-orange.svg)

Look up Saxo OpenAPI endpoint parameters and JSON samples from your terminal, or attach the same lookup tools to Cursor, Claude Desktop, and other MCP clients.

`saxo_doc_helper.py` is a zero-dependency Python script backed by `spec/json/` (~260 endpoints across 17 service groups).

---

## Features

- **Structured spec database** — `spec/json/` with nested parameters and request/response samples
- **CLI** — `search-endpoints`, `get-endpoint`, `get-schema` with depth control and "Did you mean?" suggestions
- **MCP server** — run with `--mcp`; exposes the same three tools over stdio JSON-RPC
- **Token-efficient** — progressive disclosure (collapsed nested schemas, drill down on demand)
- **For** — Saxo API integrators, AI coding agents, and developers who want the raw JSON spec

**Requirements:** Python 3.10+ (stdlib only — no `pip install` needed for the helper).

---

## Getting started — CLI

### 1. Clone

```bash
git clone https://github.com/nohikomiso/saxo-openapi-agent-brain.git
cd saxo-openapi-agent-brain
```

### 2. Try a lookup

```bash
python tools/saxo_doc_helper.py search-endpoints orders
```

### 3. Get an endpoint spec

```bash
python tools/saxo_doc_helper.py get-endpoint POST /trade/v2/orders
python tools/saxo_doc_helper.py get-schema algorithmicorderdata
```

### More CLI examples

```bash
# Expand one level of nested parameters
python tools/saxo_doc_helper.py get-endpoint POST /trade/v2/orders --depth 1
```

### Input normalization

| Input | Normalized |
|-------|------------|
| `post` | `POST` |
| `trade/v2/orders` | `/trade/v2/orders` |
| `https://gateway.saxobank.com/sim/openapi/trade/v2/orders` | `/trade/v2/orders` |

If no exact match is found, **Did you mean?** suggestions are returned.

### Full-scratch developers

You can also read `spec/json/` directly. The CLI is recommended because it returns only the slice you need and keeps token usage low.

---

## Getting started — MCP

Expose Saxo spec lookup to MCP clients (Cursor, Claude Desktop, etc.).

### Option 1: From a local clone (available now)

**Step 1.** Clone this repository (see CLI section above).

**Step 2.** Test the server:

```bash
python tools/saxo_doc_helper.py --mcp
```

**Step 3.** Add to your MCP client config:

```json
{
  "mcpServers": {
    "saxo-openapi-agent-brain": {
      "command": "python3",
      "args": ["tools/saxo_doc_helper.py", "--mcp"],
      "cwd": "/absolute/path/to/saxo-openapi-agent-brain"
    }
  }
}
```

Replace `cwd` with the path where you cloned this repository.

### Option 2: uvx (planned — not yet published)

After PyPI packaging, the target experience will be:

```bash
uvx mcp-server-saxo-openapi
```

This is **not available yet**. See the distribution roadmap in the parent development workspace (`docs/saxo-openapi-agent-brain-distribution-roadmap.md`) for plans.

### MCP tools exposed

| Tool | Description |
|------|-------------|
| `search_saxo_endpoints(query)` | Keyword search across all endpoints |
| `get_saxo_endpoint_spec(method, path, depth?)` | Parameters + request/response samples |
| `get_saxo_schema_spec(schema_name, depth?)` | Nested schema drill-down |

---

## Agent integration

Add to your agent rules (`.cursor/rules/`, `AGENTS.md`, etc.):

> When researching Saxo OpenAPI specs, do **not** read `spec/json/` files directly.  
> Use `python tools/saxo_doc_helper.py` from this repository root.

Example workflow:

```bash
python tools/saxo_doc_helper.py search-endpoints positions
python tools/saxo_doc_helper.py get-endpoint GET /port/v1/positions
```

---

## Repository layout

```text
saxo-openapi-agent-brain/
├── LICENSE
├── README.md / README.ja.md
├── CONTRIBUTING.md
├── docs/
│   └── MAINTAINER.md      # Spec regeneration (maintainers only)
├── spec/json/             # Machine-readable OpenAPI database
│   ├── trade/
│   ├── port/
│   └── ...                # 17 service groups
└── tools/
    ├── saxo_doc_helper.py
    └── test_saxo_doc_helper.py
```

Each JSON file under `spec/json/` lists endpoints with `method`, `path`, `name`, recursive `parameters`, and `request_sample` / `response_sample`.

---

## Related projects

| Project | Role |
|---------|------|
| [saxo-apy](https://github.com/nohikomiso/saxo-apy) | OAuth and session management |
| [saxo-openapi](https://github.com/nohikomiso/saxo-openapi) | Python REST/WebSocket client (AI-ready) |

This repository provides **spec lookup**. The libraries above provide **runtime API access**.

---

## Data source and disclaimer

- Spec JSON is derived from the public [Saxo Developer Portal](https://www.developer.saxo/openapi/referencedocs).
- **Unofficial** — not affiliated with or endorsed by Saxo Bank A/S.
- Data may be incomplete or outdated. Verify against official documentation and live API responses before production use.
- Check commit history for when `spec/json/` was last refreshed. Maintainers: [docs/MAINTAINER.md](docs/MAINTAINER.md).

---

## License

[MIT License](LICENSE)
