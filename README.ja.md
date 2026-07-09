# mcp-server-saxo-openapi

**Saxo OpenAPI 仕様ルックアップ — CLI と MCP サーバー**

[English](./README.md) | 日本語

---

![License](https://img.shields.io/badge/license-MIT-green.svg)
![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![CLI](https://img.shields.io/badge/CLI-saxo--doc--helper-blue.svg)
![MCP](https://img.shields.io/badge/MCP-stdio-orange.svg)

ターミナルまたは Cursor / Claude Desktop などの MCP クライアントから、Saxo OpenAPI のエンドポイントパラメータと JSON サンプルを参照できます。

サードパーティ依存なし（Python 標準ライブラリのみ）。仕様 DB は `spec/json/`（約 260 エンドポイント / 17 サービスグループ）で、wheel にも同梱されます。

---

## 機能

- **構造化仕様 DB** — ネストパラメータと Request/Response サンプル
- **CLI** — `search-endpoints` / `get-endpoint` / `get-schema`（depth 制御・Did you mean?）
- **MCP サーバー** — stdio JSON-RPC、同じ 3 ツール
- **トークン効率** — 段階的開示（ネストは折りたたみ、必要時にドリルダウン）

**要件:** Python 3.10+

---

## はじめに — 推奨（uvx）

### CLI（TestPyPI — 利用可）

```bash
uvx --index-url https://test.pypi.org/simple/ \
    --index https://pypi.org/simple/ \
    saxo-doc-helper search-endpoints orders
```

### MCP（TestPyPI）

```bash
uvx --index-url https://test.pypi.org/simple/ \
    --index https://pypi.org/simple/ \
    mcp-server-saxo-openapi
```

MCP クライアント設定例:

```json
{
  "mcpServers": {
    "saxo-openapi": {
      "command": "uvx",
      "args": [
        "--index-url", "https://test.pypi.org/simple/",
        "--index", "https://pypi.org/simple/",
        "mcp-server-saxo-openapi"
      ]
    }
  }
}
```

### GitHub から（リポジトリ公開後）

```bash
uvx --from git+https://github.com/nohikomiso/mcp-server-saxo-openapi.git saxo-doc-helper search-endpoints orders
uvx --from git+https://github.com/nohikomiso/mcp-server-saxo-openapi.git mcp-server-saxo-openapi
```

### 本番 PyPI（次ゲート — 未公開）

本番公開後:

```bash
uvx mcp-server-saxo-openapi
uvx saxo-doc-helper search-endpoints orders
```

---

## はじめに — ローカル clone

```bash
git clone https://github.com/nohikomiso/mcp-server-saxo-openapi.git
cd mcp-server-saxo-openapi
python tools/saxo_doc_helper.py search-endpoints orders
python tools/saxo_doc_helper.py get-endpoint POST /trade/v2/orders
```

または editable インストール:

```bash
uv sync
uv run saxo-doc-helper search-endpoints orders
```

### 入力正規化

| 入力 | 正規化後 |
|------|----------|
| `post` | `POST` |
| `trade/v2/orders` | `/trade/v2/orders` |
| フル gateway URL | `/trade/v2/orders` など |

一致しない場合は **Did you mean?** を返します。

---

## 公開 MCP ツール

| ツール | 説明 |
|--------|------|
| `search_saxo_endpoints(query)` | 全エンドポイントをキーワード検索 |
| `get_saxo_endpoint_spec(method, path, depth?)` | パラメータ + サンプル JSON |
| `get_saxo_schema_spec(schema_name, depth?)` | ネストスキーマのドリルダウン |

---

## エージェント統合

> Saxo OpenAPI 仕様を調べるときは `spec/json/` を直接読まないこと。  
> `saxo-doc-helper`（または clone 時は `python tools/saxo_doc_helper.py`）を使うこと。

---

## 関連プロジェクト

| プロジェクト | 役割 |
|--------------|------|
| [saxo-apy](https://github.com/nohikomiso/saxo-apy) | OAuth / セッション |
| [saxo-openapi](https://github.com/nohikomiso/saxo-openapi) | REST/WebSocket クライアント |

本リポジトリは **仕様ルックアップ**。上記は **ランタイム API アクセス**。

---

## データソースと免責

- 仕様 JSON は公開 [Saxo Developer Portal](https://www.developer.saxo/openapi/referencedocs) 由来。
- **非公式** — Saxo Bank A/S との提携・推奨はありません。
- メンテ手順: [docs/MAINTAINER.md](docs/MAINTAINER.md)。

---

## License

[MIT License](LICENSE)
