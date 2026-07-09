#!/usr/bin/env python3
"""Thin compatibility wrapper for clone-based workflows.

Prefer installed entry points:
  saxo-doc-helper …
  mcp-server-saxo-openapi
"""

from __future__ import annotations

import sys
from pathlib import Path

# Allow running from a git clone without installing the package.
_SRC = Path(__file__).resolve().parents[1] / "src"
if _SRC.is_dir() and str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from saxo_doc_helper.cli import main  # noqa: E402

if __name__ == "__main__":
    main()
