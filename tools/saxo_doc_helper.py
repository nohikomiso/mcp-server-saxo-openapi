#!/usr/bin/env python3
"""
saxo_doc_helper.py
------------------
AI-first CLI & MCP hybrid tool for querying Saxo OpenAPI spec JSON database.

Usage (CLI):
    python saxo_doc_helper.py search-endpoints <query>
    python saxo_doc_helper.py get-endpoint <METHOD> <path> [--depth N]
    python saxo_doc_helper.py get-schema <schema_name> [--depth N]

Usage (MCP server via stdio JSON-RPC):
    python saxo_doc_helper.py --mcp
"""

import os
import sys
import json
import argparse

# ---------------------------------------------------------------------------
# Path configuration
# The spec/json directory is relative to THIS file's location
# ---------------------------------------------------------------------------
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SPEC_DIR = os.path.join(SCRIPT_DIR, "..", "spec", "json")


# ---------------------------------------------------------------------------
# Input normalizer (AI-UX: absorb common input variations)
# ---------------------------------------------------------------------------
def normalize_method(method: str) -> str:
    """Normalize HTTP method to uppercase."""
    return method.strip().upper()


def normalize_path(path: str) -> str:
    """Normalize API path: ensure leading slash, strip trailing slashes and whitespace."""
    path = path.strip()
    # Remove common prefixes that AI agents may accidentally include
    for prefix in [
        "https://gateway.saxobank.com/sim/openapi",
        "https://gateway.saxobank.com/openapi",
        "/sim/openapi",
        "/openapi",
    ]:
        if path.startswith(prefix):
            path = path[len(prefix):]
    # Ensure leading slash
    if not path.startswith("/"):
        path = "/" + path
    # Remove trailing slash
    path = path.rstrip("/")
    return path


def normalize_schema_name(name: str) -> str:
    """Normalize schema name to lowercase, strip whitespace."""
    return name.strip().lower()


# ---------------------------------------------------------------------------
# Index builder
# ---------------------------------------------------------------------------
class SaxoDocIndex:
    def __init__(self, spec_dir: str):
        self.spec_dir = spec_dir
        self.endpoints: list[dict] = []
        self.schemas: dict[str, dict] = {}
        self._load()

    def _load(self):
        """Walk spec/json and index all endpoints and schemas into memory."""
        if not os.path.isdir(self.spec_dir):
            print(
                f"ERROR: spec directory not found: {self.spec_dir}",
                file=sys.stderr,
            )
            return

        for root, _dirs, files in os.walk(self.spec_dir):
            for fname in sorted(files):
                if not fname.endswith(".json"):
                    continue
                fpath = os.path.join(root, fname)
                try:
                    with open(fpath, encoding="utf-8") as f:
                        data = json.load(f)
                except Exception as e:
                    print(f"WARN: Could not load {fpath}: {e}", file=sys.stderr)
                    continue

                if not isinstance(data, dict) or "endpoints" not in data:
                    continue

                service = data.get("service", "")
                category = data.get("category", "")
                for ep in data["endpoints"]:
                    self.endpoints.append(
                        {
                            "service": service,
                            "category": category,
                            "name": ep.get("name", ""),
                            "method": ep.get("method", ""),
                            "path": ep.get("path", ""),
                            "url": ep.get("url", ""),
                            "parameters": ep.get("parameters", []),
                            "request_sample": ep.get("request_sample"),
                            "response_sample": ep.get("response_sample"),
                        }
                    )
                    self._extract_schemas(ep.get("parameters", []))

    def _extract_schemas(self, params: list):
        for p in params:
            link = p.get("link") or ""
            if "/schema-" in link:
                key = normalize_schema_name(link.split("/schema-")[-1])
                if key not in self.schemas and p.get("children"):
                    self.schemas[key] = {
                        "type_name": p.get("type", ""),
                        "description": p.get("description", ""),
                        "parameters": p.get("children", []),
                    }
            self._extract_schemas(p.get("children", []))


# ---------------------------------------------------------------------------
# Formatter helpers
# ---------------------------------------------------------------------------
def _format_params(params: list, depth: int = 0, max_depth: int = 0) -> list[str]:
    lines = []
    for p in params:
        indent = "  " * depth
        origin = f" ({p['origin']})" if p.get("origin") else ""
        line = f"{indent}- **{p['name']}** (`{p['type']}`){origin}: {p.get('description', '')}"
        lines.append(line)

        children = p.get("children", [])
        if children:
            link = p.get("link") or ""
            schema_key = normalize_schema_name(link.split("/schema-")[-1]) if "/schema-" in link else ""
            if depth < max_depth:
                lines.extend(_format_params(children, depth + 1, max_depth))
            else:
                hint = f" [Refer to Schema: {schema_key}]" if schema_key else ""
                lines.append(f"{indent}  * (Nested parameters collapsed.{hint})")
    return lines


