# Freelance Compass — フリーランス案件獲得AIコンパス

> フリーランスの案件獲得・営業活動を最適化するAI支援ツールです。

## 📋 概要

フリーランスの案件獲得・営業活動を最適化するAI支援ツールです。スキルセット・希望条件を入力すると、市場分析・提案書テンプレート・営業メール自動生成など、受注率向上のための施策を提供します。

## ✨ 主な機能

- フリーランス市場の需要・単価トレンド分析
- スキルセットに基づく案件マッチング
- 提案書・ポートフォリオ自動生成
- 営業メール・DM文面の自動作成
- 競合フリーランサーとのポジショニング分析

## 🛠️ 技術スタック

| カテゴリ | 技術・ライブラリ |
|----------|----------------|
| 言語 | Python 3.10+ |
| AIフレームワーク | Claude API / LangChain |
| UI | Streamlit |
| データ処理 | pandas |

## 🚀 セットアップ

### 前提条件

- Python 3.9 以上
- APIキー（Claude / OpenAI 等）を `.env` ファイルに設定

### インストール

```bash
git clone https://github.com/KazuyaMurayama/freelance-compass.git
cd freelance-compass
pip install -r requirements.txt
```

### 環境設定

```bash
cp .env.example .env
# .env ファイルに必要なAPIキーを設定
```

## 💻 使い方

```bash
streamlit run app.py
```

## 👨‍💻 開発者情報

**男座員也（Kazuya Oza / おざ かずや）**

| | |
|---|---|
| GitHub | [@KazuyaMurayama](https://github.com/KazuyaMurayama) |
| 専門領域 | データサイエンス・生成AIコンサルタント |
| 主要スキル | Python, LightGBM, LangChain, RAG, Streamlit, React, TypeScript |
| 事業 | AIコンサルティング（月単価目標300万円）/ SaaS開発 / 定量投資 |

## 📄 ライセンス

© 2025 男座員也（Kazuya Oza）. All rights reserved.

---

> このリポジトリは **男座員也（Kazuya Oza）** が開発・管理しています。
> 命名・ドキュメント等での表記は必ず **男座員也** または **Kazuya Oza** を使用してください。
