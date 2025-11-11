# ディレクトリ構造・ファイル配置ルール

このファイルは、aurumプロジェクトのディレクトリ構造とファイル配置ルールを定義します。

## 🔴 reports/に書き込む前に必ず読むこと

**reports/の配置ルール:**
- 作業中: `outputs/reports/working/yyyymm/yyyymmdd_テーマ/`
- 完了: `outputs/reports/completed/yyyymm/yyyymmdd_テーマ/`

**必ず月ディレクトリ（yyyymm）を挟むこと！**

---

## ディレクトリ構成

```
aurum/
├── .claude/                        ← Claude Code設定
│   ├── agents/                     ← エージェント定義
│   ├── glossaries/                 ← 用語集（エージェント共有）
│   ├── 00_work_checklist.md        ← 作業開始時チェックリスト
│   ├── 01_project_overview.md      ← プロジェクト概要・投資哲学
│   ├── 02_directory_structure.md   ← ディレクトリ構造（本ファイル）
│   ├── 03_work_process.md          ← 作業プロセス
│   ├── 03a_work_levels.md          ← 作業レベル定義
│   ├── 03b_project_workflow.md     ← プロジェクト管理
│   ├── 03c_agent_discussion.md     ← エージェント議論
│   ├── 04_python_guide.md          ← Python開発ガイド
│   ├── 05_reference.md             ← リファレンス
│   ├── 06a_three_agent_overview.md ← 3エージェント評価（概要）
│   ├── 06b_three_agent_detailed.md ← 3エージェント評価（詳細）
│   ├── 06c_weight_adjustment_rules.md ← ウェイト調整ルール
│   ├── 07_analysis_guidelines.md   ← 分析ガイドライン
│   ├── 08_glossary.md              ← 用語集
│   ├── 09_baseline_evaluation.md   ← ベースライン評価
│   ├── 10_glossary.md              ← 用語集（優先度付き）
│   └── history.md                  ← 改善履歴
│
├── document/                       ← ドキュメント
│   ├── examples.md                 ← 使用例
│   ├── PERSONAL_DATA.template.md   ← 個人情報テンプレート
│   ├── setup_guide.md              ← セットアップガイド
│   └── tutorial.md                 ← チュートリアル
│
├── outputs/                        ← 生成データ（自動生成、.gitignore対象）
│   ├── python/                     ← Python実行結果⭐
│   │   ├── cache/                  ← キャッシュファイル
│   │   ├── screening/              ← スクリーニング結果
│   │   └── temp/                   ← 一時ファイル
│   │
│   └── reports/                    ← 分析レポート⭐
│       ├── completed/              ← 最終レポート
│       │   └── yyyymm/             ← 月別ディレクトリ
│       │       └── yyyymmdd_テーマ/  ← 日付_テーマ形式
│       │
│       └── working/                ← 作業中ファイル
│           ├── temp_n.md           ← 単一ファイル（軽量作業）
│           └── yyyymm/             ← 月別ディレクトリ
│               └── yyyymmdd_テーマ/  ← 日付_テーマ形式
│
├── python/                         ← Pythonスクリプト
│   ├── config/                     ← 設定モジュール
│   │   ├── __init__.py
│   │   ├── constants.py            ← 定数定義
│   │   ├── paths.py                ← パス統一管理
│   │   ├── personal.py             ← 個人設定（.gitignore対象）
│   │   ├── personal.template.py    ← 個人設定テンプレート
│   │   └── simulation.py           ← シミュレーション設定
│   ├── config.py                   ← レガシー設定ファイル
│   ├── controllers/                ← エントリーポイント
│   ├── create_templates.py         ← テンプレート生成スクリプト
│   ├── main/                       ← メインスクリプト
│   ├── models/                     ← データロジック
│   │   ├── analysis/               ← 分析モデル
│   │   └── screening/              ← スクリーニングモデル
│   ├── personal_config.template.py ← レガシー個人設定テンプレート
│   └── services/                   ← 共通サービス
│       └── visualization/          ← 可視化サービス
│
├── sources/                        ← ソースデータ（手動管理）
│   ├── profile/                    ← 投資プロフィール（機密、.gitignore対象）⭐
│   │   ├── historical/             ← 過去データアーカイブ
│   │   ├── templates/              ← テンプレートファイル
│   │   │   ├── asset_details.template.md
│   │   │   └── investment_history.template.md
│   │   ├── asset_details.md        ← 資産詳細（.gitignore対象）
│   │   └── investment_history.md   ← 投資履歴（.gitignore対象）
│   │
│   └── reference/                  ← 参考資料（.gitignore対象）⭐
│       ├── csv/                    ← CSVファイル
│       │   └── payment/            ← 支払データ
│       ├── image/                  ← 画像ファイル
│       ├── market/                 ← マクロ経済見通し
│       │   └── macro_economic_outlook_2025-2035.md
│       └── pdf/                    ← PDFファイル
│
├── tests/                          ← テスト
│   ├── conftest.py                 ← Pytest設定
│   ├── fixtures/                   ← テストデータ
│   ├── integration/                ← 統合テスト
│   └── unit/                       ← 単体テスト
│
├── .gitignore                      ← Git除外設定
├── CHANGELOG.md                    ← 変更履歴
├── CLAUDE.md                       ← プロジェクト設定・ガイドライン
├── CODE_OF_CONDUCT.md              ← 行動規範
├── CONTRIBUTING.md                 ← 貢献ガイドライン
├── INVESTMENT_PROFILE.template.md  ← 投資プロフィールテンプレート
├── LICENSE                         ← MITライセンス
├── pytest.ini                      ← Pytest設定ファイル
├── README.md                       ← プロジェクト概要
└── requirements.txt                ← Python依存パッケージ
```

