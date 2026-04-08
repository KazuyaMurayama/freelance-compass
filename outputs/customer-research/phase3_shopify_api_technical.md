# Phase 3: Shopify API技術制約確認＋プロトタイプ構想

> 調査日: 2026-03-18
> 調査対象: Shopify Admin API / Storefront API / 関連エコシステム

---

## 1. Shopify API概要

### 1.1 Admin API

Shopify Admin APIはマーチャント向けのバックエンド操作APIであり、商品・注文・顧客・在庫・フルフィルメント等のデータに対してフルのCRUD操作が可能。

**重要な移行情報:**
- REST Admin APIは2024年10月1日をもって**レガシーAPI**に指定
- 2025年4月1日以降、新規Public AppはGraphQL Admin APIのみで構築が必須
- 既存アプリのREST利用は当面継続可能だが、完全移行期限が別途設定される予定

**主要リソース:**

| リソース | 取得可能なデータ | 更新可能な範囲 | 必要なスコープ |
|----------|-----------------|---------------|---------------|
| **Products** | title, descriptionHtml, vendor, product_type, tags, variants, images, SEOメタ, status, handle | 全フィールド更新可能。`productUpdate`ミューテーションで一括更新も可 | `read_products`, `write_products` |
| **Orders** | order_number, financial_status, fulfillment_status, line_items, customer, shipping_address, billing_address, total_price, subtotal_price, tax, discount, created_at, refunds | ノート・タグ・配送先の更新、キャンセル、返品処理 | `read_orders`, `write_orders` |
| **Customers** | email, first_name, last_name, orders_count, total_spent, tags, addresses, created_at, accepts_marketing, `lifetimeSpendAndOrderCount`(GraphQL) | 顧客情報の更新、タグ付け、マーケティング同意状態 | `read_customers`, `write_customers` |
| **Inventory** | InventoryItem(SKU, tracked, 関税情報), InventoryLevel(available, on_hand, incoming, committed, reserved等の数量状態) | 在庫の有効化、数量調整、状態間移動（available↔reserved等） | `read_inventory`, `write_inventory` |

**Ordersの重要な制限:**
- デフォルトでは**直近60日分**の注文のみ取得可能
- 全期間のアクセスには`read_all_orders`スコープが必要（Shopifyの審査が必要）

**Inventoryの重要な制限:**
- `committed`状態の在庫はAPI経由で調整不可（注文の作成・フルフィルメントでのみ変動）
- API version 2026-04以降、冪等性キーが必須

### 1.2 Storefront API

Storefront APIは**顧客向け（フロントエンド）体験**を構築するためのGraphQL API。

**できること:**
- 商品カタログの参照（商品、コレクション、バリアント）
- カートの作成・管理
- チェックアウトの開始
- 顧客認証（ログイン・登録）
- コンテンツ（ブログ、ページ）の取得
- ヘッドレスコマース、モバイルアプリ、IoT向けストアフロント構築

**できないこと:**
- 注文管理・フルフィルメント操作
- 在庫数の更新
- 顧客データの管理的操作
- 商品の作成・更新・削除
- 価格ルールやディスカウントの管理
- ストア設定の変更

**Admin APIとの主な違い:**

| 項目 | Admin API | Storefront API |
|------|-----------|----------------|
| アクセス | サーバーサイド専用（秘密鍵） | クライアントサイド安全（公開可） |
| データ操作 | フルCRUD | 主にRead + カート操作 |
| レート制限 | コストベース（後述） | リクエスト数制限なし（バイヤーIP単位） |
| ユースケース | バックオフィス管理 | カスタムストアフロント |
| API形式 | GraphQL（推奨）+ REST（レガシー） | GraphQLのみ |
| ID形式 | `gid://shopify/Product/1` | Base64エンコード |

### 1.3 Rate Limits & 制約

#### GraphQL Admin API（推奨）

| プラン | バケットサイズ | リストアレート |
|--------|-------------|--------------|
| Standard | 2,000ポイント | 50ポイント/秒 |
| Advanced | 4,000ポイント | 100ポイント/秒（推定） |
| Shopify Plus | 20,000ポイント | 500ポイント/秒（推定） |

