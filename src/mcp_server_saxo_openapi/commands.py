"""Command implementations for Saxo OpenAPI spec lookup."""

from __future__ import annotations

import json
from typing import Any

from mcp_server_saxo_openapi.index import (
    SaxoDocIndex,
    normalize_method,
    normalize_path,
    normalize_schema_name,
)
from mcp_server_saxo_openapi.pitfalls import CRITICAL_WARNING_HEADER


def _format_params(params: list, depth: int = 0, max_depth: int = 0) -> list[str]:
    lines: list[str] = []
    for param in params:
        indent = "  " * depth
        origin = f" ({param['origin']})" if param.get("origin") else ""
        line = (
            f"{indent}- **{param['name']}** (`{param['type']}`){origin}: "
            f"{param.get('description', '')}"
        )
        lines.append(line)

        children = param.get("children", [])
        if children:
            link = param.get("link") or ""
            schema_key = (
                normalize_schema_name(link.split("/schema-")[-1]) if "/schema-" in link else ""
            )
            if depth < max_depth:
                lines.extend(_format_params(children, depth + 1, max_depth))
            else:
                hint = f" [Refer to Schema: {schema_key}]" if schema_key else ""
                lines.append(f"{indent}  * (Nested parameters collapsed.{hint})")
    return lines


def _render_json_sample(sample: Any, label: str) -> str:
    if sample is None:
        return ""
    body = (
        json.dumps(sample, indent=2, ensure_ascii=False)
        if isinstance(sample, (dict, list))
        else str(sample)
    )
    return f"\n{label}:\n{body}"


def _needs_critical_warning(path: str) -> bool:
    path_lower = path.lower()
    return "/orders" in path_lower or "/positions" in path_lower


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
        candidates = [ep for ep in index.endpoints if path.rstrip("s") in ep["path"] or path in ep["path"]]
        lines = [f'Error: Endpoint "{method} {path}" not found.']
        if candidates:
            lines.append("\nDid you mean one of these?")
            for candidate in candidates[:5]:
                lines.append(f"  - {candidate['method']} {candidate['path']}  ({candidate['name']})")
        return "\n".join(lines)

    out: list[str] = []
    if _needs_critical_warning(path):
        out.extend([CRITICAL_WARNING_HEADER, ""])

    out.extend(
        [
            f"Name: {match['name']}",
            f"Path: {match['method']} {match['path']}",
            f"URL:  {match['url']}",
            "",
            "Request Parameters:",
        ]
    )
    param_lines = _format_params(match["parameters"], max_depth=depth)
    out.extend(param_lines if param_lines else ["  (no parameters)"])
    out.append("")
    out.append("Response Parameters:")
    response_param_lines = _format_params(match.get("response_parameters", []), max_depth=depth)
    out.extend(response_param_lines if response_param_lines else ["  (no response parameters)"])

    if "/orders" in path.lower() and method == "POST":
        out.append("\n" + "=" * 40)
        out.append("Saxo API Tips (Order Placement)")
        out.append("Depending on the 'OrderType', the required parameters change significantly:")
        out.append("- Market Order: 'OrderType'='Market', 'OrderPrice' is NOT used.")
        out.append("- Limit Order:  'OrderType'='Limit', 'OrderPrice' (Limit Price) is REQUIRED.")
        out.append("- Stop Order:   'OrderType'='Stop', 'TriggerPrice' is REQUIRED.")
        out.append(
            "- If-Done OCO:  Nest child orders in the 'Orders' list with "
            "'OrderRelation'='IfDone' or 'IfDoneOco'."
        )
        out.append("=" * 40)

    out.append(_render_json_sample(match["request_sample"], "Request Sample"))
    out.append(_render_json_sample(match["response_sample"], "Response Sample"))
    return "\n".join(out).strip()


def cmd_get_schema(index: SaxoDocIndex, schema_name: str, depth: int = 0) -> str:
    key = normalize_schema_name(schema_name)
    schema = index.schemas.get(key)
    if schema is None:
        candidates = [candidate for candidate in index.schemas if key in candidate or candidate in key]
        if candidates:
            key = candidates[0]
            schema = index.schemas[key]
        else:
            available = sorted(index.schemas.keys())[:10]
            return f'Error: Schema "{schema_name}" not found.\nAvailable schemas (first 10): {available}'

    param_lines = _format_params(schema["parameters"], max_depth=depth)
    out = [
        f"Schema: {schema['type_name']} (key: {key})",
        f"Description: {schema['description']}",
        "",
        "Parameters:",
    ]
    out.extend(param_lines if param_lines else ["  (no parameters)"])
    return "\n".join(out)


def cmd_get_workflow_guide(use_case: str) -> str:
    use_case = use_case.lower().strip()

    if use_case == "close_position":
        return (
            "Saxo Bank API Workflow: Close Position\n"
            'Saxo does not have a dedicated "/positions/close" endpoint. '
            "You must send a POST request to `/trade/v2/orders`.\n"
            "The parameters depend on the account's netting mode:\n\n"
            "A. Netting/FIFO Mode (Default)\n"
            "In FIFO mode, you close positions by simply placing a standard offsetting order.\n"
            '- OrderRelation: "StandAlone" (Standard new order)\n'
            '- BuySell: Must be the opposite of the current position (e.g. if Long, send "Sell").\n'
            "- Amount: The amount to close.\n"
            "- No PositionId is required. The system automatically closes the oldest open positions first.\n\n"
            "B. Hedging (NettingDisabled) Mode\n"
            "In Hedging mode, you must explicitly target a specific position ID to close it.\n"
            '- OrderRelation: Must be set to "ClosePosition"\n'
            "- PositionId or NetPositionId: REQUIRED.\n"
            "- BuySell: Must be the opposite of the targeted position.\n"
            "- Amount: The amount to close.\n"
            "- AssetType and Uic: Must match the targeted position.\n\n"
            "CRITICAL PITFALL: EndOfDayNetting (EODNetting) vs IntradayNetting\n"
            "Some demo accounts default to 'EndOfDay' netting mode.\n"
            "- EndOfDay Mode: Closed positions may STILL APPEAR during the day (zombie positions).\n"
            "- Intraday Mode: Closed positions disappear in real-time."
        )
    if use_case == "if_done_oco":
        return (
            "Saxo Bank API Workflow: If-Done / OCO (Take Profit & Stop Loss)\n"
            "Construct a single nested structure and POST to `/trade/v2/orders`.\n\n"
            "Structure:\n"
            '- Main Order: OrderType="Limit", OrderRelation="StandAlone"\n'
            "  - Orders (child orders):\n"
            '    - Take Profit: OrderType="Limit", OrderRelation="IfDone", OrderPrice=<TP>\n'
            '    - Stop Loss: OrderType="Stop", OrderRelation="IfDone", TriggerPrice=<SL>\n\n'
            "Notes:\n"
            '- Group TP and SL as OCO with OrderRelation="IfDoneOco".'
        )
    return f"Unknown use case '{use_case}'. Available: 'close_position', 'if_done_oco'."
