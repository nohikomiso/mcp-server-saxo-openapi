# saxo_doc_helper ローカル検証メモ

検証日: 2026-07-08

## シナリオ 1: 新規注文 API 調査フロー

```bash
python docs/saxo-openapi-agent-brain/tools/saxo_doc_helper.py search-endpoints orders
python docs/saxo-openapi-agent-brain/tools/saxo_doc_helper.py get-endpoint POST /trade/v2/orders
python docs/saxo-openapi-agent-brain/tools/saxo_doc_helper.py get-schema algorithmicorderdata
```

**結果**: OK。16 件ヒット → トップレベルパラメータ + Request Sample → ネストスキーマ `algorithmicorderdata` をドリルダウン可能。

## シナリオ 2: 入力ゆらぎ吸収

```bash
python docs/saxo-openapi-agent-brain/tools/saxo_doc_helper.py get-endpoint post trade/v2/order
```

**結果**: OK。「Did you mean?」で `POST /trade/v2/orders` を先頭候補として提示。

## シナリオ 3: 旧 Markdown ドキュメント経路との比較

| 観点 | 旧経路 (REFERENCE-INDEX + Grep + Read) | agent-brain (saxo_doc_helper) |
|------|----------------------------------------|-------------------------------|
| ステップ数 | 3+ (index grep → path 解決 → md Read) | 1–3 CLI（search → get-endpoint → get-schema） |
| トークン | 巨大 Markdown 全文 or 長い抜粋 | depth=0 で折りたたみ、必要分のみ |
| サンプル JSON | 別セクション探索 | Request/Response Sample を同一出力 |
| 入力ミス耐性 | パス推測で失敗しやすい | Normalizer + Did-you-mean |

**結論**: エンドポイント仕様調査は agent-brain が優位。概念説明（OAuth フロー等）は `01_auth_service.py`・Saxo 公式 URL・実装コードで代替する。
