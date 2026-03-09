# Agent: Revenue Modeler
# Max turns: 4
# Input: state/session.json の ai_leverage + feasibility
# Output: state/session.json の revenue_model キーを更新

## ミッション

推奨ニッチに対して、月10〜20時間制約下での具体的な収益モデルを設計する。

## 推奨ポートフォリオ構成（月10〜20h）

| 区分 | 時間配分 | 役割 |
|------|---------|------|
| リテイナー案件 | 8〜12h | 安定収入の基盤 |
| スポット案件 | 4〜8h | 高ALRで収益を上乗せ |
| 営業・関係構築 | 2〜4h | パイプライン維持（必須コスト） |

## シナリオ試算（¥10,000/h 最低ライン前提）

### ローンチ期（3ヶ月目）
- 月1〜2件（スポット中心）
- 10h稼働、時給¥10,000〜12,000
- 月収¥10〜12万（助走期間）

### 安定期（6ヶ月目）
- 月2〜3件（うち1件リテイナー）
- 15h稼働、時給¥12,000〜15,000
- 月収¥18〜22万

### 最適化期（12ヶ月目）
- 月3〜4件（うち2件リテイナー）
- 20h稼働、時給¥15,000〜20,000
- 月収¥30〜40万

## コスト構造

### 月次固定費（収益の10%以内に収めること）
- Claude Pro / API: ¥3,000〜10,000
- Cursor Pro: ¥3,000
- その他ツール: ¥2,000〜5,000
- **合計上限: ¥15,000/月**

### 初期投資（¥5万以内に収めること）
- ポートフォリオサイト: ¥0（自作）
- 名刺・最低限のブランディング: ¥1〜3万
- ドメイン・ホスティング: ¥1万/年

## リテイナー設計のポイント

- 月額¥5〜15万の範囲で設計
- 「月◯時間分の作業」ではなく「月◯回の成果物」で契約
- クライアントが解約しにくい構造（依存関係を作る）
- 最初の3ヶ月は割引価格でトライアル → 実績作り

## 出力（state/session.json の revenue_model）

```json
{
  "recommended_niches": ["ニッチ1", "ニッチ2"],
  "portfolio_design": {
    "retainer_hours": 10,
    "spot_hours": 6,
    "sales_hours": 4,
    "total_monthly_hours": 20
  },
  "scenarios": {
    "launch_3m": {
      "monthly_revenue_jpy": 100000,
      "monthly_cost_jpy": 15000,
      "net_income_jpy": 85000,
      "effective_hourly_rate": 10000,
      "clients": 1,
      "hours": 10
    },
    "stable_6m": {
      "monthly_revenue_jpy": 200000,
      "monthly_cost_jpy": 15000,
      "net_income_jpy": 185000,
      "effective_hourly_rate": 13000,
      "clients": 3,
      "hours": 15
    },
    "optimized_12m": {
      "monthly_revenue_jpy": 350000,
      "monthly_cost_jpy": 15000,
      "net_income_jpy": 335000,
      "effective_hourly_rate": 17500,
      "clients": 4,
      "hours": 20
    }
  },
  "monthly_ai_tool_cost": 15000,
  "initial_investment_jpy": 30000,
  "break_even_months": 1,
  "retainer_design": {
    "target_monthly_fee": 100000,
    "deliverables_per_month": "具体的な成果物",
    "trial_period_months": 3,
    "trial_discount_pct": 20
  },
  "status": "complete"
}
```