- **1リクエストあたりの最大コスト**: 1,000ポイント
- **ミューテーション**: 10ポイント/回
- **クエリ（オブジェクト取得）**: 1ポイント/オブジェクト
- **バルクオペレーション**: レート制限の対象外（大量データ処理用）
- **在庫調整帯域**: 最大500アイテム/秒、180万調整/時間

#### REST Admin API（レガシー）

| プラン | バケットサイズ | リークレート |
|--------|-------------|------------|
| Standard | 40リクエスト | 2リクエスト/秒 |
| Shopify Plus | 400リクエスト | 20リクエスト/秒 |

#### Storefront API
- リクエスト数の制限なし（バイヤーIP単位のレート制限）
- トークンレスアクセスの場合、クエリ複雑度上限1,000

#### その他の制限
- 商品バリアントが50,000を超えるストアでは、1日あたり1,000バリアントまでの追加制限（Shopify Plusは対象外）
- APIコール自体は**無料**（全プランで追加料金なし）

### 1.4 認証方式

| 方式 | 特徴 | 2026年以降の状況 |
|------|------|-----------------|
| **Custom App（Admin直接作成）** | シンプルな固定トークン。単一ストア向け | 2026年1月1日以降、Admin経由での新規作成不可。Dev Dashboard経由に移行 |
| **Custom App（Dev Dashboard作成）** | クライアントクレデンシャルグラント方式。トークン有効期限24時間 | 今後の標準。単一ストア向けカスタム連携に最適 |
| **Public App** | OAuth 2.0フロー。複数ストアへの配布可能 | 2025年4月以降、GraphQL必須。App Storeレビューが必要 |

**EC事業者向けサービスとしての推奨:**
- **初期MVP（特定クライアント向け）**: Custom App（Dev Dashboard作成）が最適
- **スケール時（複数クライアント対応）**: Public Appへの移行を検討

---

## 2. ユースケース別 技術的実現性評価

| ユースケース | 実現性 | 必要なAPI/サービス | 工数目安（Claude Code活用） | 備考 |
|-------------|--------|-------------------|--------------------------|------|
| a) 商品説明文の自動生成/改善 | ★★★★★ | Admin API (Products) + Claude API | 2-3日 | 最もROI高い。即座に価値を示せる |
| b) 売上データ分析ダッシュボード | ★★★★☆ | Admin API (Orders) + GA4 | 5-7日 | Orders APIの60日制限に注意 |
| c) 顧客セグメント分析（RFM/LTV） | ★★★★☆ | Admin API (Customers, Orders) | 3-5日 | `read_all_orders`スコープが必要 |
| d) 在庫最適化アラート | ★★★☆☆ | Admin API (Inventory) + Webhooks | 3-5日 | 在庫回転率算出にはOrders連携必須 |
| e) 広告パフォーマンス分析 | ★★☆☆☆ | Meta CAPI, Google Ads API, Shopify外部 | 7-10日 | Shopify API単体では不十分。外部API連携必須 |
| f) チャットボット/FAQ自動生成 | ★★★☆☆ | Storefront API + Claude API | 5-7日 | Shopify Inboxは外部APIなし。独自構築が必要 |

### a) 商品説明文の自動生成/改善

**技術的実現方法:**

1. **データ取得**: Admin GraphQL APIで`products`クエリにより商品情報（title, descriptionHtml, images, variants, product_type, tags）を取得
2. **AI処理**: Claude APIに商品データを渡し、SEO最適化された説明文を生成
3. **画像認識**: Claude Vision APIで商品画像を解析し、視覚的特徴を説明文に反映
4. **一括更新**: `productUpdate`ミューテーションで`descriptionHtml`を更新

**一括更新の方法:**
- 少量（〜100商品）: 個別の`productUpdate`ミューテーションをループ実行（レート制限内で十分対応可能）
- 大量（100商品以上）: バルクオペレーション（JSONL形式でアップロード → `bulkOperationRunMutation` → Webhook完了通知）

