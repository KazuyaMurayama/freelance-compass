"""
A1: AI経営診断ツール — 最小プロトタイプ
EC事業者向け10問診断 → AIスコアリング → 改善提案テキスト出力

Day 0 実測用: このファイルを作成・実行して工数を計測する
スコープ: Streamlit UI + 診断ロジック + 提案テキスト生成（Claude API連携は省略しスタブで代替）
"""

import time
from datetime import datetime

# ===== 診断質問定義 =====

QUESTIONS = [
    {
        "id": "Q1",
        "text": "Shopifyでの月商はいくらですか？",
        "options": [
            ("A", "¥100万未満"),
            ("B", "¥100-300万"),
            ("C", "¥300-1,000万"),
            ("D", "¥1,000万以上"),
        ],
        "weights": {"A": 1, "B": 2, "C": 3, "D": 4},
        "category": "規模",
    },
    {
        "id": "Q2",
        "text": "商品ページ（タイトル・説明文・画像alt）の更新頻度は？",
        "options": [
            ("A", "ほぼ更新しない（月1回以下）"),
            ("B", "月2-4回"),
            ("C", "週1-2回"),
            ("D", "週3回以上"),
        ],
        "weights": {"A": 1, "B": 2, "C": 3, "D": 4},
        "category": "コンテンツ運用",
    },
    {
        "id": "Q3",
        "text": "現在、AIツール（ChatGPT等）を業務に使っていますか？",
        "options": [
            ("A", "全く使っていない"),
            ("B", "試したことはある程度"),
            ("C", "定期的に使っている（週数回）"),
            ("D", "業務の中心にAIを組み込んでいる"),
        ],
        "weights": {"A": 1, "B": 2, "C": 3, "D": 4},
        "category": "AI習熟度",
    },
    {
        "id": "Q4",
        "text": "広告（Meta/Google/Shopify Ads）の月次予算は？",
        "options": [
            ("A", "¥10万未満 または 運用していない"),
            ("B", "¥10-50万"),
            ("C", "¥50-200万"),
            ("D", "¥200万以上"),
        ],
        "weights": {"A": 1, "B": 2, "C": 3, "D": 4},
        "category": "広告投資",
    },
    {
        "id": "Q5",
        "text": "Shopifyのデータ分析（Shopify Analytics / GA4等）を定期的に見ていますか？",
        "options": [
            ("A", "ほぼ見ていない"),
            ("B", "売上だけは確認している"),
            ("C", "コンバージョン率や離脱率も確認している"),
            ("D", "コホート分析・LTV分析まで実施している"),
        ],
        "weights": {"A": 1, "B": 2, "C": 3, "D": 4},
        "category": "データ活用",
    },
    {
        "id": "Q6",
        "text": "商品ページ作成に1件あたり何分かかりますか？",
        "options": [
            ("A", "60分以上"),
            ("B", "30-60分"),
            ("C", "15-30分"),
            ("D", "15分未満"),
        ],
        "weights": {"A": 4, "B": 3, "C": 2, "D": 1},  # 逆スコア（時間が短い=改善済み）
        "category": "業務効率",
        "reverse": True,
    },
    {
        "id": "Q7",
        "text": "カスタマーサポート（問い合わせ対応）にかける時間は週何時間？",
        "options": [
            ("A", "10時間以上"),
            ("B", "5-10時間"),
            ("C", "2-5時間"),
            ("D", "2時間未満（自動化済み）"),
        ],
        "weights": {"A": 4, "B": 3, "C": 2, "D": 1},  # 逆スコア
        "category": "業務効率",
        "reverse": True,
    },
    {
        "id": "Q8",
        "text": "リピート率（2回以上購入した顧客の割合）はどのくらいですか？",
        "options": [
            ("A", "把握していない"),
            ("B", "20%未満"),
            ("C", "20-40%"),
            ("D", "40%以上"),
        ],
        "weights": {"A": 1, "B": 2, "C": 3, "D": 4},
        "category": "顧客定着",
    },
    {
        "id": "Q9",
        "text": "新規顧客の獲得単価（CPA）を把握していますか？",
        "options": [
            ("A", "全く把握していない"),
            ("B", "おおよその感覚はある"),
            ("C", "月次で計算している"),
            ("D", "週次以上の頻度で管理し、施策に反映している"),
        ],
        "weights": {"A": 1, "B": 2, "C": 3, "D": 4},
        "category": "データ活用",
    },
    {
        "id": "Q10",
        "text": "今後6ヶ月で最も強化したい領域は？",
        "options": [
            ("A", "商品ページ・コンテンツの質"),
            ("B", "広告・集客効率"),
            ("C", "リピート率・LTV向上"),
            ("D", "業務効率化・自動化"),
        ],
        "weights": {"A": 1, "B": 2, "C": 3, "D": 4},  # 全て同スコア（意図確認）
        "category": "優先ジョブ",
        "special": "job_priority",
    },
]

