# freelance-compass

個人フリーランスが月10〜20時間の稼働で最適な事業を特定するためのAIエージェントチームシステム。

## 前提制約（全エージェント共通・厳守）

- **対象クライアント**: 個人事業主・中小企業・スモールビジネスのみ（スタートアップ・大企業・VC調達済み企業は除外）
- **実行者**: ユーザー1人のみ（外注・チーム・雇用は一切なし）
- **AI活用**: Claude Code・ChatGPT等をフル活用し、人間の稼働時間を最小化する
- **最低ライン**: 実質時給（案件単価 ÷ 人間稼働時間）が ¥10,000未満のニッチは自動却下
- **事業方針**: ローリスク・ミドルリターン型。ハイリスク・ハイリターンは避ける
- **ワークスタイル**: リモートメイン。月5時間以内の移動・現地ワークはOK

## コマンド一覧

| コマンド | 読み込むスキル | 説明 |
|---------|--------------|------|
| `/profile` | skills/01_profiler.md | スキル・経験・制約の構造化インタビュー |
| `/scout` | skills/02_market_scout.md | スモールビジネス市場の需要調査 |
| `/ai-leverage` | skills/03_ai_leverage.md | AI活用率と実質時給の算出 |
| `/feasibility` | skills/04_feasibility.md | 実行可能性の多軸評価 |
| `/revenue` | skills/05_revenue_model.md | 収益モデルとポートフォリオ設計 |
| `/synthesize` | skills/06_synthesizer.md | 最終統合レポート生成 |
| `/status` | — | state/session.json を読んで進捗を表示 |
| `/full-run` | 全スキル順次実行 | 01→06を順に実行し、各完了後にstate更新 |

## 実行ルール

1. 各スキルファイルの **Max turns** を遵守すること
2. フェーズ完了ごとに **state/session.json** を必ず更新すること
3. エラーは state/session.json の `error_log` に記録すること
4. 前フェーズの出力が `null` のまま次フェーズに進まないこと（`/full-run` 時）
5. ¥10,000/h 未満のニッチは理由を明記して即時除外すること

## state/session.json の構造

セッション状態を一元管理する。各エージェントは自身の担当キーのみ更新する。
`current_phase` は `not_started` → `profiling` → `scouting` → `ai_leverage` → `feasibility` → `revenue_model` → `synthesizing` → `complete` の順に遷移する。

## モデル使い分け

- Opus: プロファイリング（01）、最終統合（06）、判断が必要な場面
- Sonnet: 市場調査（02）、AI活用分析（03）、実行可能性（04）、収益モデル（05）
