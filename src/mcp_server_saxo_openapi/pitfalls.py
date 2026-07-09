"""Pitfalls survival guide for AI agents (MCP resource content)."""

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

CRITICAL_WARNING_HEADER = """================================================================================
⚠️ [CRITICAL WARNING] ⚠️
Saxo API has complex netting rules, hedging constraints, and dynamic order restrictions.
You MUST read the pitfall resource `saxo://docs/pitfalls.md` BEFORE writing any execution code.
================================================================================"""