# ===== スコアリングロジック =====

def calculate_scores(answers: dict) -> dict:
    """回答からスコアを計算する"""
    total_score = 0
    category_scores = {}
    job_priority = None

    for q in QUESTIONS:
        qid = q["id"]
        if qid not in answers:
            continue
        answer = answers[qid]
        score = q["weights"].get(answer, 0)

        # 特殊処理: Q10は優先ジョブの特定のみ
        if q.get("special") == "job_priority":
            job_map = {"A": "商品PG高速化", "B": "広告最適化", "C": "LTV改善", "D": "業務自動化"}
            job_priority = job_map.get(answer, "未回答")
            continue

        total_score += score
        cat = q["category"]
        if cat not in category_scores:
            category_scores[cat] = []
        category_scores[cat].append(score)

    # カテゴリ平均
    category_avg = {
        cat: sum(scores) / len(scores)
        for cat, scores in category_scores.items()
    }

    # 最大スコア（Q10除く9問 × 最大4点）
    max_score = 9 * 4
    percentage = (total_score / max_score) * 100

    # AI活用レベル判定
    if percentage >= 75:
        ai_readiness = "高（AI活用の素地あり。高度な自動化に取り組める）"
        tier = "Advanced"
    elif percentage >= 50:
        ai_readiness = "中（基礎は整っている。特定領域からAI導入を開始すべき）"
        tier = "Intermediate"
    elif percentage >= 25:
        ai_readiness = "低（まず業務の可視化・標準化から始める必要がある）"
        tier = "Beginner"
    else:
        ai_readiness = "最低（現状把握から始める必要がある）"
        tier = "Starter"

    return {
        "total_score": total_score,
        "max_score": max_score,
        "percentage": round(percentage, 1),
        "tier": tier,
        "ai_readiness": ai_readiness,
        "category_avg": category_avg,
        "job_priority": job_priority,
    }


# ===== 提案テキスト生成（スタブ — Claude API未使用） =====

def generate_proposal(answers: dict, scores: dict, shop_name: str = "貴店") -> str:
    """スコアと回答から改善提案テキストを生成する"""

    tier = scores["tier"]
    job = scores.get("job_priority", "商品PG高速化")
    pct = scores["percentage"]
    cat_avg = scores["category_avg"]

    # 最もスコアが低いカテゴリを特定
    weakest = min(cat_avg.items(), key=lambda x: x[1]) if cat_avg else ("不明", 0)
    strongest = max(cat_avg.items(), key=lambda x: x[1]) if cat_avg else ("不明", 0)

    # 優先ジョブ別の具体提案
    job_proposals = {
        "商品PG高速化": [
            "**AI商品ページ一括生成**: 商品タイトル・説明文・SEOメタをClaude APIで自動生成。現在60分/件→10分/件を目標",
            "**A/Bテスト自動化**: 商品説明の2パターンをAIで生成し、Shopifyのネイティブ機能でCVR比較",
            "**画像altテキスト自動付与**: 全商品画像のalt属性をAIで一括生成（SEO効果+アクセシビリティ）",
        ],
        "広告最適化": [
            "**ROAS改善ダッシュボード**: Meta/Google/Shopify Adsのデータを統合し、週次でROAS最適化アドバイスを自動生成",
            "**広告コピーAI生成**: 商品ページのデータからMeta広告の見出し・本文を自動生成（ABテスト用に5パターン）",
            "**除外キーワード自動洗い出し**: 検索クエリレポートからAIで不要キーワードを特定",
        ],
        "LTV改善": [
            "**リピート予測モデル**: 購入履歴から「次回購入確率が高い顧客」をAIで特定し、優先フォローリストを生成",
            "**パーソナライズメール自動化**: 購買パターン別にKlaviyoのメールシーケンスをAI設計",
            "**解約・離脱リスク顧客の早期検出**: 購買間隔の変化からLTV低下リスクをアラート",
        ],
        "業務自動化": [
            "**問い合わせ自動分類+テンプレ回答**: CSメールをAIで分類し、回答テンプレを自動提示（対応時間70%削減目標）",
            "**在庫補充アラート自動化**: 販売速度×在庫数からAIが適切な発注タイミングをSlack通知",
            "**月次レポート自動生成**: 売上・広告・CS指標を統合したPDFレポートをClaude Codeが自動作成",
        ],
    }

    proposals = job_proposals.get(job, job_proposals["商品PG高速化"])

    report = f"""
# AI経営診断レポート
## {shop_name} 様

**診断日**: {datetime.now().strftime('%Y年%m月%d日')}
**総合スコア**: {scores['total_score']}/{scores['max_score']}点（{pct}%）
**AI活用レディネス**: {tier}

---

## 診断サマリー

{scores['ai_readiness']}

| 評価カテゴリ | スコア（1-4） | 評価 |
|------------|------------|------|
"""
    for cat, avg in cat_avg.items():
        bar = "●" * int(avg) + "○" * (4 - int(avg))
        level = "優秀" if avg >= 3.5 else "良好" if avg >= 2.5 else "要改善" if avg >= 1.5 else "緊急改善"
        report += f"| {cat} | {avg:.1f} [{bar}] | {level} |\n"

    report += f"""
**最優先改善カテゴリ**: {weakest[0]}（スコア: {weakest[1]:.1f}）
**強みカテゴリ**: {strongest[0]}（スコア: {strongest[1]:.1f}）

---

## あなたの優先ジョブ: 「{job}」

診断結果から、{shop_name}様が今最も強化すべき領域は **{job}** です。
以下の3つのAI施策を段階的に導入することをお勧めします。

"""
    for i, prop in enumerate(proposals, 1):
        report += f"### 施策{i}: {prop}\n\n"

    report += f"""
---

## 実質時給の試算

| 項目 | 現状 | AI導入後（3ヶ月目標） |
|------|------|-------------------|
| {job}にかかる月次工数 | 推定{_estimate_current_hours(job)}時間 | {_estimate_after_hours(job)}時間（AI代替） |
| 浮いた時間の価値（時給¥5,000換算） | — | ¥{_estimate_value(job):,}/月 |
| AI導入コスト | — | 月額¥50,000〜（コンサル費込） |
| **実質ROI** | — | **{_estimate_roi(job)}%** |

---

## 次のステップ

1. **今すぐ（無料）**: AI診断レポートをお持ちください → [無料相談を申し込む]
2. **Phase 1（1ヶ月目）**: 最優先施策1つをパイロット実施
3. **Phase 2（2-3ヶ月目）**: 効果を確認しながら施策2・3を展開

**問い合わせ**: [LP・問い合わせフォームへ]

---
*本レポートはAI経営パートナーの診断システムによって自動生成されました*
*© 2026 AI経営パートナー*
"""
    return report


