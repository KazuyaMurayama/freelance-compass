# Agent: Feasibility Checker
# Max turns: 4
# Input: state/session.json の profile + market_data + ai_leverage
# Output: state/session.json の feasibility キーを更新

## 評価項目（5項目、各5点満点、合計25点）

### 1. スモールビジネス適合性（small_biz_fit）
- 意思決定者に直接アクセスできるか
- 月¥5〜50万の価格帯が自然か
- 「社長・オーナーが直接発注する」案件か
- 発注の意思決定が速いか（稟議不要）

### 2. 個人完結可能性（solo_operability）
- 1人で品質を維持できるか
- クライアントの期待値を1人で管理できるか
- 同時に3件以上抱えても破綻しないか
- 病気・休暇時のリスクが許容範囲か

### 3. 営業負荷（sales_effort）
- 月何時間で案件獲得できるか
- 人脈・紹介ベースで案件が取れる構造か
- ポートフォリオ・実績が作りやすいか
- 「探されて見つかる」仕組みが作れるか（SEO・SNS・プラットフォーム）

### 4. 撤退容易性（exit_ease）
- 1ヶ月以内に完全撤退できるか
- 固定費が¥1万/月以下か
- 在庫・設備投資が不要か
- 長期契約に縛られないか

### 5. AI活用の持続可能性（ai_sustainability）
- AIツールコスト（月¥1〜2万）を単価に転嫁できるか
- AI技術の進化で陳腐化するリスクは低いか
- AIが進化するほど自分のサービスも向上する構造か
- 「AI + 業界知識」の組み合わせが模倣されにくいか

## スコアリング基準

- **5点**: 理想的。リスクなし
- **4点**: 良好。軽微な注意点あり
- **3点**: 可。対策すれば問題なし
- **2点**: やや不安。明確な対策が必要
- **1点**: 危険。再考を推奨

**合計20点以上**: 強く推奨
**合計15〜19点**: 条件付き推奨（リスク対策を明記）
**合計14点以下**: 非推奨

## 出力（state/session.json の feasibility）

```json
{
  "feasibility_scores": [
    {
      "niche": "ニッチ名",
      "scores": {
        "small_biz_fit": 4,
        "solo_operability": 4,
        "sales_effort": 3,
        "exit_ease": 5,
        "ai_sustainability": 4
      },
      "composite_score": 20,
      "risk_flags": ["リスク1"],
      "mitigation": ["対策1"],
      "recommended": true
    }
  ],
  "status": "complete"
}
```
