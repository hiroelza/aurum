# セットアップガイド

このガイドでは、aurumプロジェクトのセットアップ方法を詳しく説明します。

---

## 動作環境

### 必須要件
- Python 3.8以上
- Git（オプション、バージョン管理を使用する場合）

### OS別の注意事項

#### Windows 10/11
- **開発・テスト環境**: MINGW64環境
- **推奨ターミナル**: Git Bash、PowerShell、Windows Terminal
- **文字コード**: UTF-8（`chcp 65001`で設定）

#### MacOS
- **Python**: `python3`コマンドを使用
- **文字コード**: デフォルトでUTF-8
- **注意**: Windows専用コマンド（`chcp`等）は省略

---

## セットアップ手順

### Step 1: リポジトリのクローン（または解凍）

```bash
# Gitを使用する場合
git clone <repository-url>
cd aurum

# ZIPファイルを解凍した場合
cd aurum
```

### Step 1.5: .gitignoreの確認（重要） 🔴

**Gitを使用する場合、必ず最初に確認してください。**

このプロジェクトには個人の金融情報が含まれます。誤ってコミットしないよう、`.gitignore`が正しく設定されているか確認してください。

```bash
# .gitignoreの内容を確認
cat .gitignore

# 以下のファイルが除外されていることを確認:
# - INVESTMENT_PROFILE.md
# - document/PERSONAL_DATA.md
# - sources/profile/asset_details.md
# - sources/profile/investment_history.md
# - sources/reference/
# - outputs/
# - python/config/personal.py
```

**リポジトリ初期化前の確認:**
```bash
# 初回コミット前に必ず実行
git status

# 機密ファイルが追跡されていないことを確認してからコミット
git add .
git commit -m "Initial commit"
```

### Step 2: テンプレートファイルのコピー

#### Windows（Git Bash）
```bash
# 必須ファイル
cp python/config/personal.template.py python/config/personal.py
cp INVESTMENT_PROFILE.template.md INVESTMENT_PROFILE.md

# 推奨ファイル（詳細な管理をする場合）
cp sources/profile/templates/asset_details.template.md sources/profile/asset_details.md
cp sources/profile/templates/investment_history.template.md sources/profile/investment_history.md
cp document/PERSONAL_DATA.template.md document/PERSONAL_DATA.md
```

#### Windows（PowerShell）
```powershell
# 必須ファイル
Copy-Item python\config\personal.template.py python\config\personal.py
Copy-Item INVESTMENT_PROFILE.template.md INVESTMENT_PROFILE.md

# 推奨ファイル（詳細な管理をする場合）
Copy-Item sources\profile\templates\asset_details.template.md sources\profile\asset_details.md
Copy-Item sources\profile\templates\investment_history.template.md sources\profile\investment_history.md
Copy-Item document\PERSONAL_DATA.template.md document\PERSONAL_DATA.md
```

#### MacOS
```bash
# 必須ファイル
cp python/config/personal.template.py python/config/personal.py
cp INVESTMENT_PROFILE.template.md INVESTMENT_PROFILE.md

# 推奨ファイル（詳細な管理をする場合）
cp sources/profile/templates/asset_details.template.md sources/profile/asset_details.md
cp sources/profile/templates/investment_history.template.md sources/profile/investment_history.md
cp document/PERSONAL_DATA.template.md document/PERSONAL_DATA.md
```

### Step 3: 個人情報の入力

**重要**: このプロジェクトでは、以下の5つのファイルすべてに情報を記録する必要があります。各ファイルの役割を理解してから編集してください。

#### 3-1. Python設定ファイルの編集（必須）

**ファイル**: `python/config/personal.py`

**役割**: Pythonスクリプトが実行時に読み込むデータファイル

**なぜ必要？**: モンテカルロシミュレーション、資産予測などのPythonスクリプトがこのファイルからデータを読み込みます。

**編集手順**:
```python
# プレースホルダーを実際の値に置き換え
YOUR_AGE = 35  # [YOUR_AGE] を置き換え
CURRENT_YEAR = 2025  # [CURRENT_YEAR] を置き換え
RETIREMENT_AGE = 65  # [RETIREMENT_AGE] を置き換え
YOUR_NISA = 500.0  # 万円単位 [YOUR_NISA] を置き換え
YOUR_ANNUAL_INCOME = 600.0  # 万円単位 [YOUR_ANNUAL_INCOME] を置き換え
```