def _estimate_current_hours(job: str) -> int:
    mapping = {"商品PG高速化": 20, "広告最適化": 15, "LTV改善": 10, "業務自動化": 25}
    return mapping.get(job, 15)

def _estimate_after_hours(job: str) -> int:
    mapping = {"商品PG高速化": 4, "広告最適化": 5, "LTV改善": 4, "業務自動化": 5}
    return mapping.get(job, 5)

def _estimate_value(job: str) -> int:
    hours = _estimate_current_hours(job) - _estimate_after_hours(job)
    return hours * 5000

def _estimate_roi(job: str) -> int:
    value = _estimate_value(job)
    cost = 50000
    return int(((value - cost) / cost) * 100) if cost > 0 else 0


# ===== CUIテスト実行（Streamlit省略版） =====

def run_demo():
    """架空のShopify店舗「月商600万・アパレル」でデモ実行"""
    print("=== A1診断ツール デモ実行 ===")
    print("架空店舗: アパレルEC「DEMO STORE」/ Shopify / 月商600万")
    print()

    # 架空回答（月商600万・アパレル・AI未活用・商品PG作成が課題）
    demo_answers = {
        "Q1": "C",  # 月商300-1,000万
        "Q2": "B",  # 月2-4回更新
        "Q3": "B",  # 試したことある程度
        "Q4": "B",  # 広告月10-50万
        "Q5": "B",  # 売上だけ確認
        "Q6": "A",  # 商品PG60分以上
        "Q7": "B",  # CS週5-10時間
        "Q8": "B",  # リピート20%未満
        "Q9": "A",  # CPA把握していない
        "Q10": "A", # 優先ジョブ: 商品PG高速化
    }

    scores = calculate_scores(demo_answers)
    print(f"スコア: {scores['total_score']}/{scores['max_score']} ({scores['percentage']}%)")
    print(f"ティア: {scores['tier']}")
    print(f"優先ジョブ: {scores['job_priority']}")
    print(f"カテゴリ別: {scores['category_avg']}")
    print()

    report = generate_proposal(demo_answers, scores, "DEMO STORE")
    print(report)
    return report


if __name__ == "__main__":
    start = time.time()
    run_demo()
    elapsed = time.time() - start
    print(f"\n=== 実行時間: {elapsed:.2f}秒 ===")
