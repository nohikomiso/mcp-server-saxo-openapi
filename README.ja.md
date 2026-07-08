# saxo-openapi-agent-brain

**Saxo OpenAPI 仕様ルックアップ — CLI ツール & MCP サーバー**

[English](./README.md) | 日本語

---

![License](https://img.shields.io/badge/license-MIT-green.svg)
![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![CLI](https://img.shields.io/badge/CLI-saxo__doc__helper-blue.svg)
![MCP](https://img.shields.io/badge/MCP-stdio-orange.svg)

ターミナルから Saxo OpenAPI のエンドポイント仕様・JSON サンプルを引けます。同じ機能を Cursor、Claude Desktop 等の MCP クライアントにも接続できます。

`saxo_doc_helper.py` は標準ライブラリのみの Python スクリプトで、`spec/json/`（17 サービスグループ・約 260 エンドポイント）をバックエンドに使います。

---

## 特徴

- **構造化 spec データベース** — ネストパラメータと Request/Response サンプル付き `spec/json/`
- **CLI** — `search-endpoints` / `get-endpoint` / `get-schema`、depth 制御と「もしかして？」候補
- **MCP サーバー** — `--mcp` で stdio JSON-RPC、上記 3 機能を MCP ツールとして公開
- **トークン効率** — 漸進的開示（ネストは折りたたみ、必要時にドリルダウン）
- **対象** — Saxo API 連携開発者、AI コーディングエージェント、生 JSON を使うフルスクラッチ開発者

**動作要件:** Python 3.10+（ヘルパーは stdlib のみ — `pip install` 不要）。

---

## はじめ方 — CLI

### 1. クローン

```bash
git clone https://github.com/nohikomiso/saxo-openapi-agent-brain.git
cd saxo-openapi-agent-brain
```

### 2. 検索を試す

```bash
python tools/saxo_doc_helper.py search-endpoints orders
```

### 3. エンドポイント仕様を取得

```bash
python tools/saxo_doc_helper.py get-endpoint POST /trade/v2/orders
python tools/saxo_doc_helper.py get-schema algorithmicorderdata
```

### その他の CLI 例

```bash
# ネストを 1 段階展開
python tools/saxo_doc_helper.py get-endpoint POST /trade/v2/orders --depth 1
```

### 入力の自動正規化

| 入力 | 正規化後 |
|------|----------|
| `post` | `POST` |
| `trade/v2/orders` | `/trade/v2/orders` |
| `https://gateway.saxobank.com/sim/openapi/trade/v2/orders` | `/trade/v2/orders` |

完全一致がない場合は **Did you mean?** 候補を返します。

### フルスクラッチ開発者向け

`spec/json/` を直接読むこともできます。CLI は必要な部分だけ返すため、トークン節約に向いています。

---

## はじめ方 — MCP

Saxo 仕様ルックアップを MCP クライアント（Cursor、Claude Desktop 等）に接続します。

### オプション 1: ローカル clone から（いま使える）

**ステップ 1.** 本リポジトリを clone（上記 CLI セクション参照）。

**ステップ 2.** サーバーを試す:

```bash
python tools/saxo_doc_helper.py --mcp
```

**ステップ 3.** MCP クライアント設定に追加:

```json
{
  "mcpServers": {
    "saxo-openapi-agent-brain": {
      "command": "python3",
      "args": ["tools/saxo_doc_helper.py", "--mcp"],
      "cwd": "/absolute/path/to/saxo-openapi-agent-brain"
    }
  }
}
```

`cwd` は clone 先の絶対パスに置き換えてください。

### オプション 2: uvx（予定 — 未公開）

PyPI パッケージ化後の目標:

```bash
uvx mcp-server-saxo-openapi
```

**現時点では利用できません。** 配布ロードマップは親開発ワークスペースの `docs/saxo-openapi-agent-brain-distribution-roadmap.md` を参照。

### 公開 MCP ツール

| ツール | 説明 |
|--------|------|
| `search_saxo_endpoints(query)` | 全エンドポイントをキーワード検索 |
| `get_saxo_endpoint_spec(method, path, depth?)` | パラメータ + サンプル JSON |
| `get_saxo_schema_spec(schema_name, depth?)` | ネストスキーマのドリルダウン |

---

## エージェント統合

エージェントルール（`.cursor/rules/`、`AGENTS.md` 等）に追加:

> Saxo OpenAPI 仕様を調べるときは `spec/json/` を直接読まないこと。  
> このリポジトリルートから `python tools/saxo_doc_helper.py` を使うこと。

例:

```bash
python tools/saxo_doc_helper.py search-endpoints positions
python tools/saxo_doc_helper.py get-endpoint GET /port/v1/positions
```

---

## リポジトリ構成

```text
saxo-openapi-agent-brain/
├── LICENSE
├── README.md / README.ja.md
├── CONTRIBUTING.md
├── docs/
│   └── MAINTAINER.md      # 仕様再生成（メンテナ向け）
├── spec/json/             # 機械可読 OpenAPI データベース
│   ├── trade/
│   ├── port/
│   └── ...                # 17 サービスグループ
└── tools/
    ├── saxo_doc_helper.py
    └── test_saxo_doc_helper.py
```

`spec/json/` の各 JSON には `method`、`path`、`name`、再帰的 `parameters`、`request_sample` / `response_sample` が含まれます。

---

## 関連プロジェクト

| プロジェクト | 役割 |
|--------------|------|
| [saxo-apy](https://github.com/nohikomiso/saxo-apy) | OAuth・セッション管理 |
| [saxo-openapi](https://github.com/nohikomiso/saxo-openapi) | Python REST/WebSocket クライアント |

本リポジトリは **仕様参照**、上記は **ランタイム API アクセス** を担当します。

---

## データ出典と免責

- 仕様 JSON は公開 [Saxo Developer Portal](https://www.developer.saxo/openapi/referencedocs) から派生しています。
- **非公式** — Saxo Bank A/S とは無関係であり、承認を受けたものではありません。
- 不完全・古い情報を含む可能性があります。本番前は公式情報と実 API で確認してください。
- `spec/json/` の最終更新は commit 履歴を参照。メンテナ: [docs/MAINTAINER.md](docs/MAINTAINER.md)。

---

## ライセンス

[MIT License](LICENSE)
