# mcp-server-saxo-openapi

**Saxo Bank OpenAPI spec lookup — CLI tool and MCP server**

English | [日本語](https://github.com/nohikomiso/mcp-server-saxo-openapi/blob/main/README.ja.md)

---

![License](https://img.shields.io/badge/license-MIT-green.svg)
![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![CLI](https://img.shields.io/badge/CLI-saxo--doc--helper-blue.svg)
![MCP](https://img.shields.io/badge/MCP-stdio-orange.svg)
![Spec updated](https://img.shields.io/github/last-commit/nohikomiso/mcp-server-saxo-openapi/main?label=spec%20updated)

Look up **Saxo Bank** / **Saxobank** OpenAPI endpoint parameters and JSON samples from your terminal, or attach the same tools to Cursor, Claude Desktop, and other MCP clients — without wrestling the deep official reference tree.

Zero third-party dependencies (Python stdlib only). Spec database: ~260 endpoints across 17 service groups, shipped inside the wheel.

---

## Spec snapshot

**Spec snapshot: 2026-07-08** (Saxo Release Notes through **2025/05/15**).

Structured endpoint specs for agents and developers. Saxo does not publish a single docs semver; we record the crawl date and the newest Release Notes heading present at that time. Details: [SPEC_FRESHNESS.md](SPEC_FRESHNESS.md).

Missing endpoint, wrong parameter, or something that looks out of date? Please [open an Issue](https://github.com/nohikomiso/mcp-server-saxo-openapi/issues). Pull requests: [CONTRIBUTING.md](CONTRIBUTING.md).

---

## What this is / is not

| This package | Not this package |
|--------------|------------------|
| Offline **spec lookup** (CLI + MCP) | Live trading / portfolio API calls |
| No Saxo credentials required | OAuth, order placement, balances |
| Token-efficient progressive disclosure | A substitute for a full OpenAPI client |

For **live** Saxo OpenAPI access from an MCP client, see community servers such as [`@borgels/mcp-server-saxo`](https://www.npmjs.com/package/@borgels/mcp-server-saxo) (npm, unofficial, separate project).

**Unofficial** — not affiliated with or endorsed by Saxo Bank A/S.

---

## Features

- **Structured spec database** — nested parameters and request/response samples
- **CLI** — `search-endpoints`, `get-endpoint`, `get-schema` with depth control and "Did you mean?" suggestions
- **MCP server** — stdio JSON-RPC; same three tools
- **Token-efficient** — progressive disclosure (collapsed nested schemas, drill down on demand)

**Requirements:** Python 3.10+

---

## Getting started — recommended (uvx)

### Production PyPI

```bash
uvx mcp-server-saxo-openapi
uvx --from mcp-server-saxo-openapi saxo-doc-helper search-endpoints orders
uvx --from mcp-server-saxo-openapi saxo-doc-helper --version
```

`uvx` resolves the **package** name; use `--from mcp-server-saxo-openapi` to run the `saxo-doc-helper` console script.

MCP client config:

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

### From GitHub

```bash
uvx --from git+https://github.com/nohikomiso/mcp-server-saxo-openapi.git saxo-doc-helper search-endpoints orders
uvx --from git+https://github.com/nohikomiso/mcp-server-saxo-openapi.git mcp-server-saxo-openapi
```

### TestPyPI (development only)

```bash
uvx --index-url https://test.pypi.org/simple/ \
    --index https://pypi.org/simple/ \
    --from mcp-server-saxo-openapi \
    saxo-doc-helper search-endpoints orders
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
uv run saxo-doc-helper --version
uv run saxo-doc-helper search-endpoints orders
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
├── SPEC_FRESHNESS.md
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
| [@borgels/mcp-server-saxo](https://www.npmjs.com/package/@borgels/mcp-server-saxo) | Live Saxo OpenAPI MCP (npm; unofficial) |

This repository provides **spec lookup**. Runtime API access is a separate concern.

---

## Feedback and maintainers

- Bugs / stale specs: [GitHub Issues](https://github.com/nohikomiso/mcp-server-saxo-openapi/issues)
- Maintainers: [docs/MAINTAINER.md](docs/MAINTAINER.md)
- Source crawl: public Saxo Developer Portal reference docs

---

## License

[MIT License](LICENSE)
