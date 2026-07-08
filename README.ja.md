# saxo-openapi-agent-brain

[English](./README.md) | 日本語

---

![License](https://img.shields.io/badge/license-MIT-green.svg)
![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![AI-First](https://img.shields.io/badge/AI--First-Optimized-success.svg)
![MCP](https://img.shields.io/badge/MCP-stdio-orange.svg)

**Saxo Bank OpenAPI のエージェントファースト仕様エンジン**

機械可読 JSON 仕様 + CLI/MCP ヘルパー — 人間の読者ではなく、AI コーディングエージェント向けに構築。

---

## これは何？

このリポジトリは**人間向けドキュメントサイトではありません**。AI エージェント（Claude、Gemini、GPT、Cursor 等）が以下を行うための構造化知識ベースです：

- 任意の Saxo OpenAPI エンドポイント仕様（パラメータ、型、ネスト構造）を即時参照
- リクエスト/レスポンス JSON サンプルの取得
- 最小トークンでのネストスキーマのドリルダウン

`spec/json/` は **17 サービスグループ**（約 260 エンドポイント）をカバーし、再帰スキーマ解決とサンプル JSON を含みます。

---

## 動作要件

- **Python 3.10+**（3.11 以上推奨）
- **pip インストール不要** — `saxo_doc_helper.py` は標準ライブラリのみ

---

## インストール

```bash
git clone https://github.com/nohikomiso/saxo-openapi-agent-brain.git
cd saxo-openapi-agent-brain
python tools/saxo_doc_helper.py search-endpoints orders
```

既にローカルに clone 済みの場合は、リポジトリルートで以下と同じコマンドを実行してください。

---

## CLI クイックスタート

```bash
# キーワードでエンドポイントを検索
python tools/saxo_doc_helper.py search-endpoints orders

# トップレベルパラメータ + JSON サンプル
python tools/saxo_doc_helper.py get-endpoint POST /trade/v2/orders

# "[Refer to Schema: ...]" からネストスキーマへ
python tools/saxo_doc_helper.py get-schema algorithmicorderdata

# ネストを 1 段階展開
python tools/saxo_doc_helper.py get-endpoint POST /trade/v2/orders --depth 1
```

### AI 入力ゆらぎの自動補正

| 入力 | 正規化後 |
|------|----------|
| `post` | `POST` |
| `trade/v2/orders` | `/trade/v2/orders` |
| `https://gateway.saxobank.com/sim/openapi/trade/v2/orders` | `/trade/v2/orders` |

完全一致がない場合は **Did you mean?** 候補を返します。

---

## MCP サーバー

stdio MCP として起動：

```bash
python tools/saxo_doc_helper.py --mcp
```

MCP クライアント設定例（リポジトリルートから、または絶対パスで）：

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

### 公開ツール

| ツール | 説明 |
|--------|------|
| `search_saxo_endpoints(query)` | 全エンドポイントをキーワード検索 |
| `get_saxo_endpoint_spec(method, path, depth?)` | パラメータ + サンプル JSON |
| `get_saxo_schema_spec(schema_name, depth?)` | ネストスキーマのドリルダウン |

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

各 JSON ファイルには以下が含まれます：

- `method`, `path`, `name`
- `parameters` — 再帰ツリー（型、説明、Body/Query/Path）
- `request_sample` / `response_sample`

---

## エージェント統合

エージェントルール（`.cursor/rules/`、`AGENTS.md` 等）に追加：

> Saxo OpenAPI 仕様を調べるときは `spec/json/` を直接読まないこと。  
> このリポジトリルートから `python tools/saxo_doc_helper.py` で最小トークン取得すること。

例：

```bash
python tools/saxo_doc_helper.py search-endpoints positions
python tools/saxo_doc_helper.py get-endpoint GET /port/v1/positions
```

---

## 関連プロジェクト

| プロジェクト | 役割 |
|--------------|------|
| [saxo-apy](https://github.com/nohikomiso/saxo-apy) | OAuth・セッション管理 |
| [saxo-openapi](https://github.com/nohikomiso/saxo-openapi) | Python REST/WebSocket クライアント |

本リポジトリは **仕様参照**、上記は **ランタイム API アクセス** を担当します。

---

## データ出典と鮮度

- 仕様 JSON は公開 [Saxo Developer Portal](https://www.developer.saxo/openapi/referencedocs) から派生しています。
- **非公式**であり、Saxo Bank A/S の承認を受けたものではありません。
- `spec/json/` の最終更新は commit 履歴（将来は GitHub Releases）を参照してください。

仕様の再生成手順はメンテナ向け [docs/MAINTAINER.md](docs/MAINTAINER.md)。一般向けは [CONTRIBUTING.md](CONTRIBUTING.md)。

---

## 免責事項

- **非公式**: Saxo Bank A/S とは無関係です。
- **教育目的**: 公開 API ドキュメントに基づくエージェント支援開発向けです。
- **保証なし**: 不完全・古い情報を含む可能性があります。本番前は公式情報と実 API で確認してください。
- **商標**: Saxo Bank 等の商標は各権利者に帰属します。

---

## ライセンス

[MIT License](LICENSE)
