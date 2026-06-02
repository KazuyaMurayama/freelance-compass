# freelance-compass — Claude Code 運用ルール

個人フリーランスが月10〜20時間の稼働で最適な事業を特定するための AI エージェントチームシステム。

> **本ファイルは VSCode版 / Web版 Claude Code（claude.ai）の両方で本リポジトリの単独完結ガイド**。
> Web版はグローバル `~/.claude/CLAUDE.md` を参照しない前提で、本リポの運用に必要な全ルールをここに集約。

---

## 0. セッション開始時に必ず読むファイル

1. **本ファイル（CLAUDE.md）** — 前提制約・コマンド・実行ルール
2. **`tasks.md`** — セッション間引継ぎタスクリスト（次にやること・優先順位・戦略バージョン履歴）
3. **🟢 最新戦略**: [`integrated-business-plan-v2.md`](https://github.com/KazuyaMurayama/freelance-compass/blob/claude/integrated-business-plan/outputs/integrated-business-plan-v2.md)（2026-03-25 改訂、士業+小売/EC、`claude/integrated-business-plan` ブランチ）
4. `outputs/session-summary-WDemK.md` — 直近セッションの要約（v29.0 時点・参考）
5. `state/session.json` でフェーズ進捗を確認

> ⚠️ `outputs/recommendation.md` は v9.0（士業+クリニック、旧版）または v29.0（EC+クリニック、中間版）。**最新は integrated v2**。混乱したら `tasks.md` の「戦略バージョン履歴」を確認。

---

## 1. 関連リポジトリ
| リポ | 役割 |
|---|---|
| 本リポ | 上流：事業戦略・意思決定（6エージェントで戦略策定） |
| [KazuyaMurayama/MachineLearning_App](https://github.com/KazuyaMurayama/MachineLearning_App) | 下流：18 Streamlit アプリ実装と顧客獲得 |
| [KazuyaMurayama/freelance-sales-pipeline](https://github.com/KazuyaMurayama/freelance-sales-pipeline) | 営業パイプライン管理 |
| [KazuyaMurayama/career_dev](https://github.com/KazuyaMurayama/career_dev) | キャリア開発 |

セッション開始時は `machinelearning_app/tasks.md` も突き合わせる。**v2 (士業+小売/EC) で実装と戦略が整合済み**。

---

## 2. 前提制約（全エージェント共通・厳守）

- **対象クライアント**: 個人事業主・中小企業・スモールビジネスのみ（スタートアップ・大企業・VC調達済み企業は除外）
- **実行者**: ユーザー1人のみ（外注・チーム・雇用は一切なし）
- **AI活用**: Claude Code・ChatGPT等をフル活用し、人間の稼働時間を最小化する
- **最低ライン**: 実質時給（案件単価 ÷ 人間稼働時間）が ¥10,000未満のニッチは自動却下
- **事業方針**: ローリスク・ミドルリターン型。ハイリスク・ハイリターンは避ける
- **ワークスタイル**: リモートメイン。月5時間以内の移動・現地ワークはOK
- **稼働上限**: v2 で月 32時間に拡張（旧 v9.0/v29.0 では月 10〜20h 想定）

---

## 3. コマンド一覧

| コマンド | 読み込むスキル | 説明 |
|---------|--------------|------|
| `/profile` | `agents/01_profiler.md` | スキル・経験・制約の構造化インタビュー |
| `/scout` | `agents/02_market_scout.md` | スモールビジネス市場の需要調査 |
| `/ai-leverage` | `agents/03_ai_leverage.md` | AI活用率と実質時給の算出 |
| `/feasibility` | `agents/04_feasibility.md` | 実行可能性の多軸評価 |
| `/revenue` | `agents/05_revenue_model.md` | 収益モデルとポートフォリオ設計 |
| `/synthesize` | `agents/06_synthesizer.md` | 最終統合レポート生成 |
| `/status` | — | `state/session.json` を読んで進捗を表示 |
| `/full-run` | 全スキル順次実行 | 01→06を順に実行し、各完了後にstate更新 |

---

## 4. 実行ルール

1. 各スキルファイルの **Max turns** を遵守すること
2. フェーズ完了ごとに **`state/session.json`** を必ず更新すること
3. エラーは `state/session.json` の `error_log` に記録すること
4. 前フェーズの出力が `null` のまま次フェーズに進まないこと（`/full-run` 時）
5. ¥10,000/h 未満のニッチは理由を明記して即時除外すること
6. **実行フェーズ（A1ツール / ビザスク等）の進捗は `tasks.md` に必ず反映**
7. **戦略文書を読む際は必ず最新版（integrated v2）を確認**。古い `recommendation.md` を引用する場合は版を明記

---

## 5. state/session.json の構造

セッション状態を一元管理する。各エージェントは自身の担当キーのみ更新する。
`current_phase` は `not_started` → `profiling` → `scouting` → `ai_leverage` → `feasibility` → `revenue_model` → `synthesizing` → `complete` の順に遷移する。
※ v2 完成後の実行フェーズは `tasks.md` で別途管理。

---

## 6. モデル使い分け

- Opus: プロファイリング（01）、最終統合（06）、判断が必要な場面
- Sonnet: 市場調査（02）、AI活用分析（03）、実行可能性（04）、収益モデル（05）

---

## 7. セッション終了時の手順

1. `tasks.md` の「次にやる」「完了」を更新
2. **MachineLearning_App に影響する戦略変化があれば同リポの `tasks.md` も更新**
3. 戦略の新版を作成した場合は `tasks.md` の「戦略バージョン履歴」を更新
4. 重大変更時は `outputs/session-summary-<branchID>.md` を追加
5. コミット → push

---

## 8. 開発者情報・命名ルール

| 種別 | 表記 | 用途 |
|---|---|---|
| **システム識別子（変更不可）** | `KazuyaMurayama` | GitHub ユーザー名 / URL / `@KazuyaMurayama` |
| **システム識別子（変更不可）** | `kazuya.murayama.21@gmail.com` | git `user.email` / 連絡先 |
| **表記名（人間として記載する場合）** | **男座員也（Kazuya Oza / おざ かずや）** | ドキュメント本文の著者名 / コミット message 中の自己言及 / 営業資料 |

- ドキュメント本文・営業資料等で**人間として**記載する際は **男座員也 / Kazuya Oza** を使用
- 「Murayama」「村山」「Otokoza」「おとこざ」を**表記名**として誤用しない（システム識別子としての `KazuyaMurayama` は許容）

---

## 9. ツール実行・Git・ファイル保存
- 確認不要・即実行（事前確認文を出力しない）
- 例外（事前確認必須）: main への `git push --force`、`gh repo delete`
- **ブランチ管理**: デフォルトはmainへ直接コミット。ブランチ作成は明示指示時のみ（例外: 戦略 v2 のような長期実験は `claude/integrated-business-plan` 等の専用ブランチ）。完了時は main にマージ→削除→push
- **ファイル保存**: 本リポ内のみ。`C:\Users\user\Desktop` への出力禁止

---

## 10. 成果物報告ルール

| 成果物 | 説明 | リンク |
|---|---|---|
| file.md | 1行説明 | [開く](https://github.com/KazuyaMurayama/freelance-compass/blob/main/path/to/file.md) |

- Markdownリンク `[表示名](URL)` 形式必須 / `/blob/<実ブランチ>/<実パス>` 形式
- **報告前にURL存在確認**：`Invoke-WebRequest -Uri https://api.github.com/repos/KazuyaMurayama/freelance-compass/contents/PATH?ref=main -UseBasicParsing` でステータス200確認
- push完了後のみURL生成

---

## 11. Skill 起動ルール

| トリガー | スキル |
|---|---|
| 新機能実装・設計開始時 | `.claude/skills/sp-brainstorming/SKILL.md` → `.claude/skills/sp-writing-plans/SKILL.md` |
| 複雑な多段タスク | `.claude/skills/sp-executing-plans/SKILL.md` |
| 並列エージェント運用 | `.claude/skills/sp-dispatching-parallel-agents/SKILL.md` |
| 市場・先行事例の調査（要件調査が真に必要な時のみ） | `.claude/skills/research-deep/SKILL.md` |
| アーキ図・フロー図 | `.claude/skills/mermaid-agents365/SKILL.md` |
| ROI/価格モデル試算 | `.claude/skills/business-metrics-calculator/SKILL.md` / `impact-quantification/SKILL.md` |
| 成果物の納品・コミット前 / QC | `.claude/skills/sp-verification-before-completion/SKILL.md` + `analysis-qa-checklist/SKILL.md` |