#### 3-2. 投資プロフィールの編集（最重要）

**ファイル**: `INVESTMENT_PROFILE.md`

**役割**: 投資方針、資産状況、投資判断の記録を一元管理するマスターファイル

**なぜ必要？**:
- **Claude Codeがこのファイルを参照して投資アドバイスを提供します**
- プロジェクトの設計上、最も重要なファイルです
- `.claude/01_project_overview.md`で「必ず読むこと」と定義されています

**編集手順**: 同様にプレースホルダーを置き換えてください。

#### 3-3. 資産詳細の編集（推奨）

**ファイル**: `sources/profile/asset_details.md`

**役割**: 保有銘柄の詳細情報（取得単価、含み損益など）を記録

**なぜ必要？**:
- 具体的な銘柄情報を記録することで、リバランスや売却判断に役立ちます
- Claude Codeがポートフォリオ分析を実施する際に参照します

**編集手順**: サンプルデータを参考に、以下の情報を入力：
- 銘柄名
- ファンドコード
- 取得口数
- 取得単価
- 評価単価

#### 3-4. 投資履歴の編集（推奨）

**ファイル**: `sources/profile/investment_history.md`

**役割**: 過去の投資判断を時系列で記録

**なぜ必要？**:
- 過去の判断を振り返り、学習することができます
- 感情的な判断を防ぐために重要です

#### 3-5. 個人データの編集（オプション）

**ファイル**: `document/PERSONAL_DATA.md`

**役割**: 基本情報のバックアップ

**なぜ必要？**: INVESTMENT_PROFILE.mdのバックアップとして機能します

**編集手順**: 以下のプレースホルダーを実際の値に置き換えてください：

- `[YOUR_AGE]` → あなたの年齢
- `[SPOUSE_AGE]` → 配偶者の年齢（該当する場合）
- `[CHILD1_AGE]` → 子供1の年齢（該当する場合）
- `[YOUR_COMPANY]` → 勤務先
- `[ANNUAL_INCOME_GROSS]` → 税込年収
- `[ANNUAL_INCOME_NET]` → 税引後年収
- `[TOTAL_ASSETS]` → 総資産額
- `[NISA_ASSETS]` → NISA資産額
- など

**記入例:**
```markdown
- **年齢**: 35歳（2025年11月時点）
- **年収（税込）**: 約600万円
- **総資産**: 800万円
```

---

**最低限のセットアップ**: `python/config/personal.py` と `INVESTMENT_PROFILE.md` の2つを編集すれば、プロジェクトは動作します。

**推奨セットアップ**: すべてのファイルを編集することで、Claude Codeによる高度な分析が可能になります。

### Step 4: Python実行環境の確認

### Pythonバージョンの確認

#### Windows
```bash
python --version
```

#### MacOS
```bash
python3 --version
```

**必須**: Python 3.8以上

### 必要なパッケージのインストール

```bash
# Windows
pip install pandas numpy matplotlib

# MacOS
pip3 install pandas numpy matplotlib
```

---

## 初回実行

### Step 4: Pythonスクリプトの実行

#### Windows（Git Bash）
```bash
cd aurum

# 文字コードをUTF-8に設定
chcp 65001

# スクリプト実行
python python/controllers/investment_analysis.py
```

#### Windows（PowerShell）
```powershell
cd aurum

# 文字コードをUTF-8に設定
chcp 65001

# スクリプト実行
python python\main\projection.py
```

#### MacOS
```bash
cd aurum

# スクリプト実行（chcpコマンドは不要）
python3 python/main/projection.py
```

### Step 5: 出力の確認

スクリプトが正常に実行されると、`outputs/` ディレクトリに以下のファイルが生成されます：

- 資産予測のグラフ（PNG形式）
- シミュレーション結果（CSV形式）
- 分析レポート（テキスト形式）

---

## OS別のトラブルシューティング

### Windows: 文字化けする

