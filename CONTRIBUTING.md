# Contributing

Thank you for your interest in **saxo-openapi-agent-brain**.

## What we welcome

- Bug reports and reproducible examples for `tools/saxo_doc_helper.py`
- Improvements to CLI/MCP ergonomics (normalization, error messages, tests)
- Documentation fixes in `README.md` / `README.ja.md`

## What is harder to accept

- Hand-editing large files under `spec/json/` — specs are generated from the Saxo Developer Portal. Prefer the maintainer regeneration flow.

## Updating the spec database

If you maintain a full development workspace with the crawler pipeline, see [docs/MAINTAINER.md](docs/MAINTAINER.md).

Otherwise, open an issue describing which Saxo endpoint or schema looks stale, with a link to the official Saxo reference page.

## Development setup

```bash
git clone <this-repository>
cd saxo-openapi-agent-brain
python tools/test_saxo_doc_helper.py -v
```

No pip dependencies are required for the helper tool (Python standard library only).

## Pull requests

1. Fork and create a branch from `main`
2. Run `python tools/test_saxo_doc_helper.py -v`
3. Keep README changes in sync across English and Japanese when both are affected
4. Open a PR with a short summary and test evidence

## License

By contributing, you agree that your contributions will be licensed under the [MIT License](LICENSE).
