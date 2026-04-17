# AI経営パートナー × データサイエンス 統合事業計画 v2 — INDEX

## 〜 士業・小売EC特化 | 一人法人 24ヶ月ロードマップ 〜

**作成日:** 2026年3月25日（v2改訂）
**対象期間:** 2026年5月〜2028年4月（24ヶ月）
**事業主体:** 一人法人（男座員也）
**稼働制約:** 月32時間
**目標時給:** ¥30,000/h以上（悲観シナリオでも）

---

## 本ファイルについて

本ファイルは統合事業計画 v2 の **INDEX（目次）** です。実本文は `integrated-business-plan-v2/` ディレクトリ配下に 6 ファイル分割で格納されています（API タイムアウト対策）。

> **元ファイル**: [`outputs/integrated-business-plan-v2.md`](https://github.com/KazuyaMurayama/freelance-compass/blob/claude/integrated-business-plan/outputs/integrated-business-plan-v2.md) on `claude/integrated-business-plan` ブランチ（モノリシック 32KB 版）

---

## 目次（分割ファイル構成）

| # | ファイル | 内容 | サイズ |
|---|---------|------|-------|
| 1 | [01-executive-summary.md](./integrated-business-plan-v2/01-executive-summary.md) | Executive Summary、3 層サービス構造、4 シナリオ結論、Top 5 アクション、品質スコアカード（v1→v2） | 5 KB |
| 2 | [02-segments-pains.md](./integrated-business-plan-v2/02-segments-pains.md) | ターゲットセグメント（士業 + 小売/EC の TAM/SAM/SOM・ペルソナ）、ペイン分析、価格設計の根拠 | 5 KB |
| 3 | [03-solution-channels.md](./integrated-business-plan-v2/03-solution-channels.md) | 3 層サービス詳細、逆 SHAP エンジン、MVP 定義、プロダクトロードマップ、チャネル戦略 | 5 KB |
| 4 | [04-roadmap.md](./integrated-business-plan-v2/04-roadmap.md) | Phase 0（M1–M3 週次詳細）、Phase 1（PMF 判定）、Phase 2（テンプレ化）、Phase 3（拡大） | 6 KB |
| 5 | [05-financials.md](./integrated-business-plan-v2/05-financials.md) | 4 シナリオ別 顧客数／MRR／P/L、時給分析、¥30K/h 達成条件、感度分析、サマリー | 7 KB |
| 6 | [06-kpi-risks.md](./integrated-business-plan-v2/06-kpi-risks.md) | AARRR マーケティング KPI、アラート基準、主要リスク、撤退基準（Kill Criteria） | 5 KB |

---

## Executive Summary（要約）

### 事業コンセプト

「AI経営パートナー」と「ML予測モデル」を統合し、**士業（税理士・社労士）**と**小売/EC事業者**に対して、AI活用支援からデータ分析・経営伴走までをワンストップで提供する一人法人事業。

### サービス構造（3層モデル）

| 層 | 内容 | 価格帯 |
|----|------|--------|
| **L1: AI業務効率化** | ChatGPT/Claude活用、プロンプト設計、社内RAG | スポット¥10〜20万 / 月額¥5万 |
| **L2: ML予測モデル** | 売上予測、需要予測、離脱予測、逆SHAP提案 | 初期¥30〜50万 + 月額¥10万 |
| **L3: AI経営パートナー** | 月次経営MTG、KPI設計、AI活用ロードマップ | 月額¥20〜30万 |

### 4シナリオ比較

| シナリオ | 確率 | M24 MRR | 24ヶ月累計利益 | M24時点 時給 |
|---------|------|---------|-------------|------------|
| **楽観** | 15% | ¥180万 | ¥2,410万 | ¥72,000/h |
| **標準** | 50% | ¥100万 | ¥1,310万 | ¥40,300/h |
| **悲観** | 25% | ¥62万 | ¥770万 | **¥31,000/h** |
| **ワースト** | 10% | ¥28万 | ¥250万 | ¥14,000/h |
| **期待値** | — | ¥97万 | ¥1,210万 | ¥39,100/h |

**悲観シナリオでも時給¥31,000/hを達成**する設計。

### 最重要アクション（Top 5）

1. 士業・EC向けMLデモアプリ各1本構築（M1、計12h）
2. 士業3名+EC2名へのインタビュー（M1〜M2、計10h）— 価格感度テスト必須
3. 士業向けウェビナー開催（M3、参加目標15名）
4. 初回有料契約（M3、L1スポット or L2 PoC）
5. PMF判定 + 時給実測（M6、実稼働時間の正確な記録→時給算出）

---

## 関連ドキュメント

- 実装側（下流リポ）: [MachineLearning_App](https://github.com/KazuyaMurayama/MachineLearning_App) — 18 Streamlit アプリ、`docs/sales-assets/pricing-and-scope.md`（v0.3 で v2 価格に整合済み）
- 戦略バージョン履歴: `../tasks.md` の「戦略バージョン履歴」セクション
- 参考（旧版）: `outputs/recommendation.md`（v9.0 士業+クリニック）、WDemK ブランチの recommendation.md（v29.0 EC+クリニック）

*本 INDEX は分割保存版。モノリシック版は `claude/integrated-business-plan` ブランチ参照。*
