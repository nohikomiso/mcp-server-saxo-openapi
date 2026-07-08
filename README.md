# saxo-openapi-agent-brain

English | [日本語](./README.ja.md)

---

![License](https://img.shields.io/badge/license-MIT-green.svg)
![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![AI-First](https://img.shields.io/badge/AI--First-Optimized-success.svg)
![MCP](https://img.shields.io/badge/MCP-stdio-orange.svg)

**Agent-first specification engine for Saxo Bank OpenAPI.**

Machine-readable JSON specs plus a CLI/MCP helper — built for AI coding agents, not human readers.

---

## What is this?

This repository is **not a human documentation site**. It is a structured knowledge base for AI agents (Claude, Gemini, GPT, Cursor, etc.) to:

- Look up any Saxo OpenAPI endpoint (parameters, types, nesting)
- Retrieve real request/response JSON samples
- Drill into nested schema objects on demand with minimal tokens

`spec/json/` covers **17 Saxo OpenAPI service groups** (~260 endpoints) with recursive schema resolution and embedded samples.

---

## Requirements

- **Python 3.10+** (3.11+ recommended)
- **No pip install** — `saxo_doc_helper.py` uses only the Python standard library

---

## Installation

```bash
git clone https://github.com/nohikomiso/saxo-openapi-agent-brain.git
cd saxo-openapi-agent-brain
python tools/saxo_doc_helper.py search-endpoints orders
```

If you already have a copy of this tree, `cd` into the repository root and use the same commands below.

---

## CLI quick start

```bash
# Search endpoints by keyword
python tools/saxo_doc_helper.py search-endpoints orders

# Top-level parameters + JSON samples
python tools/saxo_doc_helper.py get-endpoint POST /trade/v2/orders

# Drill into a nested schema from "[Refer to Schema: ...]" hints
python tools/saxo_doc_helper.py get-schema algorithmicorderdata

# Expand one level of nested parameters
python tools/saxo_doc_helper.py get-endpoint POST /trade/v2/orders --depth 1
```

### Input is AI-forgiving

The helper normalizes common agent mistakes:

| Input | Normalized |
|-------|------------|
| `post` | `POST` |
| `trade/v2/orders` | `/trade/v2/orders` |
| `https://gateway.saxobank.com/sim/openapi/trade/v2/orders` | `/trade/v2/orders` |

If no exact match is found, **Did you mean?** suggestions are returned.

---

## MCP server

Run as a stdio MCP server:

```bash
python tools/saxo_doc_helper.py --mcp
```

Example MCP client configuration (run from the repository root, or use absolute paths):

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

### Tools exposed

| Tool | Description |
|------|-------------|
| `search_saxo_endpoints(query)` | Keyword search across all endpoints |
| `get_saxo_endpoint_spec(method, path, depth?)` | Parameters + request/response samples |
| `get_saxo_schema_spec(schema_name, depth?)` | Nested schema drill-down |

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

Each JSON file under `spec/json/` lists endpoints with:

- `method`, `path`, `name`
- `parameters` — recursive tree (type, description, Body/Query/Path origin)
- `request_sample` / `response_sample`

---

## Agent integration

Add to your agent rules (`.cursor/rules/`, `AGENTS.md`, etc.):

> When researching Saxo OpenAPI specs, do **not** read `spec/json/` files directly.  
> Use `python tools/saxo_doc_helper.py` from this repository root with minimal token usage.

Example workflow:

```bash
python tools/saxo_doc_helper.py search-endpoints positions
python tools/saxo_doc_helper.py get-endpoint GET /port/v1/positions
```

---

## Related projects

| Project | Role |
|---------|------|
| [saxo-apy](https://github.com/nohikomiso/saxo-apy) | OAuth and session management |
| [saxo-openapi](https://github.com/nohikomiso/saxo-openapi) | Python REST/WebSocket client (AI-ready) |

This repository provides **spec lookup**; the libraries above provide **runtime API access**.

---

## Data source and freshness

- Spec JSON is derived from the public [Saxo Developer Portal](https://www.developer.saxo/openapi/referencedocs).
- This project is **unofficial** and not endorsed by Saxo Bank A/S.
- Check commit history (and future GitHub Releases) for when `spec/json/` was last refreshed.

To regenerate specs, maintainers follow [docs/MAINTAINER.md](docs/MAINTAINER.md). See also [CONTRIBUTING.md](CONTRIBUTING.md).

---

## Disclaimer

- **Unofficial**: Not affiliated with or endorsed by Saxo Bank A/S.
- **Educational use**: For agent-assisted development against publicly documented APIs.
- **No warranty**: Data may be incomplete or outdated. Verify against Saxo official documentation and live API responses before production use.
- **Trademarks**: Saxo Bank and related marks belong to their respective owners.

---

## License

[MIT License](LICENSE)
