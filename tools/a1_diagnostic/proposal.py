"""
A1 提案生成モジュール
Claude API連携版 + フォールバック（テンプレート版）
"""

import anthropic


# ===== テンプレート提案（API不使用時のフォールバック） =====

JOB_PROPOSALS = {
    "商品PG高速化": [
        ("AI商品ページ一括生成",
         "商品タイトル・説明文・SEOメタをClaude APIで自動生成。"
         "現在60分/件 → 10分/件を目標に、月20件で16時間の削減効果。"),
        ("A/Bテスト自動化",
         "商品説明の2パターンをAIで生成し、ShopifyのネイティブA/B機能でCVR比較。"
         "データに基づいた改善サイクルを月次で回せるようになります。"),
        ("画像altテキスト自動付与",
         "全商品画像のalt属性をAIで一括生成。SEO効果 + アクセシビリティ向上。"
         "既存商品100件の一括対応も可能です。"),
    ],
    "広告最適化": [
        ("ROAS改善ダッシュボード",
         "Meta / Google / Shopify Adsのデータを統合し、"
         "週次でROAS最適化アドバイスを自動生成します。"),
        ("広告コピーAI生成",
         "商品ページのデータからMeta広告の見出し・本文を自動生成。"
         "ABテスト用に5パターンを即座に作成できます。"),
        ("除外キーワード自動洗い出し",
         "検索クエリレポートからAIで不要キーワードを特定。"
         "無駄な広告費を月次で削減します。"),
    ],
    "LTV改善": [
        ("リピート予測モデル",
         "購入履歴から「次回購入確率が高い顧客」をAIで特定し、"
         "優先フォローリストを自動生成します。"),
        ("パーソナライズメール自動化",
         "購買パターン別にKlaviyoのメールシーケンスをAI設計。"
         "セグメント別の開封率・CVR改善を狙います。"),
        ("離脱リスク顧客の早期検出",
         "購買間隔の変化からLTV低下リスクをアラート。"
         "解約前にフォローアクションを取れます。"),
    ],
    "業務自動化": [
        ("問い合わせ自動分類 + テンプレ回答",
         "CSメールをAIで分類し、回答テンプレを自動提示。"
         "対応時間70%削減を目標とします。"),
        ("在庫補充アラート自動化",
         "販売速度 × 在庫数からAIが適切な発注タイミングをSlack通知。"
         "欠品・過剰在庫のリスクを低減します。"),
        ("月次レポート自動生成",
         "売上・広告・CS指標を統合したPDFレポートをAIが自動作成。"
         "毎月の振り返りを30分→5分に短縮します。"),
    ],
}

HOUR_ESTIMATES = {
    "商品PG高速化": (20, 4),   # (current_hours, after_hours)
    "広告最適化":   (15, 5),
    "LTV改善":     (10, 4),
    "業務自動化":   (25, 5),
}


def generate_proposal_fallback(answers: dict, scores: dict, shop_name: str) -> str:
    """テンプレートベースの提案生成（Claude API不使用）"""
    job = scores.get("job_priority", "商品PG高速化")
    proposals = JOB_PROPOSALS.get(job, JOB_PROPOSALS["商品PG高速化"])
    cur_h, aft_h = HOUR_ESTIMATES.get(job, (15, 5))
    saved_h = cur_h - aft_h
    saved_value = saved_h * 5000

    lines = [f"### {shop_name}様への改善提案: 「{job}」\n"]
    for i, (title, desc) in enumerate(proposals, 1):
        lines.append(f"**施策{i}: {title}**\n{desc}\n")

    lines.append(f"""
---
### ROI試算

| 項目 | 現状 | AI導入後（3ヶ月目標） |
|------|------|-------------------|
| {job}にかかる月次工数 | 推定{cur_h}時間 | {aft_h}時間 |
| 削減効果（時給¥5,000換算） | — | ¥{saved_value:,}/月 |
| AI実装パートナー費用 | — | 月額¥50,000〜 |
| **月次ROI** | — | **+¥{saved_value - 50000:,}** |
""")
    return "\n".join(lines)


def generate_proposal_with_ai(
    answers: dict,
    scores: dict,
    shop_name: str,
    industry: str,
    api_key: str,
) -> str:
    """Claude APIを使った提案生成"""
    job = scores.get("job_priority", "商品PG高速化")
    cat_summary = "\n".join(
        f"- {cat}: {avg:.1f}/4.0"
        for cat, avg in scores["category_avg"].items()
    )

    prompt = f"""あなたはEC事業者向けのAI活用コンサルタントです。
以下の診断結果を元に、{shop_name}様（{industry}）への具体的なAI改善提案を作成してください。

## 診断結果
- 総合スコア: {scores['percentage']}%（{scores['tier']}）
- AI活用レディネス: {scores['ai_readiness']}
- 優先ジョブ: {job}
- カテゴリ別:
{cat_summary}

## 出力ルール
1. 最優先ジョブ「{job}」に関する具体施策を3つ提案
2. 各施策には「何をするか」「期待効果」「実装難易度」を含める
3. ROI試算を含める（時給¥5,000換算）
4. 専門用語は避け、中小EC事業者が理解できる平易な言葉で
5. Markdown形式で出力
6. 最後に次のステップ（有償診断¥30,000の案内）を自然に含める
"""

    try:
        client = anthropic.Anthropic(api_key=api_key)
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}],
        )
        return message.content[0].text
    except Exception as e:
        # API失敗時はフォールバック
        fallback = generate_proposal_fallback(answers, scores, shop_name)
        return fallback + f"\n\n*（注: AI詳細分析は一時的に利用できません。テンプレート版を表示しています）*"
