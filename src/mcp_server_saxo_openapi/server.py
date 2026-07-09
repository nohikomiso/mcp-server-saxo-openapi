from __future__ import annotations

import json

from mcp.server.fastmcp import FastMCP

from mcp_server_saxo_openapi.spec_loader import load_openapi_spec, normalize_path

mcp = FastMCP("SaxoOpenAPIReference")

PITFALLS_MD = """# Saxo Bank OpenAPI Pitfalls & Workarounds

> **IMPORTANT:** This document describes critical behaviors and limitations of the Saxo Bank OpenAPI that are NOT officially documented or are easily misunderstood. AI Agents MUST read and follow these rules before writing any execution code.

## 1. Account Netting Modes (PositionNettingMode)
Before sending any orders, you must know the account's netting mode. Call `GET /port/v1/clients/me` and check `PositionNettingMode`.

*   **`Netting` (FIFO)**: Real-time netting. Sending an opposing order (e.g., selling an existing long position) will immediately close the position.
*   **`NettingDisabled` (Hedging)**: Hedging mode. Sending an opposing order will CREATE A NEW POSITION in the opposite direction. To close a specific position in this mode, you MUST include `PositionId` and set `OrderRelation="ClosePosition"` in your `POST /trade/v2/orders` request.
*   **`EndOfDay` (EOD)**: End-of-day netting. If you send a closing order, the realized profit/loss is calculated immediately upon execution, BUT the position will remain visible in `GET /port/v1/positions/me` until the end-of-day batch process. Do NOT attempt to close it again (double execution). Your code must tolerate "zombie positions" during the day.

## 2. Order Type Restrictions (`Stop` vs `StopIfTraded`)
Some instruments do not support standard `"Stop"` orders.
*   **Workaround**: You must query `GET /ref/v1/instruments/details` and check `SupportedOrderTypes`. If `"Stop"` is not listed, you must dynamically fallback to `"StopIfTraded"`.

## 3. Stock & StockOption Specific Parameters (`IsForceOpen`)
Including the `IsForceOpen` parameter in orders for `Stock` or `StockOption` instruments will result in an API error.
*   **Workaround**: Ensure `IsForceOpen` is completely removed from the request payload for these asset classes.

## 4. UIC Resolution (Duplicate Listings)
When searching for instruments by keyword (e.g., "AAPL"), the API will return multiple listings across different exchanges.
*   **Workaround**: Filter the search results using `Identifier == PrimaryListing` to find the main ("true") instrument Uic and avoid duplicates.

## 5. Mandatory Precheck
When operating in unverified environments or with new asset classes, your code MUST call `POST /trade/v2/orders/precheck` before sending the actual `POST /trade/v2/orders`. This validates the order parameters safely without execution.
"""


@mcp.resource("saxo://docs/pitfalls.md")
def get_pitfalls() -> str:
    """Returns the Saxo Bank OpenAPI pitfalls and workarounds guide for AI agents."""
    return PITFALLS_MD


def get_openapi_spec() -> dict:
    return load_openapi_spec()


@mcp.tool()
def search_saxo_endpoints(keyword: str) -> str:
    """
    Search for Saxo Bank OpenAPI endpoints by keyword.
    Returns a list of matching endpoints (method and path) with their summaries.
    """
    spec = get_openapi_spec()
    if not spec:
        return "Error: Could not load OpenAPI specification."

    paths = spec.get("paths", {})
    results: list[str] = []
    keyword_lower = keyword.lower()

    for path, methods in paths.items():
        if keyword_lower in path.lower():
            for method, details in methods.items():
                if method.lower() in ("get", "post", "put", "patch", "delete"):
                    results.append(f"{method.upper()} {path}: {details.get('summary', '')}")
            continue

        for method, details in methods.items():
            if method.lower() not in ("get", "post", "put", "patch", "delete"):
                continue
            summary = details.get("summary", "").lower()
            operation_id = details.get("operationId", "").lower()
            if keyword_lower in summary or keyword_lower in operation_id:
                results.append(f"{method.upper()} {path}: {details.get('summary', '')}")

    if not results:
        return f"No endpoints found matching keyword: {keyword}"

    return "\n".join(results)


@mcp.tool()
def get_saxo_endpoint_spec(method: str, path: str) -> str:
    """
    Get the detailed specification for a specific Saxo Bank OpenAPI endpoint.
    Provide the HTTP method (e.g., 'GET', 'POST') and the path.
    """
    spec = get_openapi_spec()
    if not spec:
        return "Error: Could not load OpenAPI specification."

    normalized_path = normalize_path(path)
    paths = spec.get("paths", {})
    if normalized_path not in paths:
        return f"Error: Path '{normalized_path}' not found."

    endpoint_methods = paths[normalized_path]
    method_lower = method.lower()
    if method_lower not in endpoint_methods:
        return f"Error: Method '{method.upper()}' not allowed for path '{normalized_path}'."

    details = endpoint_methods[method_lower]

    output: list[str] = []
    output.append(f"# {method.upper()} {normalized_path}")
    output.append(f"**Summary**: {details.get('summary', 'None')}")
    output.append(f"**Description**: {details.get('description', 'None')}")

    params = details.get("parameters", [])
    if params:
        output.append("\n## Parameters")
        for param in params:
            required = "(REQUIRED)" if param.get("required") else "(Optional)"
            output.append(
                f"- **{param.get('name')}** {required} [{param.get('in')}]: {param.get('description', '')}"
            )

    req_body = details.get("requestBody", {})
    if req_body:
        output.append("\n## Request Body")
        for content_type, content_details in req_body.get("content", {}).items():
            output.append(f"### {content_type}")
            schema = content_details.get("schema", {})
            output.append(f"Schema: {json.dumps(schema, indent=2)}")

    responses = details.get("responses", {})
    if responses:
        output.append("\n## Responses")
        for status_code, response_details in responses.items():
            output.append(f"### {status_code}")
            description = response_details.get("description", "")
            if description:
                output.append(description)
            for content_type, content_details in response_details.get("content", {}).items():
                output.append(f"#### {content_type}")
                schema = content_details.get("schema", {})
                if schema:
                    output.append(f"Schema: {json.dumps(schema, indent=2)}")

    path_lower = normalized_path.lower()
    if "/orders" in path_lower or "/positions" in path_lower:
        output.append("\n" + "=" * 80)
        output.append("⚠️ [CRITICAL WARNING] ⚠️")
        output.append(
            "Saxo API has complex netting rules, hedging constraints, and dynamic order restrictions."
        )
        output.append(
            "You MUST read the pitfall resource `saxo://docs/pitfalls.md` BEFORE writing any execution code."
        )
        output.append("=" * 80)

    return "\n".join(output)


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