**実装の流れ:**
```
商品一覧取得（GraphQL） → 商品画像DL → Claude Vision解析 → 説明文生成 → descriptionHtml更新
```

**注意点:**
- バルクミューテーションはJSONLファイルの作成・アップロード・完了待ちのパイプラインが必要
- 商品画像はURL経由でClaude Vision APIに直接渡せるため、ダウンロード不要
- 更新前にプレビュー機能を設けてクライアント確認を挟むのが実運用上必須

### b) 売上データ分析ダッシュボード

**Orders APIから取得可能な分析指標:**
- 売上推移（日次/週次/月次）: `created_at`, `total_price`
- 商品別売上: `line_items`の`price`, `quantity`
- 平均注文額（AOV）: `total_price`の平均
- 顧客別売上: `customer`フィールドとの紐付け
- 地域別売上: `shipping_address`の`country`, `province`
- 割引利用率: `discount_codes`, `total_discounts`
- 返品・返金率: `refunds`フィールド
- フルフィルメント状況: `fulfillment_status`

**GA4連携の方法:**
- **Shopify Pixel（Web Pixel API）**: Shopify標準のイベントトラッキング基盤。カスタムPixelとしてGA4/GTMを設定可能
- **Google & YouTube Channel App**: 最も簡易な連携方法。GA4プロパティを接続するだけ
- **カスタムPixel + GTM**: `analytics.subscribe()`でShopifyイベントをGTMデータレイヤーに送信。高度なカスタマイズ可能
- **注意**: カスタムPixelはサンドボックス化されたiFrame内で動作するため、一部の自動検出機能が制限される

**ROAS算出に必要なデータソース:**
- 売上データ: Shopify Orders API
- 広告費データ: Meta Ads API / Google Ads API（Shopify外部）
- ROAS = 売上 ÷ 広告費（クロスプラットフォームの集計が必要）

**Shopify API単体でのROAS算出は不可**。広告プラットフォームのAPIと組み合わせる必要がある。

### c) 顧客セグメント分析（RFM/LTV）

**RFM分析の実現可能性: 高い**

必要なデータはすべてAdmin APIから取得可能:
- **Recency**: 各顧客の最終注文日（`orders`クエリで`sortKey: CREATED_AT`）
- **Frequency**: 顧客の`orders_count`、またはOrders APIで注文回数を集計
- **Monetary**: `total_spent`フィールド、またはGraphQLの`lifetimeSpendAndOrderCount`

**LTV自動算出の実装:**
```
LTV = AOV × 購入頻度 × 顧客寿命
```
- AOV: 顧客の全注文の`total_price`平均
- 購入頻度: 一定期間内の注文回数
- 顧客寿命: 初回注文〜最終注文の期間

**実装上の注意:**
- `read_all_orders`スコープが必須（60日制限を超えるため）。Shopifyによる審査あり
- 初回は全注文データのバルク取得（`bulkOperationRunQuery`）が効率的
- 以降はWebhook（`orders/create`）でリアルタイム更新
- セグメント結果をShopify顧客タグに反映可能（`customerUpdate`ミューテーション）

### d) 在庫最適化アラート

**在庫回転率の自動計算:**
- 在庫回転率 = 売上原価 ÷ 平均在庫
- 必要データ: InventoryLevel（現在庫）+ Orders（販売数量）+ Product（原価情報）
- Shopify APIでは売上原価（COGS）が直接取得しにくい場合がある。`inventoryItem`の`cost`フィールドで仕入原価は取得可能

**発注タイミング予測:**
- 過去の販売速度（日次/週次の販売数量）を計算
- 現在庫 ÷ 平均日次販売数 = 在庫日数
- リードタイム（手動設定）と比較してアラート発火

**Webhook活用:**
- `inventory_levels/update`: 在庫変動時にリアルタイム通知
- `orders/create`: 新規注文時に在庫影響を即時計算

**制約:**
- 在庫の`committed`状態はAPIで操作不可
- リードタイムや発注ロットサイズはShopify APIに存在しないため、別途マスタデータとして管理が必要