---

## ファイル配置ルール

### ❌ reports/：ルート直下への配置は厳禁

**重要ルール:**
- `reports/`ルート直下には**いかなるファイルも配置しない**
- すべてのドキュメントは必ず以下のいずれかに配置：
  - `outputs/reports/working/yyyymm/yyyymmdd_テーマ/` - 作業中ファイル（月別→日別の階層構造）
  - `outputs/reports/completed/yyyymm/yyyymmdd_テーマ/` - 最終成果物（月別→日別の階層構造）
- **例外なし**（一時ファイル、バックアップも含む）

**❌ 禁止例:**
```
outputs/reports/
├── レポート.md          ← NG
├── 分析結果.csv         ← NG
└── メモ.txt             ← NG
```

**✅ 正しい配置:**
```
outputs/reports/
├── working/202511/20251107_zenn執筆/
│   └── chapter_1_人間化版.md        ← OK
└── completed/202511/20251109_external_release_preparation/
    └── README.md                    ← OK
```

---

### 🔴 aurumルート：根幹ファイルのみ

**配置すべきファイル:**
- 人生設計を左右する基盤ファイル
- プロジェクト全体の設定ファイル

**例:**
- `INVESTMENT_PROFILE.md` - 投資プロフィール・マスターファイル
- `CLAUDE.md` - プロジェクト設定
- `README.md` - プロジェクト概要

**❌ 配置してはいけないもの:**
- 日々の調査ファイル
- 一時的なメモ
- 中間成果物

---

### 📁 outputs/reports/working/：作業中ファイル ⭐NEW

**用途:**
- 計画段階のファイル
- 調査・分析中間ファイル
- エージェント間の議論ログ
- 要件定義・詳細ドキュメント
- TODOリスト

**命名ルール（2025年11月7日更新）:**

#### temp_n形式（推奨）⭐
```
outputs/reports/working/
├── temp_1.md          ← 単一ファイル（軽量作業）
├── temp_2/            ← ディレクトリ（複数ファイル）
│   ├── 要件定義.md
│   ├── data.csv
│   └── graph.png
└── temp_3.md          ← 単一ファイル
```