def _render_json_sample(sample, label: str) -> str:
    if sample is None:
        return ""
    if isinstance(sample, (dict, list)):
        body = json.dumps(sample, indent=2, ensure_ascii=False)
    else:
        body = str(sample)
    return f"\n{label}:\n{body}"


# ---------------------------------------------------------------------------
# Command implementations
# ---------------------------------------------------------------------------
def cmd_search_endpoints(index: SaxoDocIndex, query: str) -> str:
    q = query.lower()
    results = [
        ep
        for ep in index.endpoints
        if q in ep["path"].lower()
        or q in ep["name"].lower()
        or q in ep["service"].lower()
        or q in ep["category"].lower()
    ]
    if not results:
        return f"No endpoints found matching '{query}'."
    lines = [f"Found {len(results)} endpoint(s) matching '{query}':\n"]
    for ep in results:
        lines.append(f"  [{ep['service']}/{ep['category']}] {ep['method']} {ep['path']} -> {ep['name']}")
    return "\n".join(lines)


def cmd_get_endpoint(index: SaxoDocIndex, method: str, path: str, depth: int = 0) -> str:
    method = normalize_method(method)
    path = normalize_path(path)

    # Exact match
    match = next(
        (ep for ep in index.endpoints if ep["method"] == method and ep["path"] == path),
        None,
    )

    if match is None:
        # Did-you-mean: find candidates sharing path or method
        candidates = [
            ep
            for ep in index.endpoints
            if (path.rstrip("s") in ep["path"] or path in ep["path"])
        ]
        lines = [f'Error: Endpoint "{method} {path}" not found.']
        if candidates:
            lines.append("\nDid you mean one of these?")
            for c in candidates[:5]:
                lines.append(f"  - {c['method']} {c['path']}  ({c['name']})")
        return "\n".join(lines)

    param_lines = _format_params(match["parameters"], max_depth=depth)
    out = [
        f"Name: {match['name']}",
        f"Path: {match['method']} {match['path']}",
        f"URL:  {match['url']}",
        "",
        "Parameters:",
    ]
    out.extend(param_lines if param_lines else ["  (no parameters)"])
    out.append(_render_json_sample(match["request_sample"], "Request Sample"))
    out.append(_render_json_sample(match["response_sample"], "Response Sample"))
    return "\n".join(out).strip()


def cmd_get_schema(index: SaxoDocIndex, schema_name: str, depth: int = 0) -> str:
    key = normalize_schema_name(schema_name)
    # Also try without common prefixes/suffixes
    schema = index.schemas.get(key)
    if schema is None:
        # Fuzzy: find keys containing the query
        candidates = [k for k in index.schemas if key in k or k in key]
        if candidates:
            schema = index.schemas[candidates[0]]
            key = candidates[0]
        else:
            available = sorted(index.schemas.keys())[:10]
            return (
                f'Error: Schema "{schema_name}" not found.\n'
                f"Available schemas (first 10): {available}"
            )

    param_lines = _format_params(schema["parameters"], max_depth=depth)
    out = [
        f"Schema: {schema['type_name']} (key: {key})",
        f"Description: {schema['description']}",
        "",
        "Parameters:",
    ]
    out.extend(param_lines if param_lines else ["  (no parameters)"])
    return "\n".join(out)


# ---------------------------------------------------------------------------
# MCP server (stdio JSON-RPC 2.0)
# ---------------------------------------------------------------------------
MCP_TOOLS = [
    {
        "name": "search_saxo_endpoints",
        "description": (
            "Search Saxo OpenAPI endpoints by keyword. "
            "Returns a list of matching endpoints with method, path, and description."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Keyword to search (e.g. 'orders', 'positions', 'trade')",
                }
            },
            "required": ["query"],
        },
    },
    {
        "name": "get_saxo_endpoint_spec",
        "description": (
            "Get the parameter specification and JSON samples for a specific Saxo API endpoint. "
            "Input is normalized (case-insensitive method, leading slash auto-added). "
            "If not found exactly, suggestions will be returned."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "method": {"type": "string", "description": "HTTP method (GET/POST/PATCH/DELETE/PUT)"},
                "path": {"type": "string", "description": "API path, e.g. /trade/v2/orders"},
                "depth": {
                    "type": "integer",
                    "description": "How many levels of nested parameters to expand. Default 0 (top-level only).",
                    "default": 0,
                },
            },
            "required": ["method", "path"],
        },
    },
    {
        "name": "get_saxo_schema_spec",
        "description": (
            "Get the parameter details of a nested schema object referenced in an endpoint. "
            "Use the schema key shown in 'Refer to Schema: <key>' hints from get_saxo_endpoint_spec."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "schema_name": {
                    "type": "string",
                    "description": "Schema key name (e.g. 'algorithmicorderdata')",
                },
                "depth": {
                    "type": "integer",
                    "description": "How many levels of nested parameters to expand. Default 0.",
                    "default": 0,
                },
            },
            "required": ["schema_name"],
        },
    },
]