### e) 広告パフォーマンス分析

**Shopify APIだけでは実現困難**。以下の外部連携が必須:

| データソース | 取得方法 | 取得できるデータ |
|------------|---------|----------------|
| **Meta Ads** | Meta Marketing API / Conversions API | 広告費、インプレッション、クリック、コンバージョン |
| **Google Ads** | Google Ads API | 広告費、クリック、CPC、コンバージョン |
| **Shopify** | Orders API | 実売上、注文、顧客データ |

**Shopify側の連携機能:**
- **Shopify Audiences**: Shopify Plus限定。顧客行動データからMeta/Google向けの高精度オーディエンスを自動生成
- **Meta Conversions API（CAPI）**: サーバーサイドでコンバージョンデータをMetaに送信。Pixelと併用で精度向上
- **Google Data Manager連携**: サーバー間通信でコンバージョンシグナルを回復（現時点では「Checkout complete」イベントのみ対応）

**実装の現実的なアプローチ:**
- Shopify Orders APIで売上データ取得 + 各広告プラットフォームAPIで広告費取得 → クロス集計
- 初期MVPではCSVインポート（手動）でも実用的

### f) チャットボット/FAQ自動生成

**過去の問い合わせデータ取得:**
- **Shopify Inbox**: 外部向けAPIは提供されていない。データのエクスポート機能も限定的
- **代替手段**: メール問い合わせ（Gmailなど）のAPI連携、またはZendesk/Freshdesk等のヘルプデスクツールからのデータ取得

**FAQ自動生成の実現方法:**
1. 商品データ（Products API）+ ストアポリシー（手動入力 or Shop API）をナレッジベースとして構築
2. Claude APIで質問応答システムを構築
3. Storefront APIまたはShopifyテーマのApp Embed Blockとしてチャットウィジェットを配置

**Shopify App Embed Block:**
- テーマに組み込めるウィジェットとして、チャットボットUIをShopifyストアに追加可能
- Shopify App Extensionsの仕組みを利用

**制約:**
- Shopify Inboxとの直接API連携は不可
- 独自チャットボットを構築する場合、会話ログの保存・管理は自前で実装が必要
- 顧客の注文状況参照にはAdmin API連携（サーバーサイド）が必要

---

## 3. 推奨技術スタック

### 3.1 最小構成MVP（推奨）

| レイヤー | 技術選択 | 理由 |
|---------|---------|------|
| **言語** | TypeScript | Shopify公式SDKとの親和性、型安全性 |
| **フレームワーク** | Next.js 15 (App Router) | SSR/API Routes統合、Vercelデプロイ容易 |
| **Shopify SDK** | `@shopify/shopify-api` (Node.js) | 公式ライブラリ。認証・GraphQLクライアント統合 |
| **AI** | Anthropic Claude API (`@anthropic-ai/sdk`) | 高品質な日本語テキスト生成、Vision対応 |
| **DB** | PostgreSQL (Supabase or Neon) | サーバーレス対応、無料枠あり |
| **ORM** | Prisma | 型安全なDB操作、マイグレーション管理 |
| **認証** | Shopify OAuth (Custom App) | Shopify標準の認証フロー |
| **ホスティング** | Vercel | Next.jsとの最適化、無料枠で開始可能 |
| **ジョブキュー** | Vercel Cron + Edge Functions | 定期実行タスク（分析更新、アラート等） |
| **通知** | Slack Webhook / Email (Resend) | アラート通知用 |

### 3.2 Claude API + Shopify API 連携アーキテクチャ

```
┌─────────────┐     ┌──────────────────┐     ┌───────────────┐
│  クライアント  │────▶│  Next.js API     │────▶│ Shopify Admin │
│  (ブラウザ)   │◀────│  Routes          │◀────│ GraphQL API   │
└─────────────┘     │                  │     └───────────────┘
                    │  ┌────────────┐  │
                    │  │ Claude API │  │     ┌───────────────┐
                    │  │ (Anthropic)│  │────▶│  PostgreSQL   │
                    │  └────────────┘  │◀────│  (Supabase)   │
                    └──────────────────┘     └───────────────┘
                           │
                    ┌──────┴──────┐
                    │  Webhooks   │
                    │ (orders/    │
                    │  inventory) │
                    └─────────────┘
```