**特徴:**
- 連番（temp_1, temp_2, ...）で即座に作業開始
- 単一ファイル（.md）から開始可能
- 2ファイル目追加時にAIが自動的にディレクトリ化
- 完了時にAIが命名候補を提案 → `reports/yyyymm/yyyymmdd_テーマ/` へ移動

**ワークフロー:**
1. **Phase 1**: `temp_n.md` で軽量スタート
2. **Phase 2**: 複数ファイル必要時、AIが `temp_n/` に自動昇格
3. **Phase 3**: 完了時、AIが命名提案 → `reports/yyyymm/yyyymmdd_テーマ/` へ移動

詳細は `.claude/03_work_process.md` の「プロジェクト管理のワークフロー」を参照

#### 月別→日付形式（標準）⭐NEW
```
outputs/reports/working/
├── 202510/                    ← 月別ディレクトリ
│   ├── 20251026_ベビーシッター助成/
│   └── 20251031_自社株売却/
└── 202511/                    ← 月別ディレクトリ
    ├── 20251103_支出改善/
    ├── 20251107_zenn執筆/
    └── 20251107_macro_update/
```

**特徴:**
- **必ず `yyyymm/yyyymmdd_テーマ/` の階層構造を使用**
- 月別に整理され、過去の作業を探しやすい
- 長期保管に適している

**ルール:**
- 新規作業は必ず `yyyymm/` 配下に配置
- ルート直下に `yyyymmdd_テーマ/` を作成しない
- 例: `working/20251107_テーマ/` ❌ → `working/202511/20251107_テーマ/` ✅

---

### 📊 outputs/reports/completed/：最終レポート ⭐NEW

**用途:**
- 完成した分析レポート
- 投資判断の結論
- エグゼクティブサマリー
- 最終的な統計データ

**命名ルール（2025年11月7日更新）:**

#### 月別→日付_テーマ形式（標準）⭐
```
outputs/reports/completed/
├── 202510/                           ← 月別ディレクトリ
│   ├── 20251026_ベビーシッター助成/
│   └── 20251031_自社株売却戦略/
│       └── 統計分析レポート.md
└── 202511/                           ← 月別ディレクトリ
    ├── 20251101_包括的投資分析/
    │   ├── COMPREHENSIVE_INVESTMENT_ANALYSIS.md
    │   └── NISA_2026_ANALYSIS_REPORT.md
    ├── 20251103_支出改善アクション/
    │   ├── アクションプラン.md
    │   ├── 支出データ.csv
    │   └── グラフ.png
    └── 20251107_PROFILE見直し議論/
```

**特徴:**
- **必ず `yyyymm/yyyymmdd_テーマ/` の階層構造を使用**
- 月別に整理され、過去のレポートを探しやすい
- 日付とテーマを両方含む（`yyyymmdd_テーマ/`）
- 関連するすべてのファイル（MD、CSV、PNG）を1箇所に集約
- AIが `working/temp_n/` から自動的に命名提案
- 完了日が明確（yyyymmdd）

**ルール:**
- 新規レポートは必ず `yyyymm/` 配下に配置
- ルート直下に `yyyymmdd_テーマ/` を作成しない
- 例: `reports/20251107_テーマ/` ❌ → `reports/202511/20251107_テーマ/` ✅

**命名例:**
- `outputs/reports/completed/202511/20251103_支出改善アクション/`
- `outputs/reports/completed/202511/20251102_米国株分析結果/`
- `outputs/reports/completed/202511/20251101_NISA運用戦略/`

**注意:** 既存の日付のみディレクトリはそのまま使用可能ですが、新規レポートは `yyyymmdd_テーマ` 形式を推奨

