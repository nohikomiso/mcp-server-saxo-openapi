"""CLI entry point for saxo-doc-helper."""

from __future__ import annotations

import argparse
import sys

from mcp_server_saxo_openapi import (
    SAXO_RELEASE_NOTES_THROUGH,
    SPEC_SNAPSHOT_DATE,
    __version__,
)
from mcp_server_saxo_openapi.commands import (
    cmd_get_endpoint,
    cmd_get_schema,
    cmd_get_workflow_guide,
    cmd_search_endpoints,
)
from mcp_server_saxo_openapi.index import SaxoDocIndex, resolve_spec_dir


def version_string() -> str:
    return (
        f"mcp-server-saxo-openapi {__version__} "
        f"(spec snapshot {SPEC_SNAPSHOT_DATE}; saxo RN through {SAXO_RELEASE_NOTES_THROUGH})"
    )


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Saxo OpenAPI spec lookup CLI")
    parser.add_argument("--version", action="version", version=version_string())
    parser.add_argument(
        "command",
        nargs="?",
        choices=["search-endpoints", "get-endpoint", "get-schema", "workflow-guide"],
        help="CLI command to run",
    )
    parser.add_argument("args", nargs=argparse.REMAINDER, help="Command arguments")
    parsed = parser.parse_args(argv)

    if not parsed.command:
        parser.print_help()
        sys.exit(1)

    index = SaxoDocIndex(resolve_spec_dir())

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
        args = sub.parse_args(parsed.args)
        print(cmd_get_endpoint(index, args.method, args.path, args.depth))

    elif parsed.command == "get-schema":
        sub = argparse.ArgumentParser()
        sub.add_argument("schema_name")
        sub.add_argument("--depth", type=int, default=0)
        args = sub.parse_args(parsed.args)
        print(cmd_get_schema(index, args.schema_name, args.depth))

    elif parsed.command == "workflow-guide":
        if not parsed.args:
            print("Usage: workflow-guide <close_position|if_done_oco>")
            sys.exit(1)
        print(cmd_get_workflow_guide(parsed.args[0]))


if __name__ == "__main__":
    main()