**データフロー:**
1. クライアントがNext.js API Routeにリクエスト
2. API RouteがShopify Admin GraphQL APIからデータ取得
3. 取得データをClaude APIに送信（説明文生成、分析等）
4. 結果をDBに保存し、クライアントに返却
5. Webhookで注文・在庫変動をリアルタイム受信し、DB更新

### 3.3 代替構成（Python）

Python技術者の場合の代替スタック:
- **フレームワーク**: FastAPI
- **Shopify連携**: `shopify-python-api`（公式）または直接GraphQLリクエスト
- **AI**: `anthropic` Python SDK
- **DB**: SQLAlchemy + PostgreSQL
- **ホスティング**: Railway / Render / Fly.io
- **フロントエンド**: Streamlit（プロトタイプ用）

### 3.4 ホスティング・インフラ比較

| サービス | 月額コスト目安 | 特徴 |
|---------|-------------|------|
| **Vercel** | 無料〜$20 | Next.js最適化、Edge Functions |
| **Railway** | $5〜$20 | 簡単デプロイ、DBホスティング込み |
| **Render** | 無料〜$25 | フルスタック対応、無料DBあり |
| **Fly.io** | $5〜$15 | エッジデプロイ、コンテナベース |
| **Supabase（DB）** | 無料〜$25 | PostgreSQL + Auth + Realtime |

---

## 4. MVPプロトタイプ設計

### 4.1 Phase 0: MVP最小機能セット

**コンセプト: 「AI商品説明文ジェネレーター + 売上概要ダッシュボード」**

最もROIが高く、デモ映えする2機能に絞る:

#### 機能1: AI商品説明文の自動生成・改善
- Shopifyストア接続（OAuth認証）
- 商品一覧の取得・表示
- 選択した商品の説明文をClaude AIで自動生成
- 商品画像のClaude Vision解析による説明文強化
- 生成結果のプレビューと編集
- ワンクリックでShopifyに反映（`productUpdate`）

#### 機能2: 売上概要ダッシュボード
- 直近30日の売上推移グラフ
- 商品別売上ランキング（Top 10）
- AOV（平均注文額）の推移
- 簡易的なAIインサイト（Claude APIで売上傾向を自然言語で要約）

### 4.2 開発工数見積もり（Claude Code最大活用）

| タスク | 従来工数 | Claude Code活用時 |
|--------|---------|------------------|
| プロジェクト初期セットアップ（Next.js + Shopify OAuth） | 2日 | 0.5日 |
| Shopify GraphQL連携（商品・注文取得） | 3日 | 1日 |
| AI商品説明文生成機能 | 3日 | 1日 |
| Claude Vision連携（画像解析） | 2日 | 0.5日 |
| 売上ダッシュボードUI | 3日 | 1日 |
| AIインサイト生成 | 1日 | 0.5日 |
| テスト・デバッグ・調整 | 3日 | 1.5日 |
| **合計** | **17日** | **6日** |

**前提:**
- 開発者がShopify API / Next.jsの基本知識を持っている
- Claude Codeでコード生成・デバッグ・テスト作成を最大活用
- 1日 = 実稼働4-5時間想定
- 合計約30時間の人間稼働でMVP完成見込み

### 4.3 MVP画面構成

```
1. ログイン画面（Shopify OAuth）
2. ダッシュボード
   ├── 売上概要（グラフ + AIサマリー）
   └── クイックアクション
3. 商品管理
   ├── 商品一覧（Shopifyから同期）
   ├── AI説明文生成（個別）
   └── 一括生成（バッチ処理）
4. 設定
   ├── Shopify接続管理
   └── AI生成設定（トーン、ターゲット層等）
```

---

## 5. 開発ロードマップ

