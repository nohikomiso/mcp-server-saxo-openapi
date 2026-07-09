# saxo_doc_helper / mcp-server-saxo-openapi 検証メモ

## 2026-07-09 — Phase C（パッケージ化 + TestPyPI 準備）

### ローカル wheel / uvx

```bash
cd docs/mcp-server-saxo-openapi
uv build
uvx --from ./dist/mcp_server_saxo_openapi-0.1.0-py3-none-any.whl \
  saxo-doc-helper search-endpoints orders
```

**結果**: OK。16 件ヒット（`POST /trade/v2/orders` 含む）。wheel 内 JSON 84 ファイル。

### MCP initialize スモーク

```bash
printf '%s\n' \
  '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"smoke","version":"0"}}}' \
  '{"jsonrpc":"2.0","method":"notifications/initialized"}' \
  '{"jsonrpc":"2.0","id":2,"method":"tools/list"}' \
| uvx --from ./dist/mcp_server_saxo_openapi-0.1.0-py3-none-any.whl mcp-server-saxo-openapi
```

**結果**: OK。`serverInfo.name=mcp-server-saxo-openapi`, `version=0.1.0`。`tools/list` で 3 ツール。

### ユニットテスト

```bash
uv run python -m unittest discover -s tests -v
```

**結果**: 11 tests OK。

### TestPyPI

公開先: https://test.pypi.org/project/mcp-server-saxo-openapi/

```bash
uvx --index-url https://test.pypi.org/simple/ \
    --index https://pypi.org/simple/ \
    --from mcp-server-saxo-openapi \
    saxo-doc-helper search-endpoints orders
```

**結果**: OK。16 件ヒット。

```bash
printf '%s\n' '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"smoke","version":"0"}}}' \
| uvx --index-url https://test.pypi.org/simple/ \
      --index https://pypi.org/simple/ \
      mcp-server-saxo-openapi
```

**結果**: OK。`serverInfo.name=mcp-server-saxo-openapi`, `version=0.1.0`（当時）。

### Production PyPI（2026-07-09）

公開先: https://pypi.org/project/mcp-server-saxo-openapi/

```bash
uvx --refresh-package mcp-server-saxo-openapi --from mcp-server-saxo-openapi saxo-doc-helper --version
uvx --from mcp-server-saxo-openapi saxo-doc-helper search-endpoints orders
```

**結果**: OK。`0.1.1 (spec snapshot 2026-07-08; saxo RN through 2025/05/15)`。orders 16 件。

GitHub Release: https://github.com/nohikomiso/mcp-server-saxo-openapi/releases/tag/v0.1.1

---

## 2026-07-08 — 旧 clone 経路

### シナリオ 1: 新規注文 API 調査フロー

```bash
python tools/saxo_doc_helper.py search-endpoints orders
python tools/saxo_doc_helper.py get-endpoint POST /trade/v2/orders
python tools/saxo_doc_helper.py get-schema algorithmicorderdata
```

**結果**: OK。

### シナリオ 2: 入力ゆらぎ吸収

```bash
python tools/saxo_doc_helper.py get-endpoint post trade/v2/order
```

**結果**: OK。「Did you mean?」で `POST /trade/v2/orders` を先頭候補として提示。
