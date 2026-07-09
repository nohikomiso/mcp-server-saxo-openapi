"""CLI and MCP entry points."""

from __future__ import annotations

import argparse
import sys

from saxo_doc_helper import (
    SAXO_RELEASE_NOTES_THROUGH,
    SPEC_SNAPSHOT_DATE,
    __version__,
)
from saxo_doc_helper.commands import cmd_get_endpoint, cmd_get_schema, cmd_search_endpoints
from saxo_doc_helper.index import SaxoDocIndex, resolve_spec_dir
from saxo_doc_helper.mcp_server import run_mcp_server


def version_string() -> str:
    return (
        f"mcp-server-saxo-openapi {__version__} "
        f"(spec snapshot {SPEC_SNAPSHOT_DATE}; "
        f"saxo RN through {SAXO_RELEASE_NOTES_THROUGH})"
    )


def mcp_main() -> None:
    """Entry point for ``mcp-server-saxo-openapi`` (stdio MCP only)."""
    index = SaxoDocIndex(resolve_spec_dir())
    run_mcp_server(index)


def main(argv: list[str] | None = None) -> None:
    """Entry point for ``saxo-doc-helper`` and ``python -m saxo_doc_helper``."""
    parser = argparse.ArgumentParser(
        description="Saxo OpenAPI spec lookup — CLI & MCP helper",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  saxo-doc-helper search-endpoints orders
  saxo-doc-helper get-endpoint POST /trade/v2/orders
  saxo-doc-helper get-endpoint post trade/v2/orders --depth 1
  saxo-doc-helper get-schema algorithmicorderdata
  saxo-doc-helper --mcp
  mcp-server-saxo-openapi
        """,
    )
    parser.add_argument(
        "--version",
        action="version",
        version=version_string(),
    )
    parser.add_argument("--mcp", action="store_true", help="Run as MCP stdio server")
    parser.add_argument(
        "command",
        nargs="?",
        choices=["search-endpoints", "get-endpoint", "get-schema"],
        help="CLI command to run",
    )
    parser.add_argument("args", nargs=argparse.REMAINDER, help="Command arguments")

    parsed = parser.parse_args(argv)
    index = SaxoDocIndex(resolve_spec_dir())

    if parsed.mcp:
        run_mcp_server(index)
        return

    if not parsed.command:
        parser.print_help()
        sys.exit(1)

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
