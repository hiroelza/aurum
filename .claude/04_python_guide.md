# Python開発ガイド

このファイルは、aurumプロジェクトでのPythonスクリプトの開発・実行ガイドを定義します。

## 開発環境

### 必要なパッケージ

```bash
pip install numpy pandas scipy matplotlib
```

---

## Pythonスクリプトの実行方法

### 実行ディレクトリ

**重要**: すべてのPythonスクリプトは`aurum/`ディレクトリから実行してください。

```bash
# 正しい実行方法
cd .
python python/main/investment_analysis.py
python python/visualization/plot_company_stock_comparison.py

# 誤った実行方法（動作しません）
cd python/main
python investment_analysis.py  # NG
```

### メイン分析スクリプトの実行

```bash
# 投資分析の実行
python python/main/investment_analysis.py
```

**出力内容:**
1. 家計収支バランスの統計分析
2. 投資額シミュレーション（3パターン × 3シナリオ）
3. 現金保有率の評価
4. 資産配分の分析（自社株リスク含む）
5. 教育費達成確率（モンテカルロ10,000回シミュレーション）

---

## よく使うBashコマンド

### 投資分析の実行

```bash
# 基本投資分析
cd .
python python/main/investment_analysis.py

# 自社株分析
python python/main/company_stock_analysis.py

# 株式分析
python python/main/stock_analysis.py
```

### 出力ファイルの確認

```bash
# 最新の画像ファイル（グラフ）
ls -lt output/image/ | head -5

# 最新のCSVファイル
ls -lt output/csv/ | head -5

# 最新の分析レポート
ls -lt outputs/reports/completed/ | head -5
```

### ディレクトリ操作

```bash
# 今日の作業ディレクトリを作成
mkdir -p outputs/reports/working/$(date +%Y%m%d)

# 今日の作業ディレクトリに移動
cd outputs/reports/working/$(date +%Y%m%d)

# 現在のディレクトリ確認
pwd
```

### Git操作（投資判断時）

```bash
# 投資プロフィール更新時
git add INVESTMENT_PROFILE.md
git commit -m "資産状況更新: [日付] [変更内容]"

# 分析レポート追加時
git add outputs/reports/completed/
git commit -m "分析レポート追加: [テーマ]"

# 複数ファイル更新時
git add INVESTMENT_PROFILE.md outputs/reports/completed/
git commit -m "投資判断記録: [商品名]"
```

### 便利なコマンド

```bash
# すべてのPythonスクリプトを一覧表示
find python/ -name "*.py" -type f

# 特定の文字列を含むスクリプトを検索
grep -r "INVESTMENT" python/

# 最近変更されたファイルTop 10
find . -type f -mtime -7 -ls | sort -k11 -r | head -10
```

---

## パス管理

### python/config.py による統一管理

すべてのPythonスクリプトは`python/config.py`でパスを統一管理しています：

- **IMAGE_DIR**: `aurum/outputs/python/image/` - 画像ファイルの保存先
- **INPUT_CSV_DIR**: `aurum/sources/profile/csv/` - 入力CSVファイル
- **OUTPUT_CSV_DIR**: `aurum/outputs/python/csv/` - 出力CSVファイル
- **REPORTS_DIR**: `aurum/outputs/reports/completed/` - 最終レポート
- **WORKING_DIR**: `aurum/outputs/reports/working/` - 作業中ファイル

**後方互換性:**
- `CSV_DIR` = `INPUT_CSV_DIR`（非推奨、INPUT_CSV_DIR使用推奨）
- `RESULT_DIR` = `REPORTS_DIR`（非推奨）
- `RESEARCH_DIR` = `WORKING_DIR`（非推奨）

### config.pyの内容

```python
import os

# ベースディレクトリの設定
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # python/
BASE_DIR = os.path.dirname(BASE_DIR)  # aurum/

# 各ディレクトリパス
IMAGE_DIR = os.path.join(BASE_DIR, 'output', 'image')
INPUT_CSV_DIR = os.path.join(BASE_DIR, 'input', 'csv')
OUTPUT_CSV_DIR = os.path.join(BASE_DIR, 'output', 'csv')
DOCUMENT_DIR = os.path.join(BASE_DIR, 'document')
REPORTS_DIR = os.path.join(DOCUMENT_DIR, 'reports')
WORKING_DIR = os.path.join(DOCUMENT_DIR, 'working')

# 後方互換性のため
CSV_DIR = INPUT_CSV_DIR
RESULT_DIR = REPORTS_DIR
RESEARCH_DIR = WORKING_DIR
```

---

## 新しいスクリプトを作成する場合

### 基本テンプレート

```python
import sys
import os

# config.pyをimport
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import IMAGE_DIR, INPUT_CSV_DIR, OUTPUT_CSV_DIR, REPORTS_DIR, WORKING_DIR

# 入力CSVを読み込み
import pandas as pd
df = pd.read_csv(os.path.join(INPUT_CSV_DIR, 'input_data.csv'))

# 画像を保存
import matplotlib.pyplot as plt
plt.savefig(os.path.join(IMAGE_DIR, 'chart.png'))

# 出力CSVを保存
df.to_csv(os.path.join(OUTPUT_CSV_DIR, 'results.csv'))
```

### スクリプト配置場所の選定

新しいスクリプトは機能に応じて以下のディレクトリに配置：

- **`python/main/`** - メインの分析スクリプト
- **`python/screening/`** - スクリーニング・データ生成
- **`python/analysis/`** - 詳細分析・リスク分析
- **`python/visualization/`** - グラフ・可視化
- **`python/utilities/`** - 補助的なユーティリティ

