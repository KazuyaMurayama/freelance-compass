# AI経営パートナー × データサイエンス 統合事業計画 v2.1.1 — INDEX

## 〜 EC一本化 × 人+AIバンドル × PMF二段階判定 | 一人法人 24ヶ月ロードマップ 〜

**最終更新:** 2026年5月11日（v2.1.1改訂）
**対象期間:** 2026年5月〜2028年4月（24ヶ月）
**事業主体:** 一人法人（男座員也）
**稼働制約:** 月32時間
**目標時給:** ¥35,000/h（標準シナリオM24、全工数ベース）

---

## 本ファイルについて

本ファイルは統合事業計画 v2.1.1 の **INDEX（目次・要約）** です。実本文は `integrated-business-plan-v2/` ディレクトリ配下に 7 ファイル分割で格納されています。

---

## 改訂履歴

| バージョン | 改訂日 | 品質スコア | 主な変更 |
|-----------|-------|-----------|---------|
| **v1** | 2026-02-xx | 70/100 | 初版（士業＋EC二正面） |
| **v2** | 2026-03-25 | 83/100 | 財務シナリオ精緻化・チャネル追加 |
| **v2.1** | 2026-05-10 | 91/100 | EC一本化・人+AIバンドル・PMF二段階判定・4エージェントレビュー反映 |
| **v2.1.1** | 2026-05-11 | **93/100** | ファネル現実化・Kill基準修正・時給算出式明確化・政策リスクE節追加 |

---

## 目次（分割ファイル構成）

| # | ファイル | 内容 |
|---|---------|------|
| 0 | [00-v2.1-confirmed-elements.md](./integrated-business-plan-v2/00-v2.1-confirmed-elements.md) | v2.1確定要素13節（全エージェント共通参照ソース） |
| 1 | [01-executive-summary.md](./integrated-business-plan-v2/01-executive-summary.md) | Executive Summary・3層サービス構造・4シナリオ・Top5アクション・品質スコアカード |
| 2 | [02-segments-pains.md](./integrated-business-plan-v2/02-segments-pains.md) | ターゲットセグメント・ECペイン優先順位・価格帯・WTP分析 |
| 3 | [03-solution-channels.md](./integrated-business-plan-v2/03-solution-channels.md) | 3層サービス詳細・チャネル設計・Shopifyアプリ化ロードマップ・ファネル設計 |
| 4 | [04-roadmap.md](./integrated-business-plan-v2/04-roadmap.md) | Phase0週次詳細（M1-M3）・工数配分32h・Kill基準・L1→L2アップセル設計 |
| 5 | [05-financials.md](./integrated-business-plan-v2/05-financials.md) | 4シナリオ財務・時給算出式・Expert Network収益・感度分析 |
| 6 | [06-kpi-risks.md](./integrated-business-plan-v2/06-kpi-risks.md) | PMF二段階判定・Kill基準5段階・リスクマトリクス・政策リスクE節 |

---

## Executive Summary

### 事業コンセプト

**EC一本化（M1-M6）＋人+AI伴走＋IT導入補助金対応**。年商1〜10億円規模のEC事業者に対し、ML予測モデルと人による月次レビューをバンドルし、IT導入補助金を活用した実質半額の「3ヶ月PoCから始められる」伴走型データ活用支援を提供する一人法人事業。士業セグメントはM7以降に検討。

### サービス構造（3層モデル v2.1.1）

| 層 | 内容 | 価格帯 |
|----|------|--------|
| **L1: PoC階段** | ML予測1本＋月1回30分MTG。IT導入補助金で実質¥30,000/月。3ヶ月固定、効果実証後L2移行。 | **¥60,000/月（3ヶ月固定）** |
| **L2: 人+AIバンドル** | ML予測4本＋月1回60分施策MTG＋月次自動レポート（PDF）＋SNS自動化1本。ECコンサル月¥30万比で「半額＋ツール込み」。 | **¥170,000/月** |
| **L3: 戦略伴走** | L2全機能＋月2MTG＋カスタムML＋四半期戦略レビュー。**要パイロット検証**（1社×6週間以上完了が前提）。 | **¥250,000/月** |

> **主訴求3要素（全コミュニケーション共通）:**
> 1. IT導入補助金対応（実質負担1/2、申請代行込み）
> 2. 3ヶ月PoC階段（¥6万から始め、効果実証後L2へ）
> 3. 人+AI伴走（ECコンサル半額、月1MTGで効果確認）

> **用語の戦略的撤退:**「逆SHAP What-Ifシミュレーター」を全文書で廃止 → **「ML予測+月次レビュー+IT補助金対応+日本特化」** に統一（v2.1.1完全移行済み）

### 競合ポジショニング（価格帯）

| 競合カテゴリ | 代表ツール | 月額 | 脅威度 |
|-------------|----------|------|--------|
| Shopify Magic | Shopify公式AI | 無料 | **高** |
| Klaviyo CRM内蔵AI | Klaviyo | $150〜 | **高** |
| 汎用AI | GPT-5 / Claude Opus 4.x | ¥3,000 | **高** |
| 需要予測SaaS | UMWELT / FOREMAST | ¥5千〜50万 | 低 |
| 国産ECコンサル | StoreHero他 | ¥30〜100万 | 中 |
| **当社 L1-L3** | EC横断分析+人+AI | **¥6〜25万** | — |

> **差別化軸**: IT導入補助金対応（実質1/2負担）＋3ヶ月PoC階段＋人+AI伴走（月1MTG）＋日本特化（薬機法/景表法/季節性）

---

## 4シナリオ比較（v2.1.1 整合性監査済）

