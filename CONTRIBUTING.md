# Contributing

Thank you for your interest in **mcp-server-saxo-openapi**.

## What we welcome

- Bug reports and reproducible examples for `saxo-doc-helper` / MCP
- Improvements to CLI/MCP ergonomics (normalization, error messages, tests)
- Documentation fixes in `README.md` / `README.ja.md`

## What is harder to accept

- Hand-editing large files under `spec/json/` — specs are generated from the Saxo Developer Portal. Prefer the maintainer regeneration flow.

## Updating the spec database

If you maintain a full development workspace with the crawler pipeline, see [docs/MAINTAINER.md](docs/MAINTAINER.md).

Otherwise, open an issue describing which Saxo endpoint or schema looks stale, with a link to the official Saxo reference page.

## Development setup

```bash
git clone https://github.com/nohikomiso/mcp-server-saxo-openapi.git
cd mcp-server-saxo-openapi
uv sync
uv run python -m unittest discover -s tests -v
```

No third-party runtime dependencies (Python standard library only).

Before a release, sync packaged data from the maintainer source of truth:

```bash
rm -rf src/saxo_doc_helper/data/json
cp -a spec/json src/saxo_doc_helper/data/json
```

## Pull requests

1. Fork and create a branch from `main`
2. Run `uv run python -m unittest discover -s tests -v`
3. Keep README changes in sync across English and Japanese when both are affected
4. Open a PR with a short summary and test evidence

## License

By contributing, you agree that your contributions will be licensed under the [MIT License](LICENSE).