#### 原因
コマンドプロンプトのデフォルト文字コードがCP932（Shift-JIS）

#### 解決方法1: chcpコマンド
```bash
chcp 65001
python python/controllers/investment_analysis.py
```

#### 解決方法2: 環境変数
```bash
set PYTHONUTF8=1
python python/controllers/investment_analysis.py
```

#### 解決方法3: Git Bashを使用
Git Bashはデフォルトでutf-8に設定されています。

### MacOS: `chcp`コマンドが見つからない

#### 原因
`chcp 65001` はWindows専用コマンドです。

#### 解決方法
MacOSでは文字コード設定は不要です。`chcp`行を省略してください。

```bash
# ✅ MacOS
python3 python/main/projection.py

# ❌ MacOS（chcpは不要）
# chcp 65001  # <- この行は不要
python3 python/main/projection.py
```

### Windows/MacOS共通: パスが見つからない

#### 原因
サブディレクトリから実行している

#### 解決方法
必ず `aurum/` ディレクトリから実行してください。

```bash
# ✅ 正しい
cd aurum
python python/controllers/investment_analysis.py

# ❌ 間違い
cd aurum/python/main
python projection.py
```

### Python: モジュールが見つからない

#### 原因
必要なパッケージがインストールされていない

#### 解決方法
```bash
# Windows
pip install pandas numpy matplotlib

# MacOS
pip3 install pandas numpy matplotlib
```

---

## Claude Codeの設定（オプション）

このプロジェクトはClaude Codeで効率的に作業できるよう設計されています。

### Claude Code設定ファイル

- `CLAUDE.md` - プロジェクト設定
- `.claude/` - 詳細設定
  - `01_project_overview.md` - プロジェクト概要
  - `02_directory_structure.md` - ディレクトリ構造
  - `03_work_process.md` - 作業プロセス
  - `04_python_guide.md` - Python開発ガイド
  - `06a_three_agent_overview.md` - 3エージェント評価

### Claude Codeで開く

```bash
# プロジェクトを開く
claude .
```

---

## 次のステップ

セットアップが完了したら、以下を試してください：

1. **投資判断の実施**
   - `.claude/06a_three_agent_overview.md` を参照（評価システムの概要）
   - `.claude/06b_three_agent_detailed.md` を参照（詳細な実行手順）
   - `.claude/06c_weight_adjustment_rules.md` を参照（ウェイト調整ルール）
   - `.claude/09_baseline_evaluation.md` を参照（ベースライン評価の記録方法）
   - 3エージェント評価システムを使用

2. **資産予測シミュレーション**
   - `python/main/projection.py` を実行
   - 60歳時点の資産予測を確認

3. **教育費達成確率の計算**
   - `python/analysis/education_probability.py` を実行
   - モンテカルロシミュレーション

4. **月次レポートの作成**
   - `python/main/monthly_report.py` を実行
   - 家計収支の分析

---

## よくある質問

### Q1: Gitでバージョン管理したいが、個人情報が心配

**A**: `.gitignore` が既に設定されています。

以下のファイルは自動的に除外されます：
- `document/PERSONAL_DATA.md`
- `INVESTMENT_PROFILE.md`
- `sources/profile/asset_details.md`
- `sources/profile/investment_history.md`
- `sources/reference/`
- `outputs/`
- `python/config/personal.py`

### Q2: MacOSとWindowsで開発環境を共有したい

**A**: Pythonスクリプトは `os.path.join` を使用しているため、両OS で動作します。

注意点:
- Windowsの `chcp 65001` はMacOSでは不要
- Pythonコマンドは `python` (Windows) / `python3` (MacOS) を使い分け

### Q3: エディタは何を使えば良い？

**A**: 以下を推奨します：

- **Claude Code** - AI支援、プロジェクト設定済み
- **VS Code** - 汎用エディタ、拡張機能が豊富
- **PyCharm** - Python開発に特化

### Q4: Pythonの基本的な使い方がわからない

**A**: `.claude/04_python_guide.md` に詳しい説明があります。

主なコマンド:
```bash
# Windows
python python/controllers/investment_analysis.py

# MacOS
python3 python/main/projection.py
```

---

**最終更新**: 2025年11月9日