---

## コーディング規約

### Pythonスクリプト

- **日本語コメント**: コード内のコメントは日本語で記述
- **変数名**: 英語（わかりやすい命名）
- **統計関数**: NumPy/SciPy/Pandasを活用
- **可視化**: Matplotlibで日本語対応（MS Gothic/Yu Gothic）
- **出力**: 見やすい罫線区切りで結果表示

### フォント設定（Matplotlib）

```python
import matplotlib.pyplot as plt

# 日本語フォント設定
plt.rcParams['font.sans-serif'] = ['MS Gothic', 'Yu Gothic', 'Hiragino Sans']
plt.rcParams['axes.unicode_minus'] = False
```

---

## よくある操作

### シミュレーションパラメータの変更

`python/personal_config.py`の以下の変数を編集：

```python
# 基本情報
CURRENT_AGE = [YOUR_AGE]  # 例: 35
CURRENT_NISA = [NISA_ASSETS]  # 例: 760
CURRENT_IDECO = [IDECO_ASSETS]  # 例: 60
# ... 等

# 月次投資額
CURRENT_MONTHLY_NISA = [MONTHLY_NISA]  # 例: 10.0
CURRENT_MONTHLY_IDECO = [MONTHLY_IDECO]  # 例: 2.3
# ... 等
```

**注意**: python/main/投下のスクリプトに直接ハードコードしないでください。必ず`personal_config.py`を編集してください。

### 新しいシミュレーションパターンの追加

`simulate_investment_pattern()`関数を使用：

```python
pattern_new = simulate_investment_pattern(
    "パターン名",
    monthly_2025_2026=12.3,
    monthly_2027_onwards=16.2
)
```

---

## 一般的なワークフロー

### 1. 投資判断を行う時

#### Step 0: 要件定義（Plan Mode）
```bash
# 1. 何の投資判断か明確化
# 2. 必要な情報を特定
# 3. outputs/reports/working/yyyymmdd/要件定義_[投資商品].md を作成
```

#### Step 1: 情報収集

```bash
# 1. INVESTMENT_PROFILE.mdを確認
# 2. 必要に応じてinvestment_analysis.pyを実行
python python/main/investment_analysis.py

# 3. 3エージェント評価を実施
# 4. 判断結果をINVESTMENT_PROFILE.mdに記録
```

### 2. 資産状況を更新する時

```bash
# 1. INVESTMENT_PROFILE.mdの「資産状況」セクションを更新
# 2. python/main/investment_analysis.pyのパラメータを更新
# 3. シミュレーションを再実行
python python/main/investment_analysis.py
```

### 3. 新しい投資商品を検討する時

```bash
# 1. 3エージェント評価を実施
#    - hayato: 投資哲学との整合性
#    - researcher: 統計データ分析
#    - japanese: 税制・リスク評価
# 2. 評価結果（点数・支持度）を記録
# 3. INVESTMENT_PROFILE.mdに判断履歴を追加
```

---

**最終更新**: 2025年11月9日（Phase 3: output/削除、新ワークフロー対応）

---

## Phase 2: Python層の再構成（2025年11月9日）

### 新しいディレクトリ構造（MVC-like）

Pythonコードは以下のMVC-like構造に再編成されました：

```
python/
├── controllers/          # エントリーポイント、メイン実行スクリプト
│   ├── investment_analysis.py
│   ├── company_stock_analysis.py
│   └── stock_analysis.py
├── models/              # データロジック、シミュレーション、計算関数
│   ├── screening/       # スクリーニング・データ生成
│   └── analysis/        # 詳細分析・リスク分析
├── services/            # 再利用可能なサービス
│   └── visualization/   # グラフ・可視化
└── utilities/           # 補助的なユーティリティ
```

### 新しい実行方法（推奨）

```bash
# 投資分析の実行
python python/controllers/investment_analysis.py

# 自社株分析
python python/controllers/company_stock_analysis.py

# 株式分析
python python/controllers/stock_analysis.py
```

### 後方互換性（非推奨）

既存のパスも引き続き動作しますが、DeprecationWarningが表示されます：

```bash
# 非推奨: python/main/ からの実行
python python/main/investment_analysis.py
# ⚠️ DeprecationWarning: python.main is deprecated. Use python.controllers instead.
```

### 新しいconfig モジュールの使用

すべてのcontrollersスクリプトは新しいconfig モジュールを使用します：

```python
# 新しいimport方法
from config.personal import CURRENT_AGE, TOTAL_ASSETS, ...
from config.paths import IMAGE_DIR, INPUT_CSV_DIR, ...
from config.simulation import MONTE_CARLO_ITERATIONS, ...
from config.constants import HIGH_RISK_THRESHOLD, ...
```

### スクリプト配置場所の選定（更新版）

新しいスクリプトは機能に応じて以下のディレクトリに配置：

- **`python/controllers/`** - エントリーポイント、メイン分析スクリプト
- **`python/models/screening/`** - スクリーニング・データ生成
- **`python/models/analysis/`** - 詳細分析・リスク分析
- **`python/services/visualization/`** - グラフ・可視化
- **`python/utilities/`** - 補助的なユーティリティ

**非推奨（後方互換性のみ）:**
- `python/main/` → `python/controllers/` を使用してください
- `python/screening/` → `python/models/screening/` を使用してください
- `python/analysis/` → `python/models/analysis/` を使用してください
- `python/visualization/` → `python/services/visualization/` を使用してください

