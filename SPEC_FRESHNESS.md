# Spec freshness

| Field | Value |
|-------|-------|
| **Spec snapshot** | `2026-07-08` |
| **Saxo Release Notes through** | `2025/05/15` |
| Package version | `0.1.1` (tool/PyPI version; independent of the snapshot dates) |

There is **no single semver** for the whole Saxo OpenAPI documentation set. Saxo publishes dated [Release Notes](https://www.developer.saxo/openapi/releasenotes/release-notes) (e.g. `Release 2025/05/15`). Endpoint paths may contain `v1`/`v2` — those are per-service API versions, not a global docs version.

## What the dates mean

- **Spec snapshot** — the day this repository’s structured `spec/json/` was crawled/synced from the Saxo Developer Portal.
- **Saxo Release Notes through** — the newest Release Notes heading present on the portal when that snapshot was taken.

## Source

- Reference docs: https://www.developer.saxo/openapi/referencedocs
- Release notes: https://www.developer.saxo/openapi/releasenotes
- Planned changes: https://www.developer.saxo/openapi/releasenotes/planned-changes

When the portal changes, maintainers refresh `spec/json/`, update the dates in this file (and the matching constants in the package), sync package data, and publish a new package version.

## Feedback

Missing endpoint, wrong parameter, or something that looks out of date? Please [open an Issue](https://github.com/nohikomiso/mcp-server-saxo-openapi/issues).
