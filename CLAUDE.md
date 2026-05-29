# freelance-compass

個人フリーランスが月10〜20時間の稼働で最適な事業を特定するためのAIエージェントチームシステム。

## セッション開始時に必ず読むファイル

1. **本ファイル（CLAUDE.md）** — 前提制約・コマンド・実行ルール
2. **`tasks.md`** — セッション間引継ぎタスクリスト（次にやること・優先順位・戦略バージョン履歴）
3. **🟢 最新戦略**: [`integrated-business-plan-v2.md`](https://github.com/KazuyaMurayama/freelance-compass/blob/claude/integrated-business-plan/outputs/integrated-business-plan-v2.md)（2026-03-25 改訂、士業+小売/EC、`claude/integrated-business-plan` ブランチ）
4. `outputs/session-summary-WDemK.md` — 直近セッションの要約（v29.0 時点・参考）
5. `state/session.json` でフェーズ進捗を確認

> ⚠️ `outputs/recommendation.md` は v9.0（士業+クリニック、旧版）または v29.0（EC+クリニック、中間版）。**最新は integrated v2**。混乱したら `tasks.md` の「戦略バージョン履歴」を確認。

## 関連リポジトリ

| リポ | 役割 |
|------|------|
| 本リポ | 上流：事業戦略・意思決定（6エージェントで戦略策定） |
| `kazuyamurayama/machinelearning_app` | 下流：18 Streamlit アプリ実装と顧客獲得 |

セッション開始時は `machinelearning_app/tasks.md` も突き合わせる。**v2 (士業+小売/EC) で実装と戦略が整合済み**。

## 前提制約（全エージェント共通・厳守）

- **対象クライアント**: 個人事業主・中小企業・スモールビジネスのみ（スタートアップ・大企業・VC調達済み企業は除外）
- **実行者**: ユーザー1人のみ（外注・チーム・雇用は一切なし）
- **AI活用**: Claude Code・ChatGPT等をフル活用し、人間の稼働時間を最小化する
- **最低ライン**: 実質時給（案件単価 ÷ 人間稼働時間）が ¥10,000未満のニッチは自動却下
- **事業方針**: ローリスク・ミドルリターン型。ハイリスク・ハイリターンは避ける
- **ワークスタイル**: リモートメイン。月5時間以内の移動・現地ワークはOK
- **稼働上限**: v2 で月 32時間に拡張（旧 v9.0/v29.0 では月 10〜20h 想定）

## コマンド一覧

| コマンド | 読み込むスキル | 説明 |
|---------|--------------|------|
| `/profile` | agents/01_profiler.md | スキル・経験・制約の構造化インタビュー |
| `/scout` | agents/02_market_scout.md | スモールビジネス市場の需要調査 |
| `/ai-leverage` | agents/03_ai_leverage.md | AI活用率と実質時給の算出 |
| `/feasibility` | agents/04_feasibility.md | 実行可能性の多軸評価 |
| `/revenue` | agents/05_revenue_model.md | 収益モデルとポートフォリオ設計 |
| `/synthesize` | agents/06_synthesizer.md | 最終統合レポート生成 |
| `/status` | — | state/session.json を読んで進捗を表示 |
| `/full-run` | 全スキル順次実行 | 01→06を順に実行し、各完了後にstate更新 |

## 実行ルール

1. 各スキルファイルの **Max turns** を遵守すること
2. フェーズ完了ごとに **state/session.json** を必ず更新すること
3. エラーは state/session.json の `error_log` に記録すること
4. 前フェーズの出力が `null` のまま次フェーズに進まないこと（`/full-run` 時）
5. ¥10,000/h 未満のニッチは理由を明記して即時除外すること
6. **実行フェーズ（A1ツール / ビザスク等）の進捗は `tasks.md` に必ず反映**
7. **戦略文書を読む際は必ず最新版（integrated v2）を確認**。古い `recommendation.md` を引用する場合は版を明記

## state/session.json の構造

セッション状態を一元管理する。各エージェントは自身の担当キーのみ更新する。
`current_phase` は `not_started` → `profiling` → `scouting` → `ai_leverage` → `feasibility` → `revenue_model` → `synthesizing` → `complete` の順に遷移する。
※ v2 完成後の実行フェーズは `tasks.md` で別途管理。

## モデル使い分け

- Opus: プロファイリング（01）、最終統合（06）、判断が必要な場面
- Sonnet: 市場調査（02）、AI活用分析（03）、実行可能性（04）、収益モデル（05）

## セッション終了時の手順

1. `tasks.md` の「次にやる」「完了」を更新
2. **machinelearning_app に影響する戦略変化があれば同リポの `tasks.md` も更新**
3. 戦略の新版を作成した場合は `tasks.md` の「戦略バージョン履歴」を更新
4. 重大変更時は `outputs/session-summary-<branchID>.md` を追加
5. コミット → push

## 開発者情報・命名ルール

このリポジトリの開発者・所有者は **男座員也（Kazuya Oza / おざ かずや）** です。

- ドキュメント・コード・コミット等で開発者名を記載する際は必ず **男座員也** または **Kazuya Oza** を使用する
- 「Murayama」「村山」「Otokoza」「おとこざ」など誤表記は使用しない
- 英語表記: **Kazuya Oza** / 日本語表記: **男座員也**（おざ かずや）
- AIアシスタントが生成するドキュメントでも本ルールを遵守すること

## ファイル保存ルール
- 成果物・スクリプトは本リポジトリ内のみに保存。`C:\\Users\\user\\Desktop` への出力禁止（ユーザー明示指定時を除く）。

<!-- SKILLS_RULES_START -->
## Skill 起動ルール（v2.1 / 2026-05-29）
以下のスキルは **必須・スキップ禁止**。該当シーンでは SKILL.md を読んでから作業を開始すること。

- **新機能実装・設計を始める前に必ず** `.claude/skills/sp-brainstorming/SKILL.md` でアイデアを出し、`.claude/skills/sp-writing-plans/SKILL.md` で計画を作成してから着手する
- **複雑な多段タスクは** `.claude/skills/sp-executing-plans/SKILL.md` の手順で実行する
- **アーキ図・フロー図が必要な時は必ず** `.claude/skills/mermaid-agents365/SKILL.md` を読んでからダイアグラムを作成する
- **成果物の納品・コミット前、または品質チェック（QC）・レビューフェーズに入る時は必ず** `.claude/skills/sp-verification-before-completion/SKILL.md` のチェックリストを実行する
- **要件調査が真に必要な時のみ** `.claude/skills/research-deep/SKILL.md` を読んで Web リサーチを実行する
<!-- SKILLS_RULES_END -->
