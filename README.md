# mcp-server-saxo-openapi

**Saxo Bank OpenAPI spec lookup — CLI tool and MCP server**

English | [日本語](https://github.com/nohikomiso/mcp-server-saxo-openapi/blob/main/README.ja.md)

---

![License](https://img.shields.io/badge/license-MIT-green.svg)
![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![CLI](https://img.shields.io/badge/CLI-saxo--doc--helper-blue.svg)
![MCP](https://img.shields.io/badge/MCP-stdio-orange.svg)
![Spec updated](https://img.shields.io/github/last-commit/nohikomiso/mcp-server-saxo-openapi/main?label=spec%20updated)

Look up **Saxo Bank** / **Saxobank** OpenAPI endpoint parameters and JSON samples from your terminal, or from Cursor, Claude Desktop, and other MCP clients. Built because the official reference tree is deep and hard for AI tools (and humans) to navigate.

No third-party dependencies (Python standard library only). Spec data is JSON: ~260 endpoints across 17 service groups, shipped with the package.

**Requirements:** Python 3.10+

---

## What this is / is not

**Purpose:** Help AI agents (and developers) understand *how* to use Saxo OpenAPI — parameters and JSON samples extracted from the official reference, available via CLI and MCP.

**What it does**

- Search endpoints by keyword
- Look up parameters and sample JSON by method + path
- Open nested schemas step by step
- No Saxo login or API keys (does not call Saxo over the network)

**What it does not do**

- Call live Saxo APIs (orders, balances, positions, …)
- OAuth / token management
- Replace a full trading client

For live API access, use a separate library or tool. One community MCP example: [`@borgels/mcp-server-saxo`](https://www.npmjs.com/package/@borgels/mcp-server-saxo) (npm, unofficial, unrelated project).

**Unofficial** — not affiliated with or endorsed by Saxo Bank A/S.

---

## Usage

The easiest path is [uv](https://docs.astral.sh/uv/)’s `uvx` (run without a permanent install).

### Cursor / Claude Desktop (MCP)

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

### Terminal (CLI)

```bash
uvx --from mcp-server-saxo-openapi saxo-doc-helper search-endpoints orders
uvx --from mcp-server-saxo-openapi saxo-doc-helper get-endpoint POST /trade/v2/orders
uvx --from mcp-server-saxo-openapi saxo-doc-helper --version
```

The **package** name is `mcp-server-saxo-openapi`; the **CLI** command is `saxo-doc-helper`. Use `--from mcp-server-saxo-openapi` when running the CLI via `uvx`.

To start the MCP server only:

```bash
uvx mcp-server-saxo-openapi
```

---

## MCP tools

| Tool | Description |
|------|-------------|
| `search_saxo_endpoints(query)` | Keyword search across endpoints |
| `get_saxo_endpoint_spec(method, path, depth?)` | Parameters + sample JSON |
| `get_saxo_schema_spec(schema_name, depth?)` | Nested schema details |

The CLI exposes the same content (`search-endpoints` / `get-endpoint` / `get-schema`).

---

## Spec snapshot

**Snapshot date: 2026-07-08** (newest Saxo Release Notes heading at that time: **2025/05/15**).

Saxo does not publish a single docs version number, so we record the crawl date and the newest Release Notes heading on the portal. Details: [SPEC_FRESHNESS.md](SPEC_FRESHNESS.md).

Missing endpoint, wrong parameter, or something that looks stale? Please [open an Issue](https://github.com/nohikomiso/mcp-server-saxo-openapi/issues).

---

## Related projects

This repo is for **reading specs**. Calling the API is a separate concern:

| Project | Role |
|---------|------|
| [saxo-apy](https://github.com/nohikomiso/saxo-apy) | OAuth / session (author’s other repo) |
| [saxo-openapi](https://github.com/nohikomiso/saxo-openapi) | REST / WebSocket client (author’s other repo) |
| [@borgels/mcp-server-saxo](https://www.npmjs.com/package/@borgels/mcp-server-saxo) | Live API via MCP (community; unofficial; different author) |

---

## Feedback & development

- Bugs / stale specs: [GitHub Issues](https://github.com/nohikomiso/mcp-server-saxo-openapi/issues)
- Contributing (clone, tests): [CONTRIBUTING.md](CONTRIBUTING.md)
- Spec refresh & release (maintainers): [docs/MAINTAINER.md](docs/MAINTAINER.md)

---

## License

[MIT License](LICENSE)
