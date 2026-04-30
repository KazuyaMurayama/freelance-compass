# FILE_INDEX.md — freelance-compass

> **新セッション開始時に必ずこのファイルを読む。**
> ファイル追加・削除・移動時は必ずこのファイルを更新すること。
> 最終更新: 2026-04-30

## 概要
フリーランス転身を目指すためのビジネス計画・市場調査・仮説検証・MVP設計ドキュメント群。診断ツール（Streamlit）付き。

**スタック:** Python, Streamlit, Markdown

---

## 📋 最初に読むべきファイル

| 優先度 | ファイル | 内容 |
|---|---|---|
| ★★★ | `CLAUDE.md` | 運用ルール・指針 |
| ★★★ | `outputs/integrated-business-plan-v2/` | 統合ビジネスプランv2 |
| ★★★ | `tools/a1_diagnostic/app.py` | 診断ツールメインアプリ |
| ★★ | `outputs/ai-utilization-plan-v7.md` | AI活用計画v7 |
| ★★ | `outputs/shigyou-mvp-roadmap.md` | 士業MVP ロードマップ |

---

## 🗂️ ディレクトリ構造

```
freelance-compass/
├── CLAUDE.md                    ← 最重要ルール
├── skills/
│   ├── 01_profiler.md ～ 06_synthesizer.md
├── state/session.json
├── tools/
│   └── a1_diagnostic/           ← 診断ツール
│       ├── app.py
│       ├── scoring.py
│       ├── proposal.py
│       ├── pdf_export.py
│       ├── test_diagnostic.py
│       └── requirements.txt
└── outputs/
    ├── ai-utilization-plan-v7.md
    ├── integrated-business-plan-v2/
    │   └── 01～06.md
    ├── customer-research/       ← EC・美容・歯科・専門職
    ├── verification-v3/
    ├── shigyou-mvp-roadmap.md
    ├── weekly-execution-plan.md
    └── recommendation.md
```

---

## 📑 全ファイル一覧

| パス | 種別 | 説明 |
|---|---|---|
| `CLAUDE.md` | ドキュメント | 運用ルール・指針 |
| `skills/01_profiler.md` | ドキュメント | プロファイラースキル定義 |
| `skills/06_synthesizer.md` | ドキュメント | シンセサイザースキル定義 |
| `state/session.json` | データ | セッション状態管理 |
| `tools/a1_diagnostic/app.py` | Python | 診断ツールメインアプリ（Streamlit） |
| `tools/a1_diagnostic/scoring.py` | Python | スコアリングロジック |
| `tools/a1_diagnostic/proposal.py` | Python | 提案書生成 |
| `tools/a1_diagnostic/pdf_export.py` | Python | PDF出力 |
| `tools/a1_diagnostic/test_diagnostic.py` | Python | 診断テスト |
| `tools/a1_diagnostic/requirements.txt` | 設定 | 診断ツール依存関係 |
| `outputs/ai-utilization-plan-v7.md` | ドキュメント | AI活用計画v7 |
| `outputs/integrated-business-plan-v2/` | ドキュメント | 統合ビジネスプランv2（01〜06章） |
| `outputs/customer-research/` | ドキュメント | 顧客調査（EC・美容・歯科・専門職） |
| `outputs/verification-v3/` | ドキュメント | 市場調査・構造分析・ペルソナ・メタ検証 |
| `outputs/shigyou-mvp-roadmap.md` | ドキュメント | 士業向けMVPロードマップ |
| `outputs/weekly-execution-plan.md` | ドキュメント | 週次実行計画 |
| `outputs/recommendation.md` | ドキュメント | 推奨アクション |

---

## 🔖 ファイル更新ルール

1. 新ファイル追加時: 該当セクションに1行追加
2. ファイル削除・移動時: 該当行を削除または更新
3. 更新後: `git add FILE_INDEX.md && git commit -m "docs: FILE_INDEX.md更新"`
