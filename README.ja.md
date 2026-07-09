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

**要件:** Python 3.10 以上

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

## 使い方

いちばん簡単なのは [uv](https://docs.astral.sh/uv/) の `uvx` です（インストール不要でそのまま実行できます）。

### Cursor / Claude Desktop（MCP）

設定例:

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
uvx --from mcp-server-saxo-openapi saxo-doc-helper get-endpoint POST /trade/v2/orders
uvx --from mcp-server-saxo-openapi saxo-doc-helper --version
```

パッケージ名（`mcp-server-saxo-openapi`）と CLI コマンド名（`saxo-doc-helper`）が違うため、CLI では `--from mcp-server-saxo-openapi` を付けてください。

MCP サーバーだけ起動する場合:

```bash
uvx mcp-server-saxo-openapi
```

---

## 使えるツール（MCP）

| ツール | 説明 |
|--------|------|
| `search_saxo_endpoints(query)` | エンドポイントをキーワード検索 |
| `get_saxo_endpoint_spec(method, path, depth?)` | パラメータとサンプル JSON |
| `get_saxo_schema_spec(schema_name, depth?)` | ネストしたスキーマの詳細 |

CLI でも同じ内容を扱えます（`search-endpoints` / `get-endpoint` / `get-schema`）。

---

## 仕様データの時点

**取得日: 2026-07-08**（その時点の Saxo Release Notes 最新見出し: **2025/05/15**）

Saxo 側に「ドキュメント全体のバージョン番号」はないため、取得した日と、ポータルに載っていた最新の Release Notes 見出しを記録しています。詳細は [SPEC_FRESHNESS.md](SPEC_FRESHNESS.md) を参照してください。

欠けている項目・誤り・古そうな内容を見つけたら、[Issue](https://github.com/nohikomiso/mcp-server-saxo-openapi/issues) で教えてください。

---

## 関連プロジェクト

本リポジトリは「仕様を読む」ためのものです。実際に API を呼ぶときは、次のような別プロジェクトを使います。

| プロジェクト | 何をするか |
|--------------|------------|
| [saxo-apy](https://github.com/nohikomiso/saxo-apy) | OAuth / セッション（作者の別リポ） |
| [saxo-openapi](https://github.com/nohikomiso/saxo-openapi) | REST / WebSocket クライアント（作者の別リポ） |
| [@borgels/mcp-server-saxo](https://www.npmjs.com/package/@borgels/mcp-server-saxo) | MCP からライブ API を叩く例（コミュニティ・非公式・別作者） |

---

## フィードバック・開発者向け

- 不具合・古い仕様: [GitHub Issues](https://github.com/nohikomiso/mcp-server-saxo-openapi/issues)
- コントリビュート（clone・テストなど）: [CONTRIBUTING.md](CONTRIBUTING.md)
- 仕様の再取得・リリース手順（メンテナー向け）: [docs/MAINTAINER.md](docs/MAINTAINER.md)

---

## License

[MIT License](LICENSE)
