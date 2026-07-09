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

**目的:** AI エージェント（や開発者）が、「この API はどう使うのか」を理解するためのものです。公式リファレンスから取り出したパラメータ定義と JSON サンプルを、CLI / MCP から参照できます。

**できること**

- エンドポイントをキーワードで探す
- メソッド・パスを指定して、パラメータとサンプル JSON を見る
- ネストした型（スキーマ）を段階的に開いて読む
- Saxo のログインや API キーは不要（ネット経由で Saxo に問い合わせない）

**できないこと（このパッケージの範囲外）**

- Saxo の API を実際に呼び出すこと（発注・残高照会・ポジション取得など）
- OAuth 認証やトークン管理
- 取引クライアントそのものの代替

実際に API を叩く必要がある場合は、別のライブラリやツールを使ってください。MCP 経由でライブ API を扱うコミュニティ製の例として、[`@borgels/mcp-server-saxo`](https://www.npmjs.com/package/@borgels/mcp-server-saxo)（npm・非公式・別プロジェクト）があります。本リポジトリとは無関係です。

**非公式**です。Saxo Bank A/S との提携・推奨はありません。

---

## 機能

- **仕様 JSON** — パラメータ定義と Request / Response のサンプル
- **CLI** — `search-endpoints` / `get-endpoint` / `get-schema`（表示の深さ指定・近い候補の提示）
- **MCP サーバー** — 上記と同じ 3 ツールを Cursor などから呼べる
- **トークン節約** — まず要約を返し、必要ならネストを段階的に開く

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

本リポジトリは「仕様を読む」ためのものです。実際に API を呼ぶときは、次のような別プロジェクトを使います。

| プロジェクト | 何をするか |
|--------------|------------|
| [saxo-apy](https://github.com/nohikomiso/saxo-apy) | OAuth / セッション（作者の別リポ） |
| [saxo-openapi](https://github.com/nohikomiso/saxo-openapi) | REST / WebSocket クライアント（作者の別リポ） |
| [@borgels/mcp-server-saxo](https://www.npmjs.com/package/@borgels/mcp-server-saxo) | MCP からライブ API を叩く例（コミュニティ・非公式・別作者） |

---

## フィードバック

- 不具合・古い仕様: [GitHub Issues](https://github.com/nohikomiso/mcp-server-saxo-openapi/issues)
- メンテ手順: [docs/MAINTAINER.md](docs/MAINTAINER.md)

---

## License

[MIT License](LICENSE)