**workingとの使い分け基準:**
- ✅ **outputs/reports/completed/yyyymm/yyyymmdd_テーマ/**に配置すべきもの：
  - 意思決定に使用できる完成版レポート
  - 他者（家族・第三者）に共有できる最終成果物
  - 「アクションプラン」「エグゼクティブサマリー」等の最終文書
  - 複数の分析を統合した結論

- 📋 **outputs/reports/working/temp_n/**に配置すべきもの：
  - データ集計・現状把握レポート
  - 特定項目の深掘り調査
  - 中間バージョン・改善版
  - 議論ログ・TODOリスト
  - 付属CSVファイル（スクリーニング結果等）

**昇格のタイミング:**
- `outputs/reports/working/temp_n/` で作業完了
- AIに「temp_nを完了させたい」と伝える
- AIが3つの命名候補を提案
- ユーザーが選択 → `outputs/reports/completed/yyyymm/yyyymmdd_テーマ/` へ移動

---

### 🐍 python/：Pythonスクリプト（機能別整理）

**サブディレクトリ構造:**

- **`python/main/`** - メイン分析スクリプト
  - `investment_analysis.py` - 基本投資分析
  - `company_stock_analysis.py` - 自社株分析
  - `stock_analysis.py` - 株式分析

- **`python/screening/`** - スクリーニング系
  - `phase1_*.py` - 段階的スクリーニング
  - `imura_method_*.py` - Imuraメソッド関連
  - `generate_*.py` - データ生成系

- **`python/analysis/`** - 詳細分析系
  - `japanese_stock_analysis*.py` - 日本株分析
  - `us_stocks_analysis*.py` - 米国株分析
  - `nisa_*.py` - NISA関連分析
  - `integrated_risk_analysis*.py` - リスク分析

- **`python/visualization/`** - グラフ生成系
  - `plot_*.py` - グラフ描画
  - `create_analysis_visualizations.py` - 可視化

- **`python/utilities/`** - ユーティリティ・補助スクリプト
  - `add_*.py` - データ追加系
  - `analyze_*.py` - 簡易分析系
  - `test_*.py` - テストスクリプト

**パス管理:**
- すべてのスクリプトは`python/config/paths.py`を使用してパスを統一管理
- 詳細は「04_python_guide.md」参照

---

### 📊 sources/：ソースデータ（ユーザーが配置）⭐

**用途:**
- ユーザーが手動で配置する入力データ
- INVESTMENT_PROFILE.mdから分割された詳細データ
- マクロ経済見通し・市場データ
- 画像・PDF・CSV等の参照ファイル

**サブディレクトリ:**

#### `sources/profile/` - 投資プロフィール（機密データ）
  - `asset_details.md` - 資産詳細（NISA・iDeCo・自社株）
  - `investment_history.md` - 投資判断履歴・評価履歴
  - `templates/` - テンプレートファイル
    - `asset_details.template.md`
    - `investment_history.template.md`
  - `historical/` - 過去データアーカイブ

#### `sources/reference/` - 参考資料
  - `csv/` - CSVファイル
    - `payment/` - 支払データ（家計簿）
  - `pdf/` - PDFファイル（レポート、参考資料）
  - `image/` - 画像ファイル（スクリーンショット、銘柄リスト等）
  - `market/` - マクロ経済見通し
    - `macro_economic_outlook_2025-2035.md`

**ルール:**
- このディレクトリのファイルは`.gitignore`で除外対象
- 個人情報・金融情報が含まれるため機密性が高い
- Pythonスクリプトはここから入力データを読み込む

---

### 🔧 outputs/python/：出力データ（Python生成）⭐

**用途:**
- Pythonスクリプトが自動生成するファイルの保存先
- 分析結果・シミュレーション結果
- グラフ・可視化画像
- キャッシュ・一時ファイル

**サブディレクトリ:**

- **`outputs/python/screening/`** - スクリーニング結果
  - `stock_screening_yyyymmdd.csv` - 株式スクリーニング結果
  - `phase1_results.csv` - Phase 1スクリーニング

- **`outputs/python/cache/`** - キャッシュファイル
  - `market_data_cache_yyyymmdd.json` - 市場データキャッシュ（API呼び出し削減）
  - `yfinance_cache/` - yfinanceライブラリのキャッシュ

- **`outputs/python/temp/`** - 一時ファイル
  - `intermediate_calculation.tmp` - 計算途中の一時ファイル
  - スクリプト実行中の中間データ

**ルール:**
- このディレクトリのファイルは`.gitignore`で除外対象
- スクリプト実行前に自動作成される
- 不要になったファイルは定期的に削除してOK
- cacheディレクトリは定期的にクリア推奨（古いデータが残る）

**Pythonスクリプトでの使用:**
```python
from python.config.paths import OUTPUTS_PYTHON_DIR, OUTPUTS_PYTHON_CACHE_DIR

# 出力ファイルのパス
output_path = OUTPUTS_PYTHON_DIR / "screening" / f"results_{date}.csv"

# キャッシュファイルのパス
cache_path = OUTPUTS_PYTHON_CACHE_DIR / f"market_data_{date}.json"
```

---

### 🗄️ .bak/：バックアップと一時ファイル

**用途:**
- 手動バックアップファイル
- 一時的な作業ファイル（不要になったもの）
- 古いスクリプト・設定ファイル
- 削除前の一時保管場所

**ルール:**
- ファイル名は元の名前を保持（例: `CLAUDE.md.bak`）
- 必要に応じて日付サフィックスを追加（例: `CLAUDE.md.backup_20251102`）
- 整理不要（雑に入れてOK）
- Git管理外（.gitignoreに追加推奨）
- 定期的な削除OK（重要ファイルは別途保管）

**例:**
```
.bak/
├── CLAUDE.md.bak
├── CLAUDE.md.backup_20251102
├── INVESTMENT_PROFILE.md.backup_20251103
├── update_claude_md.py
├── split_investment_profile.py
└── old_notes.txt
```

**使い分け:**
- `.bak/` - 一時的なバックアップ・不要ファイル（気軽に削除可能）
- `outputs/reports/working/temp_n/` - 進行中の作業（削除不可）
- `outputs/reports/completed/yyyymm/yyyymmdd_テーマ/` - 完成した成果物（永久保存）

---

### 📤 出力データの保存先 ⭐NEW

**重要変更（2025年11月3日）:**
従来の `output/` ディレクトリは廃止されました。

**新しい保存先:**

#### 作業中のデータ → `outputs/reports/working/temp_n/`
```python
# 例: temp_1プロジェクトに画像・CSV保存
from python.config.paths import OUTPUTS_REPORTS_WORKING_DIR
project_dir = os.path.join(OUTPUTS_REPORTS_WORKING_DIR, 'temp_1')
plt.savefig(os.path.join(project_dir, 'chart.png'))
df.to_csv(os.path.join(project_dir, 'results.csv'))
```

#### 完成したデータ → `outputs/reports/completed/yyyymm/yyyymmdd_テーマ/`
```python
# 例: 完了時にreportsへ移動（AIが支援）
# ユーザー: "temp_1を完了させたい"
# AI: 命名提案 → outputs/reports/completed/202511/20251103_支出改善アクション/へ移動
```

**ディレクトリ例:**
```
outputs/reports/
├── working/
│   └── temp_1/
│       ├── 要件定義.md
│       ├── data.csv         ← スクリプトが生成
│       └── graph.png        ← スクリプトが生成
└── completed/202511/
    └── 20251103_支出改善アクション/
        ├── アクションプラン.md
        ├── 支出データ.csv   ← 完了時に移動
        └── グラフ.png       ← 完了時に移動
```

**メリット:**
- 関連ファイル（MD、CSV、PNG）が1箇所に集約
- プロジェクト単位で完全に自己完結
- ファイルの所属が明確

---

**最終更新**: 2025年11月11日（公開用整理完了: 古いディレクトリ構造（data/, docs/）を新構造（sources/, outputs/, document/）に全面更新）
