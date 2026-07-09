"""CLI command implementations for Saxo OpenAPI spec lookup."""

from __future__ import annotations

import json

from saxo_doc_helper.index import SaxoDocIndex, normalize_method, normalize_path, normalize_schema_name


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
            schema_key = (
                normalize_schema_name(link.split("/schema-")[-1]) if "/schema-" in link else ""
            )
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
        lines.append(
            f"  [{ep['service']}/{ep['category']}] {ep['method']} {ep['path']} -> {ep['name']}"
        )
    return "\n".join(lines)


def cmd_get_endpoint(index: SaxoDocIndex, method: str, path: str, depth: int = 0) -> str:
    method = normalize_method(method)
    path = normalize_path(path)

    match = next(
        (ep for ep in index.endpoints if ep["method"] == method and ep["path"] == path),
        None,
    )

    if match is None:
        candidates = [
            ep for ep in index.endpoints if (path.rstrip("s") in ep["path"] or path in ep["path"])
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
    schema = index.schemas.get(key)
    if schema is None:
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
