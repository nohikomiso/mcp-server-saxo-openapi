from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from mcp_server_saxo_openapi.commands import (
    cmd_get_endpoint,
    cmd_get_schema,
    cmd_get_workflow_guide,
    cmd_search_endpoints,
)
from mcp_server_saxo_openapi.index import SaxoDocIndex, resolve_spec_dir
from mcp_server_saxo_openapi.pitfalls import PITFALLS_MD

mcp = FastMCP("SaxoOpenAPIReference")
_index = SaxoDocIndex(resolve_spec_dir())


@mcp.resource("saxo://docs/pitfalls.md")
def get_pitfalls() -> str:
    """Returns the Saxo Bank OpenAPI pitfalls and workarounds guide for AI agents."""
    return PITFALLS_MD


@mcp.tool()
def search_saxo_endpoints(query: str) -> str:
    """Search for Saxo Bank OpenAPI endpoints by keyword."""
    return cmd_search_endpoints(_index, query)


@mcp.tool()
def get_saxo_endpoint_spec(method: str, path: str, depth: int = 0) -> str:
    """Get parameter specs and JSON samples for a Saxo Bank OpenAPI endpoint."""
    return cmd_get_endpoint(_index, method, path, depth)


@mcp.tool()
def get_saxo_schema_spec(schema_name: str, depth: int = 0) -> str:
    """Get nested schema parameters referenced from endpoint specs."""
    return cmd_get_schema(_index, schema_name, depth)


@mcp.tool()
def get_saxo_workflow_guide(use_case: str) -> str:
    """Get workflow guidance for complex Saxo operations (close_position, if_done_oco)."""
    return cmd_get_workflow_guide(use_case)


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
