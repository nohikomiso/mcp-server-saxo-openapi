# mcp-server-saxo-openapi

**Saxo Bank / サクソバンク証券 OpenAPI 仕様ルックアップ — CLI と MCP サーバー**

[English](https://github.com/nohikomiso/mcp-server-saxo-openapi/blob/main/README.md) | 日本語

---

![License](https://img.shields.io/badge/license-MIT-green.svg)
![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![CLI](https://img.shields.io/badge/CLI-saxo--doc--helper-blue.svg)
![MCP](https://img.shields.io/badge/MCP-FastMCP-orange.svg)
![Spec updated](https://img.shields.io/github/last-commit/nohikomiso/mcp-server-saxo-openapi/main?label=spec%20updated)

**版 0.3.3** · 仕様スナップショット: 2026-07-08

ターミナル、または Cursor / Claude Desktop などの MCP クライアントから、**サクソバンク証券（Saxo Bank）** OpenAPI のエンドポイント仕様を参照できます。AI エージェントがコードを書く前に、パラメータ・サンプル JSON・Saxo 特有の罠（pitfalls）を学ぶための**辞書サーバー**です（取引の実行はしません）。

クロール済み `spec/json`（84 ファイル）をパッケージに同梱し、ネストパラメータ・Request/Response サンプル・スキーマドリルダウンを提供します。

**要件:** Python 3.11 以上

---

## これは何か / 何かではないか

**目的:** AI エージェント（や開発者）が Saxo OpenAPI の使い方を理解するためのリファレンス。

**できること**

- エンドポイントをキーワードで探す
- メソッド・パス指定でパラメータとサンプル JSON を取得
- ネストスキーマのドリルダウン（`get_saxo_schema_spec`）
- 決済・OCO などのワークフロー手順（`get_saxo_workflow_guide`）
- `saxo://docs/pitfalls.md` — netting / StopIfTraded / IsForceOpen 等の攻略本
- `/orders`・`/positions` 照会時の **CRITICAL WARNING**
- Saxo へのログイン・API 呼び出しは不要（オフライン）

**できないこと**

- 発注・残高照会・ポジション操作などの **ライブ API 実行**
- OAuth / トークン管理

**非公式**です。Saxo Bank A/S との提携・推奨はありません。

---

## 使い方

### Cursor / Claude Desktop（MCP）

```json
{
  "mcpServers": {
    "saxo-openapi": {
      "command": "uvx",
      "args": ["mcp-server-saxo-openapi"]
    }
  }
}
```

### ターミナル（CLI）

```bash
uvx --from mcp-server-saxo-openapi saxo-doc-helper search-endpoints orders
uvx --from mcp-server-saxo-openapi saxo-doc-helper get-endpoint POST /trade/v2/orders --depth 1
uvx --from mcp-server-saxo-openapi saxo-doc-helper workflow-guide close_position
uvx --from mcp-server-saxo-openapi saxo-doc-helper --version
```

---

## MCP ツール / リソース

| ツール / リソース | 説明 |
|------------------|------|
| `search_saxo_endpoints(query)` | キーワードでエンドポイント検索 |
| `get_saxo_endpoint_spec(method, path, depth?)` | パラメータ・サンプル・警告 |
| `get_saxo_schema_spec(schema_name, depth?)` | ネストスキーマの詳細 |
| `get_saxo_workflow_guide(use_case)` | `close_position` / `if_done_oco` |
| `saxo://docs/pitfalls.md` | Saxo 特有の罠と回避策 |

---

## 0.3.0 の変更点

0.2.0 は単一の `saxo_openapi.json` で lookup しており、仕様が浅くなっていました。**0.3.0 で rich な `spec/json` 方式に復帰**しつつ、0.2.0 の pitfalls と警告は維持しています。

詳細は [CHANGELOG.md](https://github.com/nohikomiso/mcp-server-saxo-openapi/blob/main/CHANGELOG.md)。

---

## 既知の制限

- 警告はソフト示唆であり、エージェントが `pitfalls.md` を読み飛ばす場合がある
- 一部エンドポイントでは `response_parameters` ツリーが薄い（`response_sample` の方が信頼できる）
- pitfalls は実務知見ベース。公式ドキュメントの完全代替ではない

---

## 仕様データの時点

**取得日: 2026-07-08**（Saxo Release Notes 最新見出し: **2025/05/15**）

詳細は [SPEC_FRESHNESS.md](https://github.com/nohikomiso/mcp-server-saxo-openapi/blob/main/SPEC_FRESHNESS.md)。誤り・古さは [Issue](https://github.com/nohikomiso/mcp-server-saxo-openapi/issues) で報告歓迎。

---

## 関連プロジェクト

| プロジェクト | 何をするか |
|--------------|------------|
| [saxo-api-client](https://github.com/nohikomiso/saxo-api-client) | OAuth / セッション・REST / WebSocket クライアント |

---

## フィードバック・開発者向け

- 不具合・古い仕様・コントリビュート: [GitHub Issues](https://github.com/nohikomiso/mcp-server-saxo-openapi/issues)
- リリース手順: [docs/MAINTAINER.md](https://github.com/nohikomiso/mcp-server-saxo-openapi/blob/main/docs/MAINTAINER.md)

---

## License

[MIT License](https://github.com/nohikomiso/mcp-server-saxo-openapi/blob/main/LICENSE)
