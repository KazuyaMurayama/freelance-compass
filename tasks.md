# タスク（セッション間引継ぎ用ランニングリスト）

> 最終更新: 2026-04-16
> 作業ブランチ: `claude/review-repo-docs-2nBuQ`
> **🟢 最新戦略（分割保存済）**: [outputs/integrated-business-plan-v2.md](./outputs/integrated-business-plan-v2.md) — INDEX + 6 パートファイル
> **🟢 モノリシック版**: [integrated-business-plan-v2.md](https://github.com/KazuyaMurayama/freelance-compass/blob/claude/integrated-business-plan/outputs/integrated-business-plan-v2.md)（`claude/integrated-business-plan` ブランチ、32KB）
> 関連リポ: `kazuyamurayama/machinelearning_app`（下流＝実装）

## プロジェクトの現在地（最新戦略 = integrated v2）

事前分析・統合計画は完了。**Phase 0（M1=2026年5月開始）の準備フェーズ**。

| 項目 | 内容 |
|---|---|
| 推奨事業 | AI経営パートナー × データサイエンス 統合事業 |
| 初期ターゲット（v2） | **士業（税理士・社労士）+ 小売/EC** |
| サービス構造 | L1 AI業務効率化 ¥5万 / L2 ML予測モデル ¥10-12万 / L3 AI経営パートナー ¥20-25万 |
| 想定月稼働 | 32時間 |
| 24ヶ月期待値 | M24 MRR ¥97万 / 累計利益 ¥1,210万 / 時給 ¥46,700/h |
| ¥30K/h達成月 | 標準 M12 / 悲観 M18 |
| 4シナリオ確率 | 楽観15% / 標準50% / 悲観25% / ワースト10% |
| Phase 0 完了条件（M3末） | デモ2本、インタビュー5名、ウェビナー1回、有料契約1社 |

## 戦略バージョン履歴

| 版 | 日付 | ターゲット | 状態 |
|---|---|---|---|
| v9.0 | 2026-03-10 | 士業 + クリニック | 旧版（IBKFu / integrated-business-plan の `recommendation.md`） |
| v29.0 | 2026-03-16 | EC + クリニック | 中間版（WDemK の `outputs/recommendation.md` 285KB） |
| **integrated v2** | **2026-03-25** | **士業 + 小売/EC** | **🟢 最新・採用。本ブランチに 6 分割で配置済** |

→ machinelearning_app の実装（士業 11本 + EC 7本）は v2 に整合済み。価格も v2 L3（士業 ¥20万 / EC ¥25万）に整合（machinelearning_app pricing-and-scope v0.3）。

## 起動時チェックリスト

1. `CLAUDE.md` を読む（前提制約・コマンド一覧）
2. 本ファイル（tasks.md）を読む
3. **`outputs/integrated-business-plan-v2.md`（INDEX）から必要パートを読む**
4. `machinelearning_app/tasks.md`（実装側の現在地）を確認

---

## 次にやる（優先度順）

### 🔴 P0: Phase 0 準備（M1=2026年5月までに）

- [ ] **A1 診断ツール（`tools/a1_diagnostic/`）を v2 の MVP-1（士業デモ）/ MVP-2（ECデモ）として位置づけ直す**（士業版と EC 版 2 本に分割検討）
- [ ] **サービスペライチ + 料金表 PDF 作成**（v2 の L1 ¥5万 / L2 ¥10-12万 / L3 ¥20-25万 に準拠、machinelearning_app の pricing-and-scope v0.3 と整合）
- [ ] **ペイン仮説リスト作成**（士業/EC 各 10 項目、v2 Part 2 を雛形）
- [ ] **インタビュー候補リストアップ**（士業 3 名 + EC 2 名）

### 🟠 P1: アウトリーチチャネル準備

- [ ] **ビザスクエキスパート登録**（即日）
- [ ] **ココナラ出品**（¥5,000 診断レポート、2-3日以内）
- [ ] **Shopify Partner 申請**（審査 1-3ヶ月リードタイム）
- [ ] **note / X 記事 3本公開**（士業×AI、EC×DS テーマ）
- [ ] **Peatix/connpass ウェビナー登録**（M3 開催準備）

### 🟡 P2: M1〜M3 Phase 0 実行（v2 Part 4）

v2 の Top 5 アクション + WDemK セッション P0 を統合。M3末までに完了。

- [ ] **MVP-1 士業デモ**（離反予測+SHAP）— W1, 工数 6h
- [ ] **MVP-2 ECデモ**（需要予測+在庫最適化）— W2, 工数 6h
- [ ] **士業 3名 + EC 2名 インタビュー実行**（W3-W8, 計 10h、価格感度テスト ¥10万/月）
- [ ] **士業向けウェビナー開催**（M3 W9, 参加目標 15名）
- [ ] **初回有料契約**（M3 W12, L1 スポット or L2 PoC × 1社）
- [ ] **稼働時間記録の運用開始**（時給算出のため）

### 🟢 P3: PMF 判定基盤・撤退基準運用化

- [ ] **PMF 判定指標 5項目を運用ドキュメント化**（3ヶ月継続率、NPS、自然紹介、L2アップセル率、実測時給）
- [ ] **撤退基準（Kill Criteria）を運用ドキュメント化**（M6/M12/M18/M24 の判定タイミング、v2 Part 6）
- [ ] **マーケティング KPI ダッシュボード**（AARRR ファネル、悲観ベースのKPIターゲット）

---

## 進行中

- なし

---

## 完了（直近）

- 2026-04-16: **v2 文書を本ブランチに分割保存**。`outputs/integrated-business-plan-v2.md`（INDEX）+ `outputs/integrated-business-plan-v2/01〜06-*.md`（6 パート）の 7 ファイル構成。API タイムアウト対策で各 <8KB。モノリシック版は引き続き `claude/integrated-business-plan` にも存在
- 2026-04-16: **戦略バージョン整理完了**。v2（士業+小売/EC、2026-03-25）が最新であることを確認。tasks.md / CLAUDE.md / machinelearning_app 側ドキュメントから「戦略整合性アラート」を撤回し、v2 ベースで P0-P3 を再定義
- 2026-04-16: **machinelearning_app `pricing-and-scope.md` を v2 整合版 (v0.3) に更新**（L3 士業 ¥300k→¥200k / EC ¥260k→¥250k）
- 2026-04-02 頃: WDemK セッション（v29.0 集約・ハイパーリンクサマリー）
- 2026-03-25: **integrated-business-plan v2 策定**（士業+小売/EC、4シナリオ、時給目標 ¥30K/h、24ヶ月期待値 ¥1,210万）
- 2026-03-17〜20: 仮説検証 v3（Track A/B/C + Day3 判定）
- 2026-03-16: recommendation v29.0（EC+クリニック、¥180k/月）
- 2026-03-10: recommendation v9.0（士業+クリニック）

---

## 既知のリスク（v2 Part 6）

- 🔴 **価格が市場に受容されない**（高影響・中確率）— M2 価格感度テストで早期検知。受容されない場合は L2 ¥7万 + 成果報酬への切替準備
- 🔴 **大手（freee AI 等）参入**（高影響・高確率）— 人的関係性・ニッチ集中で差別化
- 🟠 士業のAI拒否反応 — インタビューで早期検知、EC側ピボット余地確保
- 🟠 稼働時間不足 — テンプレ化前倒し、最低 16h/月設計
- 🟠 顧客データ取扱リスク — NDA標準化、顧客環境内処理

## 撤退基準（v2 Part 6）

| 条件 | 判定時期 |
|---|---|
| 有料顧客 0社 | M6末 |
| MRR ¥10万未満 | M12末 |
| NPS 0未満 | M12末 |
| **実測時給 ¥15,000/h未満** | M12末 |
| 累計利益マイナス | M18末 |
| 紹介 0件 | M24末 |

---

## 次セッションへの申し送り

1. **最新戦略は v2（士業+小売/EC）**。本ブランチの `outputs/integrated-business-plan-v2.md`（INDEX）から各パートを読む
2. machinelearning_app の実装と価格は v2 に整合済み（pricing-and-scope v0.3）
3. M1=2026年5月 が Phase 0 開始。それまでに P0/P1 を完了する
4. v2 の時給目標 ¥30K/h は構造的に達成可能（感度分析で全変数20%悪化でも ¥25K-35K/h）
5. 主要報告には 2〜4 件の GitHub ハイパーリンクを付与（確立ルール）