| シナリオ | 確率 | M24 MRR | 24ヶ月累計利益 | M24時給（全工数） |
|---------|------|---------|-------------|----------------|
| **楽観** | 15% | ¥150万 | ¥2,000万 | **¥50K** |
| **標準** | 50% | ¥110万 | ¥1,400万 | **¥35K** |
| **悲観** | 25% | ¥50万 | ¥600万 | **¥18K**（撤退ライン近接を明示） |
| **ワースト** | 10% | ¥20万 | ¥150万 | **¥6K** |
| **期待値** | — | ¥98万 | ¥1,260万 | **¥31K** |

> **v2→v2.1修正**: 「悲観で時給¥31K」を「¥18K」に修正（単位混乱解消、月32h×24=768h一貫使用）
> **時給算出式**: 売上工数ベース（月20h上限）= MRR/20h、全工数ベース（月32h）= MRR/32h を明示区別

---

## 標準シナリオ 月次MRR推移

| 月 | L1客数 | L2客数 | L3客数 | Network | MRR | 時給(全体) | マイルストーン |
|---|--------|--------|--------|---------|-----|-----------|--------------|
| M3 | 1 | 0 | 0 | ¥3万 | **¥9万** | ¥2.8K | 初回L1 PoC締結 |
| M6 | 2 | 1 | 0 | ¥3万 | **¥32万** | ¥10K | **暫定PMF判定**（継続率67%/NPS25） |
| M9 | 2 | 2 | 0 | ¥9万 | **¥55万** | ¥17K | L2 2社目アップセル完了 |
| M12 | 2 | 2 | 1 | ¥15万 | **¥86万** | ¥27K | **本PMF判定**（継続率67%/NPS30） |
| M18 | 1 | 3 | 1 | ¥15万 | **¥97万** | ¥30K | テンプレ化・工数効率化 |
| M24 | 1 | 4 | 1 | ¥15万 | **¥110万** | ¥35K | **目標達成** |

> L1¥6万 / L2¥17万 / L3¥25万 / Network = Expert Network（ビザスク/GLG）単発収益
> M13以降は1h→1.3h換算でテンプレ化保守コストを反映

---

## PMF二段階判定基準

| タイミング | 判定区分 | 継続率 | NPS | 時給（全工数） | 判定 |
|-----------|---------|-------|-----|-------------|------|
| **M6** | 暫定Go/Kill | ≥ 67% | ≥ 25 | ≥ ¥10K | 3指標全クリア → L2展開 |
| **M12** | 本判定 | ≥ 67% | ≥ 30 | ≥ ¥15K | 3指標全クリア → 事業継続 |

---

## Kill基準（5段階）

| タイミング | 最優先Kill条件 | 補助条件 |
|-----------|--------------|---------|
| **M3** | 契約0件（最優先） | 商談8件達成・継続率0% |
| **M6** | パイロット0件 OR 時給¥8K未満 | NPS15未満 |
| **M12** | 本PMF不達（継続率<67% AND NPS<25） | 時給¥10K未満 |
| **M18** | MRR成長停滞（3ヶ月連続減少） | 新規獲得0件 |
| **M24** | 累計利益¥250,000（¥25万）未満 | — |

> M3 Kill: 「商談8件達成・契約0件」は契約0件でKill発動（v2.1.1で修正済み）

---

## 月32h工数配分（Phase0: M1-M3）

| 活動 | 時間/月 | 備考 |
|------|--------|------|
| 商談・営業 | 8h | ECzine/ビザスク/知人紹介リード |
| 診断・提案 | 4h | 無償EC診断レポート |
| PoC納品 | 4h | L1パイロット実施 |
| コンテンツ | 4h | note記事 or ECzine寄稿 |
| Network | 4h | ビザスク/GLG登録・対応 |
| 開発 | 6h | Shopifyアプリ化（M3-M15の5段階） |
| 学習 | 2h | EC事業者インサイト収集 |
| **合計** | **32h** | — |

---

## 関連ドキュメント

| リポジトリ | ファイル | 概要 |
|-----------|---------|------|
| **freelance-compass** | [outputs/integrated-business-plan-v2/](https://github.com/KazuyaMurayama/freelance-compass/tree/main/outputs/integrated-business-plan-v2) | 本計画の詳細ファイル群（01-06） |
| **freelance-compass** | [outputs/weekly-execution-plan.md](https://github.com/KazuyaMurayama/freelance-compass/blob/main/outputs/weekly-execution-plan.md) | 週次実行計画 |
| **machinelearning_app** | [docs/ec-business-alignment.md](https://github.com/KazuyaMurayama/MachineLearning_App/blob/main/docs/ec-business-alignment.md) | EC MVP × 事業計画整合性（v2.1.1） |
| **machinelearning_app** | [docs/sales-assets/pricing-and-scope.md](https://github.com/KazuyaMurayama/MachineLearning_App/blob/main/docs/sales-assets/pricing-and-scope.md) | 料金体系SSOT |
| **machinelearning_app** | [docs/step6_revised_strategy.md](https://github.com/KazuyaMurayama/MachineLearning_App/blob/main/docs/step6_revised_strategy.md) | EC GTM改訂戦略 |

---

## v2.1.1 残課題（B優先度）

| 課題 | 状況 | 対応時期 |
|------|------|---------|
| Phase1一次データ参照不在 | インタビュー0件段階での仮説ベース | M1-M2インタビュー5社で補完 |
| ec-dashboardのML充足率45% | L1完成のボトルネック | M1-M2開発（6h/月枠） |
| 中堅EC向け補助金外の価格正当化 | IT補助金使えない場合のWTP論拠弱い | M3商談フィードバックで検証 |

---

*本 INDEX は v2.1.1 統合事業計画の要約。詳細はパート別ファイル（01-06）を参照。*
*machinelearning_app側対応ドキュメント: `docs/ec-business-alignment.md`（v2.1.1整合済）*
