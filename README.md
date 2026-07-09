# mcp-server-saxo-openapi

**Saxo OpenAPI spec lookup — CLI tool and MCP server**

English | [日本語](./README.ja.md)

---

![License](https://img.shields.io/badge/license-MIT-green.svg)
![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![CLI](https://img.shields.io/badge/CLI-saxo--doc--helper-blue.svg)
![MCP](https://img.shields.io/badge/MCP-stdio-orange.svg)

Look up Saxo OpenAPI endpoint parameters and JSON samples from your terminal, or attach the same lookup tools to Cursor, Claude Desktop, and other MCP clients.

Zero third-party dependencies (Python stdlib only). Spec database: `spec/json/` (~260 endpoints across 17 service groups), also shipped inside the wheel.

---

## Features

- **Structured spec database** — nested parameters and request/response samples
- **CLI** — `search-endpoints`, `get-endpoint`, `get-schema` with depth control and "Did you mean?" suggestions
- **MCP server** — stdio JSON-RPC; same three tools
- **Token-efficient** — progressive disclosure (collapsed nested schemas, drill down on demand)

**Requirements:** Python 3.10+

---

## Getting started — recommended (uvx)

### CLI (TestPyPI — available now)

`uvx` resolves the **package** name; use `--from mcp-server-saxo-openapi` to run the `saxo-doc-helper` console script:

```bash
uvx --index-url https://test.pypi.org/simple/ \
    --index https://pypi.org/simple/ \
    --from mcp-server-saxo-openapi \
    saxo-doc-helper search-endpoints orders
```

```bash
uvx --index-url https://test.pypi.org/simple/ \
    --index https://pypi.org/simple/ \
    --from mcp-server-saxo-openapi \
    saxo-doc-helper get-endpoint POST /trade/v2/orders
```

### MCP (TestPyPI)

Package name matches the MCP entry point, so `--from` is optional:

```bash
uvx --index-url https://test.pypi.org/simple/ \
    --index https://pypi.org/simple/ \
    mcp-server-saxo-openapi
```

MCP client config example:

```json
{
  "mcpServers": {
    "saxo-openapi": {
      "command": "uvx",
      "args": [
        "--index-url", "https://test.pypi.org/simple/",
        "--index", "https://pypi.org/simple/",
        "mcp-server-saxo-openapi"
      ]
    }
  }
}
```

### From GitHub

```bash
uvx --from git+https://github.com/nohikomiso/mcp-server-saxo-openapi.git saxo-doc-helper search-endpoints orders
uvx --from git+https://github.com/nohikomiso/mcp-server-saxo-openapi.git mcp-server-saxo-openapi
```

### Production PyPI (next gate — not published yet)

After the production release:

```bash
uvx mcp-server-saxo-openapi
uvx --from mcp-server-saxo-openapi saxo-doc-helper search-endpoints orders
```

---

## Getting started — local clone

```bash
git clone https://github.com/nohikomiso/mcp-server-saxo-openapi.git
cd mcp-server-saxo-openapi
python tools/saxo_doc_helper.py search-endpoints orders
python tools/saxo_doc_helper.py get-endpoint POST /trade/v2/orders
python tools/saxo_doc_helper.py get-schema algorithmicorderdata
```

Or install editable:

```bash
uv sync
uv run saxo-doc-helper search-endpoints orders
uv run mcp-server-saxo-openapi
```

### Input normalization

| Input | Normalized |
|-------|------------|
| `post` | `POST` |
| `trade/v2/orders` | `/trade/v2/orders` |
| `https://gateway.saxobank.com/sim/openapi/trade/v2/orders` | `/trade/v2/orders` |

If no exact match is found, **Did you mean?** suggestions are returned.

---

## MCP tools exposed

| Tool | Description |
|------|-------------|
| `search_saxo_endpoints(query)` | Keyword search across all endpoints |
| `get_saxo_endpoint_spec(method, path, depth?)` | Parameters + request/response samples |
| `get_saxo_schema_spec(schema_name, depth?)` | Nested schema drill-down |

---

## Agent integration

> When researching Saxo OpenAPI specs, do **not** read `spec/json/` files directly.  
> Use `saxo-doc-helper` (or `python tools/saxo_doc_helper.py` from a clone).

---

## Repository layout

```text
mcp-server-saxo-openapi/
├── pyproject.toml
├── LICENSE
├── README.md / README.ja.md
├── CONTRIBUTING.md
├── docs/
│   └── MAINTAINER.md
├── src/saxo_doc_helper/   # installable package (+ data/json)
├── spec/json/             # maintainer source of truth
├── tests/
└── tools/
    └── saxo_doc_helper.py # thin clone-compatible wrapper
```

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
- Maintainers: [docs/MAINTAINER.md](docs/MAINTAINER.md).

---

## License

[MIT License](LICENSE)
