"""
A1: AI経営診断ツール — Streamlit フル実装版
EC事業者向け10問診断 → AIスコアリング → Claude提案生成 → PDF出力

使い方:
  streamlit run tools/a1_diagnostic/app.py
"""

import os
import io
import streamlit as st
from datetime import datetime

from scoring import QUESTIONS, calculate_scores
from proposal import generate_proposal_with_ai, generate_proposal_fallback
from pdf_export import generate_pdf


# ===== ページ設定 =====
st.set_page_config(
    page_title="AI実装パートナー｜無料EC診断",
    page_icon="📊",
    layout="centered",
)

# ===== セッションステート初期化 =====
if "step" not in st.session_state:
    st.session_state.step = "intro"  # intro → questions → result
if "answers" not in st.session_state:
    st.session_state.answers = {}
if "shop_info" not in st.session_state:
    st.session_state.shop_info = {}


def show_intro():
    """イントロ画面"""
    st.title("EC事業 AI活用度 無料診断")
    st.markdown("""
    **10問・3分で完了** — あなたのShopifyストアのAI活用レベルを診断し、
    具体的な改善提案をレポートでお届けします。

    ### この診断でわかること
    - 📊 AI活用レディネススコア（4段階評価）
    - 🔍 5カテゴリ別の強み・弱み
    - 💡 あなたの優先課題に合わせたAI施策3選
    - 💰 導入によるROI試算

    ---
    """)

    with st.form("shop_info_form"):
        shop_name = st.text_input(
            "ストア名（任意・レポート表示用）",
            placeholder="例: My Apparel Shop",
        )
        industry = st.selectbox(
            "主な取扱商品",
            ["アパレル・ファッション", "コスメ・美容", "雑貨・インテリア",
             "食品・飲料", "健康・サプリ", "その他"],
        )
        submitted = st.form_submit_button("診断を開始する →", type="primary")

    if submitted:
        st.session_state.shop_info = {
            "name": shop_name or "あなたのストア",
            "industry": industry,
        }
        st.session_state.step = "questions"
        st.rerun()


def show_questions():
    """質問画面（10問を1ページで表示）"""
    shop = st.session_state.shop_info
    st.title(f"📋 {shop['name']} の診断")
    st.progress(0.5, text="10問中…回答してください")

    with st.form("diagnostic_form"):
        answers = {}
        for i, q in enumerate(QUESTIONS):
            st.markdown(f"**Q{i+1}. {q['text']}**")
            options = [opt[1] for opt in q["options"]]
            keys = [opt[0] for opt in q["options"]]
            choice = st.radio(
                f"Q{i+1}",
                options=options,
                key=f"q_{q['id']}",
                label_visibility="collapsed",
            )
            # 選択肢のテキストからキーを逆引き
            idx = options.index(choice)
            answers[q["id"]] = keys[idx]

            if i < len(QUESTIONS) - 1:
                st.divider()

        submitted = st.form_submit_button("診断結果を見る →", type="primary")

    if submitted:
        st.session_state.answers = answers
        st.session_state.step = "result"
        st.rerun()


def show_result():
    """結果画面"""
    answers = st.session_state.answers
    shop = st.session_state.shop_info
    shop_name = shop["name"]
    industry = shop["industry"]

    # スコア計算
    scores = calculate_scores(answers)

    st.title("📊 診断結果")

    # ===== サマリーカード =====
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("総合スコア", f"{scores['percentage']}%")
    with col2:
        st.metric("AI活用レベル", scores["tier"])
    with col3:
        st.metric("優先ジョブ", scores["job_priority"] or "—")

    st.divider()

    # ===== カテゴリ別スコア =====
    st.subheader("カテゴリ別評価")
    for cat, avg in scores["category_avg"].items():
        level = "優秀" if avg >= 3.5 else "良好" if avg >= 2.5 else "要改善" if avg >= 1.5 else "緊急改善"
        st.markdown(f"**{cat}** — {avg:.1f}/4.0 ({level})")
        st.progress(avg / 4.0)

    st.divider()

    # ===== AI提案生成 =====
    st.subheader("💡 AI改善提案")

    api_key = os.environ.get("ANTHROPIC_API_KEY", "")

    with st.spinner("AIが改善提案を生成中…"):
        if api_key:
            proposal = generate_proposal_with_ai(
                answers, scores, shop_name, industry, api_key
            )
        else:
            proposal = generate_proposal_fallback(answers, scores, shop_name)

    st.markdown(proposal)

    st.divider()

    # ===== PDF出力 =====
    st.subheader("📄 レポートダウンロード")

    report_text = build_full_report(shop_name, industry, scores, proposal)
    pdf_bytes = generate_pdf(report_text, shop_name, scores)

    st.download_button(
        label="PDFレポートをダウンロード",
        data=pdf_bytes,
        file_name=f"ai_diagnostic_{shop_name}_{datetime.now().strftime('%Y%m%d')}.pdf",
        mime="application/pdf",
        type="primary",
    )

    st.divider()

    # ===== CTA =====
    st.markdown("""
    ### 次のステップ

    この診断レポートを元に、**より詳細な分析と具体的な実装プラン**を
    ご提案できます。

    - **有償診断（¥30,000）**: 貴店のShopifyデータを直接分析し、
      ROI試算付きの実装ロードマップを作成
    - **スポット実装（¥80,000）**: 最優先施策1つを実際にセットアップ・納品

    👉 [詳細はこちら — お問い合わせフォーム]
    """)

    # やり直しボタン
    if st.button("最初からやり直す"):
        st.session_state.step = "intro"
        st.session_state.answers = {}
        st.session_state.shop_info = {}
        st.rerun()


def build_full_report(shop_name: str, industry: str, scores: dict, proposal: str) -> str:
    """PDF用のフルテキストレポートを組み立てる"""
    cat_lines = ""
    for cat, avg in scores["category_avg"].items():
        level = "優秀" if avg >= 3.5 else "良好" if avg >= 2.5 else "要改善" if avg >= 1.5 else "緊急改善"
        cat_lines += f"  {cat}: {avg:.1f}/4.0 ({level})\n"

    return f"""AI経営診断レポート
{shop_name} 様（{industry}）
診断日: {datetime.now().strftime('%Y年%m月%d日')}

━━━━━━━━━━━━━━━━━━━━
総合スコア: {scores['total_score']}/{scores['max_score']}点（{scores['percentage']}%）
AI活用レベル: {scores['tier']}
{scores['ai_readiness']}

カテゴリ別評価:
{cat_lines}
優先ジョブ: {scores.get('job_priority', '未回答')}
━━━━━━━━━━━━━━━━━━━━

AI改善提案:
{proposal}

━━━━━━━━━━━━━━━━━━━━
次のステップ:
1. 有償診断（¥30,000）: Shopifyデータ直接分析 + 実装ロードマップ
2. スポット実装（¥80,000）: 最優先施策1つをセットアップ・納品
3. 月額リテイナー: 継続的なAI活用改善パートナー

© 2026 AI実装パートナー
"""


# ===== メインルーティング =====
def main():
    if st.session_state.step == "intro":
        show_intro()
    elif st.session_state.step == "questions":
        show_questions()
    elif st.session_state.step == "result":
        show_result()


if __name__ == "__main__":
    main()
