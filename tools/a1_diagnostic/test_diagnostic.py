"""A1診断ツールの単体テスト"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from scoring import QUESTIONS, calculate_scores
from proposal import generate_proposal_fallback
from pdf_export import generate_pdf


def test_scoring():
    """スコアリングの基本テスト"""
    answers = {
        "Q1": "C", "Q2": "B", "Q3": "B", "Q4": "B", "Q5": "B",
        "Q6": "A", "Q7": "B", "Q8": "B", "Q9": "A", "Q10": "A",
    }
    scores = calculate_scores(answers)

    assert scores["total_score"] > 0
    assert scores["max_score"] == 36
    assert 0 <= scores["percentage"] <= 100
    assert scores["tier"] in ("Starter", "Beginner", "Intermediate", "Advanced")
    assert scores["job_priority"] == "商品PG高速化"
    assert len(scores["category_avg"]) > 0
    print(f"  Score: {scores['total_score']}/{scores['max_score']} ({scores['percentage']}%)")
    print(f"  Tier: {scores['tier']}, Job: {scores['job_priority']}")
    print(f"  Categories: {scores['category_avg']}")
    return scores


def test_proposal(scores):
    """テンプレート提案生成のテスト"""
    proposal = generate_proposal_fallback({}, scores, "テストストア")
    assert len(proposal) > 100
    assert "テストストア" in proposal
    print(f"  Proposal length: {len(proposal)} chars")
    return proposal


def test_pdf(scores, proposal):
    """PDF生成のテスト"""
    report_text = f"""診断サマリー
スコア: {scores['percentage']}%
レベル: {scores['tier']}

{proposal}
"""
    pdf_bytes = generate_pdf(report_text, "テストストア", scores)
    assert len(pdf_bytes) > 0
    assert pdf_bytes[:4] == b"%PDF"

    # ファイルに保存してサイズ確認
    out_path = os.path.join(os.path.dirname(__file__), "test_output.pdf")
    with open(out_path, "wb") as f:
        f.write(pdf_bytes)
    size_kb = len(pdf_bytes) / 1024
    print(f"  PDF size: {size_kb:.1f} KB -> {out_path}")
    return pdf_bytes


if __name__ == "__main__":
    print("=== A1 Diagnostic Tool Tests ===\n")

    print("[1] Scoring...")
    scores = test_scoring()
    print("  PASS\n")

    print("[2] Proposal generation...")
    proposal = test_proposal(scores)
    print("  PASS\n")

    print("[3] PDF export...")
    test_pdf(scores, proposal)
    print("  PASS\n")

    print("=== All tests passed ===")
