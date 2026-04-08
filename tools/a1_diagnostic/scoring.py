"""
A1 診断スコアリングモジュール
プロトタイプ(outputs/verification-v3/a1_diagnostic_prototype.py)から移植・整理
"""

QUESTIONS = [
    {
        "id": "Q1",
        "text": "Shopifyでの月商はいくらですか？",
        "options": [
            ("A", "¥100万未満"),
            ("B", "¥100〜300万"),
            ("C", "¥300〜1,000万"),
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
            ("B", "月2〜4回"),
            ("C", "週1〜2回"),
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
        "text": "広告（Meta / Google / Shopify Ads）の月次予算は？",
        "options": [
            ("A", "¥10万未満 または 運用していない"),
            ("B", "¥10〜50万"),
            ("C", "¥50〜200万"),
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
            ("B", "30〜60分"),
            ("C", "15〜30分"),
            ("D", "15分未満"),
        ],
        "weights": {"A": 4, "B": 3, "C": 2, "D": 1},
        "category": "業務効率",
        "reverse": True,
    },
    {
        "id": "Q7",
        "text": "カスタマーサポート（問い合わせ対応）にかける時間は週何時間？",
        "options": [
            ("A", "10時間以上"),
            ("B", "5〜10時間"),
            ("C", "2〜5時間"),
            ("D", "2時間未満（自動化済み）"),
        ],
        "weights": {"A": 4, "B": 3, "C": 2, "D": 1},
        "category": "業務効率",
        "reverse": True,
    },
    {
        "id": "Q8",
        "text": "リピート率（2回以上購入した顧客の割合）はどのくらいですか？",
        "options": [
            ("A", "把握していない"),
            ("B", "20%未満"),
            ("C", "20〜40%"),
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
        "weights": {"A": 1, "B": 2, "C": 3, "D": 4},
        "category": "優先ジョブ",
        "special": "job_priority",
    },
]


JOB_MAP = {
    "A": "商品PG高速化",
    "B": "広告最適化",
    "C": "LTV改善",
    "D": "業務自動化",
}


def calculate_scores(answers: dict) -> dict:
    """回答辞書 {"Q1": "C", ...} からスコアを計算"""
    total_score = 0
    category_scores: dict[str, list[int]] = {}
    job_priority = None

    for q in QUESTIONS:
        qid = q["id"]
        answer = answers.get(qid)
        if answer is None:
            continue

        score = q["weights"].get(answer, 0)

        if q.get("special") == "job_priority":
            job_priority = JOB_MAP.get(answer, "未回答")
            continue

        total_score += score
        cat = q["category"]
        category_scores.setdefault(cat, []).append(score)

    category_avg = {
        cat: round(sum(s) / len(s), 2)
        for cat, s in category_scores.items()
    }

    max_score = 9 * 4  # Q10除く9問 × 最大4点
    percentage = round((total_score / max_score) * 100, 1)

    if percentage >= 75:
        ai_readiness = "高 — AI活用の素地あり。高度な自動化に取り組める段階です。"
        tier = "Advanced"
    elif percentage >= 50:
        ai_readiness = "中 — 基礎は整っています。特定領域からAI導入を開始すべき段階です。"
        tier = "Intermediate"
    elif percentage >= 25:
        ai_readiness = "低 — まず業務の可視化・標準化から始める必要があります。"
        tier = "Beginner"
    else:
        ai_readiness = "最低 — 現状把握から始める必要があります。"
        tier = "Starter"

    return {
        "total_score": total_score,
        "max_score": max_score,
        "percentage": percentage,
        "tier": tier,
        "ai_readiness": ai_readiness,
        "category_avg": category_avg,
        "job_priority": job_priority,
    }