def run_mcp_server(index: SaxoDocIndex):
    """Minimal stdio JSON-RPC 2.0 MCP server."""
    for raw_line in sys.stdin:
        raw_line = raw_line.strip()
        if not raw_line:
            continue
        try:
            req = json.loads(raw_line)
        except json.JSONDecodeError:
            continue

        req_id = req.get("id")
        method = req.get("method", "")

        def respond(result):
            print(json.dumps({"jsonrpc": "2.0", "id": req_id, "result": result}), flush=True)

        def error(msg):
            print(
                json.dumps({"jsonrpc": "2.0", "id": req_id, "error": {"code": -32600, "message": msg}}),
                flush=True,
            )

        if method == "initialize":
            respond({
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "saxo-openapi-agent-brain", "version": "1.0.0"},
            })
        elif method == "tools/list":
            respond({"tools": MCP_TOOLS})
        elif method == "tools/call":
            params = req.get("params", {})
            tool_name = params.get("name", "")
            args = params.get("arguments", {})
            if tool_name == "search_saxo_endpoints":
                result = cmd_search_endpoints(index, args.get("query", ""))
            elif tool_name == "get_saxo_endpoint_spec":
                result = cmd_get_endpoint(
                    index,
                    args.get("method", ""),
                    args.get("path", ""),
                    int(args.get("depth", 0)),
                )
            elif tool_name == "get_saxo_schema_spec":
                result = cmd_get_schema(
                    index,
                    args.get("schema_name", ""),
                    int(args.get("depth", 0)),
                )
            else:
                error(f"Unknown tool: {tool_name}")
                continue
            respond({"content": [{"type": "text", "text": result}]})
        elif method == "notifications/initialized":
            pass  # No-op acknowledgement
        else:
            error(f"Unknown method: {method}")


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(
        description="Saxo OpenAPI Agent Brain - CLI & MCP helper tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python saxo_doc_helper.py search-endpoints orders
  python saxo_doc_helper.py get-endpoint POST /trade/v2/orders
  python saxo_doc_helper.py get-endpoint post trade/v2/orders --depth 1
  python saxo_doc_helper.py get-schema algorithmicorderdata
  python saxo_doc_helper.py --mcp
        """,
    )
    parser.add_argument("--mcp", action="store_true", help="Run as MCP stdio server")
    parser.add_argument("command", nargs="?", choices=["search-endpoints", "get-endpoint", "get-schema"],
                        help="CLI command to run")
    parser.add_argument("args", nargs=argparse.REMAINDER, help="Command arguments")

    parsed = parser.parse_args()
    index = SaxoDocIndex(SPEC_DIR)

    if parsed.mcp:
        run_mcp_server(index)
        return

    if not parsed.command:
        parser.print_help()
        sys.exit(1)

    # Sub-parse per command
    if parsed.command == "search-endpoints":
        if not parsed.args:
            print("Usage: search-endpoints <query>")
            sys.exit(1)
        print(cmd_search_endpoints(index, " ".join(parsed.args)))

    elif parsed.command == "get-endpoint":
        sub = argparse.ArgumentParser()
        sub.add_argument("method")
        sub.add_argument("path")
        sub.add_argument("--depth", type=int, default=0)
        a = sub.parse_args(parsed.args)
        print(cmd_get_endpoint(index, a.method, a.path, a.depth))

    elif parsed.command == "get-schema":
        sub = argparse.ArgumentParser()
        sub.add_argument("schema_name")
        sub.add_argument("--depth", type=int, default=0)
        a = sub.parse_args(parsed.args)
        print(cmd_get_schema(index, a.schema_name, a.depth))


if __name__ == "__main__":
    main()
