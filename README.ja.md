# mcp-server-saxo-openapi

**Saxo Bank / サクソバンク証券 OpenAPI 仕様ルックアップ — CLI と MCP サーバー**

[English](https://github.com/nohikomiso/mcp-server-saxo-openapi/blob/main/README.md) | 日本語

---

![License](https://img.shields.io/badge/license-MIT-green.svg)
![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![CLI](https://img.shields.io/badge/CLI-saxo--doc--helper-blue.svg)
![MCP](https://img.shields.io/badge/MCP-stdio-orange.svg)
![Spec updated](https://img.shields.io/github/last-commit/nohikomiso/mcp-server-saxo-openapi/main?label=spec%20updated)

ターミナルまたは Cursor / Claude Desktop などの MCP クライアントから、**サクソバンク証券（Saxo Bank）** OpenAPI のエンドポイントパラメータと JSON サンプルを参照できます。公式リファレンスツリーが深すぎて辿りにくい、という問題向けです。

サードパーティ依存なし（Python 標準ライブラリのみ）。仕様 DB は約 260 エンドポイント / 17 サービスグループで、wheel にも同梱されます。

---

## Spec snapshot

**Spec snapshot: 2026-07-08**（Saxo Release Notes through **2025/05/15**）。

エージェント向けに再構成したスナップショットです。Saxo にドキュメント全体の semver はなく、クロール日と当時の最新 Release Notes 見出しを記録します。詳細: [SPEC_FRESHNESS.md](SPEC_FRESHNESS.md)。

欠け・誤り・古さを見つけたら [Issue](https://github.com/nohikomiso/mcp-server-saxo-openapi/issues) をください。PR: [CONTRIBUTING.md](CONTRIBUTING.md)。

---

## これは何か / 何かではないか

| 本パッケージ | 対象外 |
|--------------|--------|
| オフラインの **仕様ルックアップ**（CLI + MCP） | ライブ取引・ポートフォリオ API |
| Saxo 認証情報は不要 | OAuth・発注・残高照会 |
| トークン効率の段階的開示 | フル OpenAPI クライアントの代替 |

**ライブ** API を MCP から叩く場合は、コミュニティの [`@borgels/mcp-server-saxo`](https://www.npmjs.com/package/@borgels/mcp-server-saxo)（npm・非公式・別プロジェクト）などを参照。

**非公式** — Saxo Bank A/S との提携・推奨はありません。

---

## 機能

- **構造化仕様 DB** — ネストパラメータと Request/Response サンプル
- **CLI** — `search-endpoints` / `get-endpoint` / `get-schema`（depth 制御・Did you mean?）
- **MCP サーバー** — stdio JSON-RPC、同じ 3 ツール
- **トークン効率** — 段階的開示

**要件:** Python 3.10+

---

## はじめに — 推奨（uvx）

### 本番 PyPI

```bash
uvx mcp-server-saxo-openapi
uvx --from mcp-server-saxo-openapi saxo-doc-helper search-endpoints orders
uvx --from mcp-server-saxo-openapi saxo-doc-helper --version
```

CLI はパッケージ名と違うため `--from mcp-server-saxo-openapi` が必要です。

MCP 設定例:

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

### GitHub から

```bash
uvx --from git+https://github.com/nohikomiso/mcp-server-saxo-openapi.git saxo-doc-helper search-endpoints orders
```

### TestPyPI（開発用）

```bash
uvx --index-url https://test.pypi.org/simple/ \
    --index https://pypi.org/simple/ \
    --from mcp-server-saxo-openapi \
    saxo-doc-helper search-endpoints orders
```

---

## はじめに — ローカル clone

```bash
git clone https://github.com/nohikomiso/mcp-server-saxo-openapi.git
cd mcp-server-saxo-openapi
python tools/saxo_doc_helper.py search-endpoints orders
```

または:

```bash
uv sync
uv run saxo-doc-helper --version
```

---

## 公開 MCP ツール

| ツール | 説明 |
|--------|------|
| `search_saxo_endpoints(query)` | 全エンドポイントをキーワード検索 |
| `get_saxo_endpoint_spec(method, path, depth?)` | パラメータ + サンプル JSON |
| `get_saxo_schema_spec(schema_name, depth?)` | ネストスキーマのドリルダウン |

---

## 関連プロジェクト

| プロジェクト | 役割 |
|--------------|------|
| [saxo-apy](https://github.com/nohikomiso/saxo-apy) | OAuth / セッション |
| [saxo-openapi](https://github.com/nohikomiso/saxo-openapi) | REST/WebSocket クライアント |
| [@borgels/mcp-server-saxo](https://www.npmjs.com/package/@borgels/mcp-server-saxo) | ライブ Saxo OpenAPI MCP（npm・非公式） |

本リポジトリは **仕様ルックアップ**。ランタイム API は別レイヤーです。

---

## フィードバック

- 不具合・古い仕様: [GitHub Issues](https://github.com/nohikomiso/mcp-server-saxo-openapi/issues)
- メンテ: [docs/MAINTAINER.md](docs/MAINTAINER.md)

---

## License

[MIT License](LICENSE)
