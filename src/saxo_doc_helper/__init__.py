"""Saxo OpenAPI spec lookup — CLI and MCP server."""

__version__ = "0.1.0"

from saxo_doc_helper.index import (
    SaxoDocIndex,
    normalize_method,
    normalize_path,
    normalize_schema_name,
    resolve_spec_dir,
)
from saxo_doc_helper.commands import (
    cmd_get_endpoint,
    cmd_get_schema,
    cmd_search_endpoints,
)

__all__ = [
    "SaxoDocIndex",
    "__version__",
    "cmd_get_endpoint",
    "cmd_get_schema",
    "cmd_search_endpoints",
    "normalize_method",
    "normalize_path",
    "normalize_schema_name",
    "resolve_spec_dir",
]
