# mcp-server-saxo-openapi

**Saxo Bank / サクソバンク証券 OpenAPI 仕様ルックアップ — CLI と MCP サーバー**

[English](https://github.com/nohikomiso/mcp-server-saxo-openapi/blob/main/README.md) | 日本語

---

![License](https://img.shields.io/badge/license-MIT-green.svg)
![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![CLI](https://img.shields.io/badge/CLI-saxo--doc--helper-blue.svg)
![MCP](https://img.shields.io/badge/MCP-stdio-orange.svg)
![Spec updated](https://img.shields.io/github/last-commit/nohikomiso/mcp-server-saxo-openapi/main?label=spec%20updated)

ターミナル、または Cursor / Claude Desktop などの MCP クライアントから、**サクソバンク証券（Saxo Bank）** OpenAPI のエンドポイントパラメータと JSON サンプルを参照できます。公式リファレンスが深すぎて、AI で情報を取りにくい・わかりにくい、という課題から作ったものです。

追加のライブラリは不要です（Python 標準ライブラリのみ）。仕様データは JSON で、約 260 エンドポイント・17 サービスグループ分をパッケージに同梱しています。

---

## Spec snapshot（仕様の時点）

**Spec snapshot: 2026-07-08**（Saxo Release Notes の最新見出し: **2025/05/15**）

エージェント向けに整理したスナップショットです。Saxo 側に「ドキュメント全体のバージョン番号」はないため、取得した日と、その時点でポータルに載っていた最新の Release Notes 見出しを記録しています。詳細は [SPEC_FRESHNESS.md](SPEC_FRESHNESS.md) を参照してください。

欠けている項目・誤り・古そうな内容を見つけたら、[Issue](https://github.com/nohikomiso/mcp-server-saxo-openapi/issues) で教えてください。Pull Request は [CONTRIBUTING.md](CONTRIBUTING.md) を参照してください。

---

## これは何か / 何かではないか

| 本パッケージ | 対象外 |
|--------------|--------|
| オフラインの **仕様ルックアップ**（CLI + MCP） | ライブの取引・ポートフォリオ API |
| Saxo の認証情報は不要 | OAuth・発注・残高照会 |
| 必要な分だけ段階的に返す | 本格的な OpenAPI クライアントの代替 |

**ライブ** API を MCP から使う場合は、コミュニティの [`@borgels/mcp-server-saxo`](https://www.npmjs.com/package/@borgels/mcp-server-saxo)（npm・非公式・別プロジェクト）などを参照してください。

**非公式**です。Saxo Bank A/S との提携・推奨はありません。

---

## 機能

- **構造化された仕様 JSON** — ネストしたパラメータと Request / Response サンプル
- **CLI** — `search-endpoints` / `get-endpoint` / `get-schema`（深さの制御・Did you mean?）
- **MCP サーバー** — stdio の JSON-RPC。上記と同じ 3 ツール
- **トークン節約** — まず要約、必要ならドリルダウン

**要件:** Python 3.10 以上

---

## はじめに（推奨: uvx）

### 本番 PyPI

```bash
uvx mcp-server-saxo-openapi
uvx --from mcp-server-saxo-openapi saxo-doc-helper search-endpoints orders
uvx --from mcp-server-saxo-openapi saxo-doc-helper --version
```

CLI コマンド名（`saxo-doc-helper`）とパッケージ名が違うため、CLI では `--from mcp-server-saxo-openapi` を付けてください。

MCP の設定例:

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

## はじめに（ローカル clone）

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

## 公開している MCP ツール

| ツール | 説明 |
|--------|------|
| `search_saxo_endpoints(query)` | エンドポイントをキーワード検索 |
| `get_saxo_endpoint_spec(method, path, depth?)` | パラメータとサンプル JSON |
| `get_saxo_schema_spec(schema_name, depth?)` | ネストしたスキーマの詳細 |

---

## 関連プロジェクト

| プロジェクト | 役割 |
|--------------|------|
| [saxo-apy](https://github.com/nohikomiso/saxo-apy) | OAuth / セッション |
| [saxo-openapi](https://github.com/nohikomiso/saxo-openapi) | REST / WebSocket クライアント |
| [@borgels/mcp-server-saxo](https://www.npmjs.com/package/@borgels/mcp-server-saxo) | ライブ Saxo OpenAPI MCP（npm・非公式） |

本リポジトリは **仕様のルックアップ** 用です。実際の API 呼び出しは別レイヤーです。

---

## フィードバック

- 不具合・古い仕様: [GitHub Issues](https://github.com/nohikomiso/mcp-server-saxo-openapi/issues)
- メンテ手順: [docs/MAINTAINER.md](docs/MAINTAINER.md)

---

## License

[MIT License](LICENSE)