### Phase 0: MVP（1-2週間）
- Shopify OAuth連携の実装
- AI商品説明文生成機能
- 簡易売上ダッシュボード
- **目標**: デモ可能なプロトタイプの完成。1-2社のEC事業者にデモして反応を検証

### Phase 1: コア機能拡充（2-3週間）
- 顧客セグメント分析（RFM）の追加
- LTV自動算出
- Webhook連携（注文・在庫のリアルタイム同期）
- バッチ処理の安定化（エラーハンドリング、リトライ）
- **目標**: 有料テストユーザー（2-3社）の獲得

### Phase 2: 分析強化（3-4週間）
- 在庫最適化アラート
- 売上予測（過去データに基づくトレンド分析）
- GA4連携（Custom Pixel経由）
- レポート自動生成（月次/週次）
- **目標**: 月額課金モデルの確立

### Phase 3: エコシステム連携（4-6週間）
- Meta Ads / Google Ads連携（ROAS分析）
- チャットボット/FAQ生成機能
- マルチストア対応
- Public App化（Shopify App Store申請）
- **目標**: スケーラブルなSaaSへの移行

### 各フェーズの収益性見通し

| フェーズ | 提供形態 | 想定単価 | 実質時給目安 |
|---------|---------|---------|------------|
| Phase 0 | 初期設定+説明文生成代行 | ¥50,000-100,000/回 | ¥15,000-30,000/h |
| Phase 1 | 月額コンサル+ツール提供 | ¥30,000-50,000/月 | ¥15,000-25,000/h（安定後） |
| Phase 2 | SaaSツール+分析レポート | ¥50,000-100,000/月 | ¥20,000-50,000/h |
| Phase 3 | SaaS + セルフサーブ | ¥10,000-30,000/月×多数 | スケーラブル |

---

## 補足: Shopify MCP Server

Shopifyは公式のDev MCP Serverを提供しており、Claude CodeやCursorなどのAI開発ツールから直接ShopifyのAPIドキュメントにアクセスし、コード生成の精度を高めることが可能。開発時にはこのMCP Serverの活用を推奨する。

```bash
# Claude CodeへのShopify MCP Server追加
claude mcp add shopify-dev-mcp -- npx -- -y @anthropic-ai/claude-code-mcp@latest
```

---

## 調査情報源

- [Shopify API Rate Limits](https://shopify.dev/docs/api/usage/limits)
- [GraphQL Admin API Reference](https://shopify.dev/docs/api/admin-graphql/latest)
- [REST Admin API Rate Limits](https://shopify.dev/docs/api/admin-rest/usage/rate-limits)
- [productUpdate Mutation](https://shopify.dev/docs/api/admin-graphql/latest/mutations/productUpdate)
- [Bulk Operations Guide](https://shopify.dev/docs/api/usage/bulk-operations/queries)
- [Storefront API Reference](https://shopify.dev/docs/api/storefront/latest)
- [Shopify API Authentication](https://shopify.dev/docs/api/usage/authentication)
- [InventoryLevel (GraphQL)](https://shopify.dev/docs/api/admin-graphql/latest/objects/InventoryLevel)
- [InventoryItem (GraphQL)](https://shopify.dev/docs/api/admin-graphql/latest/objects/InventoryItem)
- [Shopify Inventory API Explained (2026)](https://www.prediko.io/blog/shopify-inventory-api)
- [Shopify Custom App Deprecation 2026](https://datronixtech.com/shopify-custom-app-deprecation/)
- [Shopify Conversion API](https://www.shopify.com/blog/conversion-api)
- [Shopify Dev MCP Server](https://shopify.dev/docs/apps/build/devmcp)
- [Build a Storefront AI Agent](https://shopify.dev/docs/apps/build/storefront-mcp/build-storefront-ai-agent)
- [Shopify GA4 Custom Pixel](https://help.shopify.com/en/manual/promoting-marketing/pixels/custom-pixels/gtm-tutorial)
- [Shopify Customer LTV](https://www.shopify.com/blog/customer-lifetime-value)
