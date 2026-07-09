"""Minimal stdio JSON-RPC 2.0 MCP server (stdlib only)."""

from __future__ import annotations

import json
import sys

from saxo_doc_helper import __version__
from saxo_doc_helper.commands import cmd_get_endpoint, cmd_get_schema, cmd_search_endpoints
from saxo_doc_helper.index import SaxoDocIndex

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
                "method": {
                    "type": "string",
                    "description": "HTTP method (GET/POST/PATCH/DELETE/PUT)",
                },
                "path": {"type": "string", "description": "API path, e.g. /trade/v2/orders"},
                "depth": {
                    "type": "integer",
                    "description": (
                        "How many levels of nested parameters to expand. "
                        "Default 0 (top-level only)."
                    ),
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


def run_mcp_server(index: SaxoDocIndex) -> None:
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
                json.dumps(
                    {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32600, "message": msg}}
                ),
                flush=True,
            )

        if method == "initialize":
            respond(
                {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {"tools": {}},
                    "serverInfo": {
                        "name": "mcp-server-saxo-openapi",
                        "version": __version__,
                    },
                }
            )
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
            pass
        else:
            error(f"Unknown method: {method}")
