# saxo-openapi-agent-brain

**Saxo Bank OpenAPI のエージェントファースト仕様エンジン**  
機械可読JSON仕様 + CLI/MCPツール — 人間の読者ではなく、AIコーディングエージェント向けに構築。

---

## これは何？

このリポジトリは**人間が読むためのドキュメントサイトではありません**。AIコーディングエージェント（Claude、Gemini、GPT、Cursor等）が以下を行うための構造化知識ベースです：

- 任意のSaxo OpenAPIエンドポイント仕様（パラメータ、型、ネスト構造）を即時参照
- 任意のエンドポイントの実際のリクエスト/レスポンスJSONサンプルの取得
- ネストされたスキーマオブジェクトへのオンデマンドドリルダウン

`spec/json/` 配下のJSONスペックは**Saxo OpenAPIの全17サービスグループ**（合計約260エンドポイント）を対象とし、完全な再帰スキーマ解決と実際のリクエスト/レスポンスサンプルが埋め込まれています。

---

## クイックスタート（CLI）

インストール不要 — Python 3.x 標準ライブラリのみ。

```bash
# キーワードでエンドポイントを検索
python tools/saxo_doc_helper.py search-endpoints orders

# 特定エンドポイントのトップレベルパラメータ + JSONサンプル取得
python tools/saxo_doc_helper.py get-endpoint POST /trade/v2/orders

# 出力に表示されたネストスキーマをドリルダウン
python tools/saxo_doc_helper.py get-schema algorithmicorderdata

# ネストパラメータを展開（depth=1で1段階子を表示）
python tools/saxo_doc_helper.py get-endpoint POST /trade/v2/orders --depth 1
```

### AI入力ゆらぎの自動補正

よくあるAIエージェントのミスを自動正規化：
- メソッドの大文字小文字: `post` → `POST`
- 先頭スラッシュ抜け: `trade/v2/orders` → `/trade/v2/orders`
- フルURL指定: `https://gateway.saxobank.com/sim/openapi/trade/v2/orders` → `/trade/v2/orders`

完全一致が見つからない場合は「もしかして？」候補を返却。

---

## MCPサーバー（Claude Desktop / Cursor / 任意のMCPクライアント）

```bash
python tools/saxo_doc_helper.py --mcp
```

MCPクライアントの設定に追加：
```json
{
  "mcpServers": {
    "saxo-openapi-agent-brain": {
      "command": "python",
      "args": ["/path/to/docs/saxo-openapi-agent-brain/tools/saxo_doc_helper.py", "--mcp"]
    }
  }
}
```

---

## エージェントへの推奨指示

エージェントのルールファイル（`.cursor/rules/`、`AGENTS.md`等）に追加：

> Saxo OpenAPI仕様を調査する際は、JSONファイルを直接読まないこと。  
> `python docs/saxo-openapi-agent-brain/tools/saxo_doc_helper.py` を使って最小トークンで仕様をクエリしなさい。
