"""
A1 PDF出力モジュール
fpdf2を使って日本語対応の診断レポートPDFを生成
"""

import io
import os
from datetime import datetime
from fpdf import FPDF


# Noto Sans JP フォントパス（存在しなければフォールバック）
FONT_DIR = os.path.join(os.path.dirname(__file__), "fonts")
NOTO_SANS_PATH = os.path.join(FONT_DIR, "NotoSansJP-Regular.ttf")
NOTO_SANS_BOLD_PATH = os.path.join(FONT_DIR, "NotoSansJP-Bold.ttf")


class DiagnosticPDF(FPDF):
    """診断レポート用PDF"""

    def __init__(self):
        super().__init__()
        self._has_jp_font = False
        self._setup_fonts()

    def _setup_fonts(self):
        """日本語フォントの設定"""
        if os.path.exists(NOTO_SANS_PATH):
            self.add_font("NotoSansJP", "", NOTO_SANS_PATH, uni=True)
            # Bold用にも同じフォントを登録（可変ウェイトフォントの場合）
            bold_path = NOTO_SANS_BOLD_PATH if os.path.exists(NOTO_SANS_BOLD_PATH) else NOTO_SANS_PATH
            self.add_font("NotoSansJP", "B", bold_path, uni=True)
            self._has_jp_font = True
            self.set_font("NotoSansJP", size=10)
        else:
            self.set_font("Helvetica", size=10)

    @property
    def font_family_name(self) -> str:
        return "NotoSansJP" if self._has_jp_font else "Helvetica"

    def header(self):
        self.set_font(self.font_family_name, "B" if self._has_jp_font else "", 14)
        title = "AI EC Diagnostic Report" if not self._has_jp_font else "AI経営診断レポート"
        self.cell(0, 10, title, align="C", new_x="LMARGIN", new_y="NEXT")
        self.ln(4)

    def footer(self):
        self.set_y(-15)
        self.set_font(self.font_family_name, "", 8)
        copy_text = "(C) 2026 AI Implementation Partner" if not self._has_jp_font else "© 2026 AI実装パートナー"
        self.cell(0, 10, f"{copy_text} | Page {self.page_no()}", align="C")


def _bar_text(value: float, max_val: float = 4.0) -> str:
    """スコアバーのテキスト表現"""
    filled = int((value / max_val) * 10)
    return "█" * filled + "░" * (10 - filled)


def generate_pdf(report_text: str, shop_name: str, scores: dict) -> bytes:
    """診断レポートのPDFバイト列を生成"""
    pdf = DiagnosticPDF()
    pdf.add_page()
    fn = pdf.font_family_name

    # ===== ストア情報 =====
    pdf.set_font(fn, "B" if pdf._has_jp_font else "", 12)
    pdf.cell(0, 8, f"{shop_name}", new_x="LMARGIN", new_y="NEXT")

    pdf.set_font(fn, "", 10)
    date_str = datetime.now().strftime("%Y-%m-%d")
    pdf.cell(0, 6, f"Diagnosis Date: {date_str}", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)

    # ===== サマリーボックス =====
    pdf.set_fill_color(240, 248, 255)
    pdf.set_font(fn, "B" if pdf._has_jp_font else "", 11)

    summary_label = "Score" if not pdf._has_jp_font else "総合スコア"
    tier_label = "AI Level" if not pdf._has_jp_font else "AI活用レベル"
    job_label = "Priority Job" if not pdf._has_jp_font else "優先ジョブ"

    pdf.cell(60, 8, f"{summary_label}: {scores['percentage']}%",
             border=1, fill=True, new_x="RIGHT", new_y="TOP")
    pdf.cell(60, 8, f"{tier_label}: {scores['tier']}",
             border=1, fill=True, new_x="RIGHT", new_y="TOP")
    pdf.cell(0, 8, f"{job_label}: {scores.get('job_priority', '-')}",
             border=1, fill=True, new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)

    # ===== カテゴリ別スコア =====
    pdf.set_font(fn, "B" if pdf._has_jp_font else "", 11)
    cat_header = "Category Scores" if not pdf._has_jp_font else "カテゴリ別評価"
    pdf.cell(0, 8, cat_header, new_x="LMARGIN", new_y="NEXT")
    pdf.set_font(fn, "", 10)

    for cat, avg in scores.get("category_avg", {}).items():
        level = "Excellent" if avg >= 3.5 else "Good" if avg >= 2.5 else "Needs Work" if avg >= 1.5 else "Urgent"
        if pdf._has_jp_font:
            level = "優秀" if avg >= 3.5 else "良好" if avg >= 2.5 else "要改善" if avg >= 1.5 else "緊急改善"
        bar = _bar_text(avg)
        pdf.cell(0, 6, f"  {cat}: {avg:.1f}/4.0 {bar} ({level})",
                 new_x="LMARGIN", new_y="NEXT")

    pdf.ln(6)

    # ===== 提案テキスト =====
    pdf.set_font(fn, "B" if pdf._has_jp_font else "", 11)
    proposal_header = "AI Improvement Proposals" if not pdf._has_jp_font else "AI改善提案"
    pdf.cell(0, 8, proposal_header, new_x="LMARGIN", new_y="NEXT")

    pdf.set_font(fn, "", 9)
    # report_textをそのまま書き込む（multi_cellで自動折り返し）
    effective_width = pdf.w - pdf.l_margin - pdf.r_margin
    for line in report_text.split("\n"):
        # Markdown記法を簡易除去
        clean = line.replace("###", "").replace("**", "").replace("---", "─" * 30)
        clean = clean.strip()
        if not clean:
            pdf.ln(3)
        elif clean.startswith("| "):
            # テーブル行 — 長すぎたらトランケート
            pdf.cell(0, 5, clean[:100], new_x="LMARGIN", new_y="NEXT")
        else:
            pdf.multi_cell(effective_width, 5, clean)

    # ===== CTA =====
    pdf.ln(6)
    pdf.set_font(fn, "B" if pdf._has_jp_font else "", 11)
    next_header = "Next Steps" if not pdf._has_jp_font else "次のステップ"
    pdf.cell(0, 8, next_header, new_x="LMARGIN", new_y="NEXT")
    pdf.set_font(fn, "", 10)

    steps = [
        ("1", "有償診断（¥30,000）" if pdf._has_jp_font else "Paid Diagnosis (¥30,000)",
         "Shopifyデータ直接分析 + 実装ロードマップ" if pdf._has_jp_font else "Direct Shopify data analysis + implementation roadmap"),
        ("2", "スポット実装（¥80,000）" if pdf._has_jp_font else "Spot Implementation (¥80,000)",
         "最優先施策1つをセットアップ・納品" if pdf._has_jp_font else "Setup and deliver top priority measure"),
        ("3", "月額リテイナー" if pdf._has_jp_font else "Monthly Retainer",
         "継続的なAI活用改善パートナー" if pdf._has_jp_font else "Ongoing AI implementation partner"),
    ]
    for num, title, desc in steps:
        pdf.cell(0, 6, f"  {num}. {title}: {desc}", new_x="LMARGIN", new_y="NEXT")

    # バイト列として返す
    return bytes(pdf.output())
