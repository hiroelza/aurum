# aurum - 個人資産運用・人生設計プロジェクト

個人の資産運用、教育費計画、老後資金シミュレーションを統計的に分析し、データに基づいた投資判断を支援するプロジェクトです。

**プロジェクト名の由来**: aurum（アウルム）はラテン語で「金（Gold）」を意味し、古代から資産価値の象徴として扱われてきました。時間を経ても変わらない価値を表現しています。

## 主な特徴

- **3エージェント評価システム**: 投資判断を3つの視点（哲学・統計・税制）で評価
- **モンテカルロシミュレーション**: 60歳時点の資産予測（保守的・標準・楽観的シナリオ）
- **教育費達成確率分析**: 子供の教育費目標達成確率を計算
- **投資哲学の明文化**: 伊藤ハヤト氏の投資原則を採用
- **詳細な投資履歴管理**: 過去の判断を記録・評価

## 動作環境

### 開発・テスト環境
- **OS**: Windows 10/11（MINGW64環境）、MacOS
- **Python**: 3.8以上
  - Python 3.8-3.12: 完全サポート ✅
  - Python 3.13: 未対応（numpy/scipyとの互換性問題）❌
- **推奨エディタ**: Claude Code、VS Code

### 依存パッケージ
- numpy, pandas, scipy（データ分析）
- matplotlib（可視化）
- yfinance（市場データ取得）
- pytest（テスト）

## セットアップ手順

### 前提条件

- Python 3.8以上
- pip（Pythonパッケージマネージャー）
- Git（オプション、リポジトリをクローンする場合）

### 1. リポジトリのクローンまたはダウンロード

```bash
# Gitを使用する場合
git clone <repository-url>
cd aurum

# ZIPファイルをダウンロードした場合は解凍して移動
cd aurum
```

### 2. 依存パッケージのインストール

```bash
# Windows
pip install -r requirements.txt

# MacOS / Linux
pip3 install -r requirements.txt
```

### 3. 個人設定ファイルのコピー

**重要**: 以下のコマンドを実行して、テンプレートから個人設定ファイルを作成してください。

```bash
# 必須ファイル
cp python/config/personal.template.py python/config/personal.py
cp INVESTMENT_PROFILE.template.md INVESTMENT_PROFILE.md

# 推奨ファイル（詳細な管理をする場合）
cp sources/profile/templates/asset_details.template.md sources/profile/asset_details.md
cp sources/profile/templates/investment_history.template.md sources/profile/investment_history.md
cp document/PERSONAL_DATA.template.md document/PERSONAL_DATA.md
```

**Windows PowerShellの場合:**
```powershell
# 必須ファイル
Copy-Item python\config\personal.template.py python\config\personal.py
Copy-Item INVESTMENT_PROFILE.template.md INVESTMENT_PROFILE.md

# 推奨ファイル（詳細な管理をする場合）
Copy-Item sources\profile\templates\asset_details.template.md sources\profile\asset_details.md
Copy-Item sources\profile\templates\investment_history.template.md sources\profile\investment_history.md
Copy-Item document\PERSONAL_DATA.template.md document\PERSONAL_DATA.md
```

### 4. 個人情報の入力

**重要**: このプロジェクトでは、以下の5つのファイルすべてに情報を記録する必要があります。

#### 4-1. Python設定ファイル（必須）

`python/config/personal.py` を編集して、あなたの情報を入力してください：

**必須項目（プレースホルダーを置き換え）:**
- `[YOUR_AGE]` → あなたの年齢（例: 35）
- `[CURRENT_YEAR]` → 現在の年（例: 2025）
- `[RETIREMENT_AGE]` → 退職予定年齢（例: 65）
- `[YOUR_NISA]` → NISA資産額（万円、例: 500.0）
- `[YOUR_ANNUAL_INCOME]` → 年収（税引後、万円、例: 600.0）

その他の項目も同様に置き換えてください。

#### 4-2. 投資プロフィール（最重要）

`INVESTMENT_PROFILE.md` を編集して、投資方針と資産状況を記録してください：

**記録すべき情報:**
- 基本プロフィール（年齢、家族構成、年収）
- 資産状況サマリー（NISA、iDeCo、現金、総資産）
- 投資方針（リスク許容度、投資期間）
- 過去の投資判断の記録

**なぜ必要？**
- **Claude Codeがこのファイルを参照して投資アドバイスを提供します**
- 投資判断の履歴を記録することで、過去の判断を評価できます
- プロジェクトの設計上、最も重要なファイルです

#### 4-3. 資産詳細（推奨）

`sources/profile/asset_details.md` を編集して、保有銘柄の詳細を記録してください：

**記録すべき情報:**
- NISA保有銘柄の詳細（銘柄名、取得単価、含み損益）
- iDeCoの詳細
- 自社株の詳細

**なぜ必要？**
- 具体的な銘柄情報を記録することで、リバランスや売却判断に役立ちます
- Claude Codeがポートフォリオ分析を実施する際に参照します

#### 4-4. 投資履歴（推奨）

`sources/profile/investment_history.md` を編集して、過去の投資判断を記録してください：

**記録すべき情報:**
- 日付、判断内容、理由、結果
- 3エージェント評価（哲学・統計・税制の点数）

**なぜ必要？**
- 過去の判断を振り返り、学習することができます
- 感情的な判断を防ぐために重要です

#### 4-5. 個人データ（オプション）

`document/PERSONAL_DATA.md` を編集して、基本情報のバックアップを作成してください：

**記録すべき情報:**
- 基本プロフィール、収入情報、資産概要

**なぜ必要？**
- INVESTMENT_PROFILE.mdのバックアップとして機能します

---

**最低限のセットアップ**: `python/config/personal.py` と `INVESTMENT_PROFILE.md` の2つを編集すれば、プロジェクトは動作します。

**推奨セットアップ**: すべてのファイルを編集することで、Claude Codeによる高度な分析が可能になります。

### 5. テスト実行（動作確認）

```bash
# 依存パッケージのインストール（pytest含む）
pip install -r requirements.txt

# テストを実行してセットアップが正しいか確認
pytest

# 期待される結果: "11 passed, 1 skipped" または "11 passed" (personal.py設定後)
```

### 6. Pythonスクリプトの実行

```bash
# Windows
python python/controllers/investment_analysis.py

# MacOS / Linux
python3 python/controllers/investment_analysis.py
```

### よくある問題と解決方法

#### `personal.py not found` という警告が出る

**原因**: Step 3でファイルをコピーしていない

**解決方法**:
```bash
cp python/config/personal.template.py python/config/personal.py
```

#### `ModuleNotFoundError: No module named 'numpy'`

**原因**: 依存パッケージがインストールされていない

**解決方法**:
```bash
pip install -r requirements.txt
```

#### パスが見つからないエラー

**原因**: aurumディレクトリ以外から実行している

**解決方法**: 必ずaurumディレクトリから実行してください
```bash
cd aurum
python python/controllers/investment_analysis.py
```

## ディレクトリ構成

詳細は `.claude/02_directory_structure.md` を参照してください。

```
aurum/
├── .claude/              # Claude Code設定
│   ├── agents/           # エージェント定義
│   ├── glossaries/       # 用語集
│   ├── 00_work_checklist.md
│   ├── 01_project_overview.md
│   ├── 02_directory_structure.md
│   └── ...
├── document/             # ドキュメント
│   ├── PERSONAL_DATA.template.md
│   ├── examples.md
│   ├── setup_guide.md
│   └── tutorial.md
├── outputs/              # 生成データ（自動生成、.gitignore対象）
│   ├── python/           # Python実行結果
│   │   ├── cache/
│   │   ├── screening/
│   │   └── temp/
│   └── reports/          # 分析レポート
│       ├── completed/
│       └── working/
├── python/               # Pythonコード
│   ├── config/           # 設定管理
│   ├── controllers/      # エントリーポイント
│   ├── main/             # メインスクリプト
│   ├── models/           # データロジック
│   └── services/         # 共通サービス
├── sources/              # ソースデータ（手動管理）
│   ├── profile/          # 投資プロフィール（機密、.gitignore対象）
│   │   ├── historical/
│   │   └── templates/
│   └── reference/        # 参考資料（.gitignore対象）
│       ├── csv/
│       ├── image/
│       ├── market/
│       └── pdf/
├── tests/                # テストコード
│   ├── fixtures/
│   ├── integration/
│   └── unit/
├── .gitignore            # Git除外設定
├── CHANGELOG.md          # 変更履歴
├── CLAUDE.md             # プロジェクト設定
├── CODE_OF_CONDUCT.md    # 行動規範
├── CONTRIBUTING.md       # 貢献ガイドライン
├── INVESTMENT_PROFILE.template.md # 投資プロフィールテンプレート
├── LICENSE               # ライセンス
├── README.md             # このファイル
├── pytest.ini            # テスト設定
└── requirements.txt      # 依存パッケージ
```

## 投資哲学

このプロジェクトは**伊藤ハヤト氏の投資哲学**（低コスト・インデックス投資、最大限の分散、市場タイミングを取らない）を基本とします。

詳細は [`.claude/01_project_overview.md`](.claude/01_project_overview.md) を参照してください。

## 3エージェント評価システム

重要な投資判断は、哲学・統計・税制の3つの視点で評価します。

詳細は [`.claude/06a_three_agent_overview.md`](.claude/06a_three_agent_overview.md) を参照してください。

## トラブルシューティング

### Python実行時に文字化けする（Windows）

```bash
# UTF-8モードで実行
chcp 65001
python python/controllers/investment_analysis.py

# または環境変数を設定
set PYTHONUTF8=1
python python/controllers/investment_analysis.py
```

### パスが見つからないエラー

Pythonスクリプトは必ず `aurum/` ディレクトリから実行してください。

```bash
# ✅ 正しい
cd aurum
python python/controllers/investment_analysis.py

# ❌ 間違い
cd aurum/python/controllers
python investment_analysis.py
```

## AI開発ツールでの使用

このプロジェクトは、AI開発ツールと組み合わせて使うことで、より効率的な投資判断が可能になります。

### Claude Code（推奨）

**フルサポート** ✅

- `.claude/` ディレクトリに26個の詳細な設定ファイルを含む
- `CLAUDE.md` を自動的に読み込み、プロジェクトのコンテキストを理解
- 3エージェント評価システム（hayato/researcher/japanese）が利用可能
- 投資哲学、作業プロセス、用語集を自動参照

**使い方**:
```bash
# Claude Code で aurum ディレクトリを開くだけで自動認識
claude .
```

### Cursor

**部分サポート** ⚠️

- `.claude/` ディレクトリの内容は手動で参照可能
- `CLAUDE.md` を手動でAIに提供する必要がある
- 3エージェント評価は手動で実施

**使い方**:
1. Cursorで aurum ディレクトリを開く
2. `.claude/01_project_overview.md` などを手動で読み込ませる
3. `INVESTMENT_PROFILE.md` を参照しながら質問

### GitHub Copilot / Codeium

**コード補完のみ** ⚙️

- Pythonコードの補完・リファクタリングは動作
- `.claude/` ディレクトリの設定は無視される
- 投資哲学の理解は不可
- 汎用的なコーディング支援ツールとして利用可能

### 汎用的な使い方

AI開発ツールに関係なく、以下のファイルを読み込ませることで投資アドバイスを受けられます：

- `INVESTMENT_PROFILE.md` - あなたの投資プロフィール
- `.claude/01_project_overview.md` - プロジェクト概要と投資哲学
- `.claude/06a_three_agent_overview.md` - 3エージェント評価システムの説明

## ⚠️ セキュリティと機密情報の管理

**重要**: このプロジェクトには個人の金融情報が含まれます。GitHubやブログで公開する際は、以下の点に**必ず**注意してください。

### .gitignoreの重要性

**除外される機密ファイル:**
- `INVESTMENT_PROFILE.md` - 投資プロフィール（ルート）
- `sources/profile/asset_details.md` - 資産詳細
- `sources/profile/investment_history.md` - 投資履歴
- `sources/reference/` - 参考資料（CSV/PDF/画像）
- `outputs/python/` - Python実行結果（**スクリーンショット、グラフ含む**）
- `outputs/reports/` - レポート（**実データが含まれる**）
- `document/PERSONAL_DATA.md` - 個人情報
- `python/config/personal.py` - Python個人設定（**年齢、資産額、収入など**）

### GitHub/GitLabで公開する前の最終チェックリスト

```bash
# 1. .gitignoreが正しく設定されているか確認
cat .gitignore

# 2. 追跡されるファイルを確認（機密ファイルが含まれていないこと）
git status

# 3. すべての変更内容を確認（diffで意図しないファイルがないか）
git diff --cached

# 4. outputs/フォルダが除外されているか確認
ls -la outputs/ 2>/dev/null && echo "WARNING: outputs/フォルダが存在します。git statusで確認してください" || echo "OK: outputs/未作成"

# 5. 問題がなければコミット
git add .
git commit -m "Initial commit"
```

### ブログやSNSで共有する際の注意事項

**スクリーンショットやグラフを投稿する際は、以下の情報を必ず削除してください:**

1. **数値データ**:
   - 資産額、年収、具体的な金額
   - 年齢、家族構成
   - 具体的な銘柄名（特定される可能性がある場合）

2. **ファイルパス**:
   - ターミナルのスクリーンショットにユーザー名が含まれる
   - エラーメッセージに絶対パスが含まれる

3. **outputs/フォルダ内のファイル**:
   - グラフ画像（`outputs/python/*.png`）
   - レポート（`outputs/reports/*.md`）
   - これらには実データが含まれています

**推奨**: スクリーンショットを投稿する前に、モザイク処理や架空データへの置き換えを行ってください。

### Pythonエラーメッセージにも個人情報が含まれる可能性

```python
# 例: エラーメッセージにファイルパスが含まれる
FileNotFoundError: [Errno 2] No such file or directory: 'C:/Users/YourName/aurum/python/config/personal.py'
```

**対策**: エラーメッセージを共有する際は、ユーザー名やパスを `***` で置き換えてください。

### outputs/フォルダの取り扱い

**`outputs/` フォルダは .gitignore で除外されていますが、以下に注意してください:**

- Python実行時に自動生成されるファイル（グラフ、CSV、一時ファイル）には実データが含まれます
- これらのファイルを誤って他人と共有しないでください
- ブログ投稿用に加工する場合は、別フォルダにコピーして編集してください

### 二重チェックの推奨

公開前に、以下を確認してください：

```bash
# Git履歴に機密ファイルが含まれていないか確認
git log --all --full-history -- python/config/personal.py
git log --all --full-history -- outputs/

# 何も表示されなければOK
# もし履歴に含まれている場合は、git filter-branchで削除が必要
```

### 万が一、機密情報をコミットしてしまった場合

**すぐに以下を実行してください:**

```bash
# 1. 該当ファイルを削除
git rm --cached python/config/personal.py

# 2. コミット
git commit -m "Remove sensitive file"

# 3. すでにpushしている場合は、リポジトリを削除して再作成
# GitHubの場合: Settings > Danger Zone > Delete this repository
```

**注意**: `git filter-branch` や `BFG Repo-Cleaner` で履歴から削除する方法もありますが、複雑なため、リポジトリを削除して再作成する方が安全です。

## ライセンス

MIT License

## 免責事項（Disclaimer）

**重要**: このツールを使用する前に、以下の免責事項を必ずお読みください。

### 1. 投資助言ではありません

このツール（aurum）は、個人の学習・研究目的のために作成された統計分析・シミュレーションツールです。

- **投資助言ではありません**: このツールは、日本の金融商品取引法に基づく「投資助言業」ではなく、個別具体的な投資推奨を行うものではありません。
- **教育目的**: 投資に関する統計的な分析手法を学ぶための教育目的のツールです。
- **金融商品取引業者ではありません**: 作成者は金融商品取引業の登録を受けていません。

### 2. 自己責任の原則

**すべての投資判断は利用者の自己責任で行ってください。**

- **最終判断は利用者**: このツールが提供する情報・分析結果は参考情報であり、利用者が独自に判断する必要があります。
- **損失の責任**: 投資により損失が発生した場合でも、作成者および貢献者は一切の責任を負いません。
- **独自の検証**: 提供されるデータ・計算結果を利用者自身で検証してください。

### 3. 統計・確率モデルの限界

このツールが使用する統計モデル・シミュレーションには以下の限界があります：

- **過去データの限界**: 過去の実績は将来の成果を保証するものではありません。
- **確率的予測**: モンテカルロシミュレーション等の結果は「確率的予測」であり、「確実な予測」ではありません。
- **市場変動**: 実際の市場は予測モデルと異なる動きをする可能性があります。
- **ボラティリティの変動**: 過去のボラティリティが将来も維持される保証はありません。

### 4. データの正確性・バグ

- **外部データソース**: yfinance等の外部APIから取得するデータの正確性を保証しません。
- **ソフトウェアのバグ**: このツールには既知または未知のバグが存在する可能性があります。
- **計算結果の検証**: すべての計算結果は利用者自身で検証してください。

### 5. 法的責任の否定

**作成者および貢献者は、以下を含むいかなる損害に対しても一切の責任を負いません：**

- 直接損害、間接損害、特別損害、付随的損害、結果的損害
- 利益の喪失、データの喪失、事業機会の喪失
- このツールの使用または使用不能から生じるすべての損害

**このツールは「現状のまま（AS IS）」で提供されます。** MIT Licenseの条項に従い、明示的または黙示的な保証は一切ありません。詳細は `LICENSE` ファイルを参照してください。

### 6. 専門家への相談を推奨

重要な投資判断を行う前に、以下の専門家に相談することを強く推奨します：

- **金融アドバイザー**: 登録された金融商品取引業者（投資助言業）
- **税理士**: 税務上の判断（NISA、iDeCo、確定申告等）
- **弁護士**: 法的判断が必要な場合

このツールは専門家の助言の代替とはなりません。

### 7. 日本の法律との関係

- **金融商品取引法**: このツールは日本の金融商品取引法に基づく「投資助言業」の登録を必要としない個人利用のツールです。
- **税法**: 税務上のアドバイスは提供しません。税法の解釈は税理士に相談してください。
- **居住地の法律**: 利用者の居住地の法律・規制を確認し、遵守してください。

### 8. 利用者の責任

このツールを利用することで、利用者は以下に同意したものとみなされます：

- 上記の免責事項をすべて理解し、同意した
- すべての投資判断を自己責任で行う
- 作成者および貢献者に対していかなる請求も行わない
- データ・計算結果を独自に検証する

### 9. 投資のリスク

**投資には以下のリスクが伴います：**

- **元本割れリスク**: 投資元本を下回る可能性があります。
- **市場リスク**: 株式市場の変動により資産価値が変動します。
- **為替リスク**: 外国資産への投資には為替変動リスクがあります。
- **流動性リスク**: 市場環境により売却が困難になる可能性があります。

**重要**: 投資は余裕資金で行い、生活費や教育費など必要不可欠な資金を投資に回さないでください。

---

**最終更新**: 2025年11月11日

## 参考資料

- [伊藤ハヤト氏のブログ](https://hayatoito.github.io/2020/capitalism/)
- [INVESTMENT_PROFILE.md](INVESTMENT_PROFILE.md) - 投資プロフィール
- [.claude/01_project_overview.md](.claude/01_project_overview.md) - プロジェクト概要
- [.claude/02_directory_structure.md](.claude/02_directory_structure.md) - 詳細なディレクトリ構造

---

**最終更新**: 2025年11月11日（公開準備完了: プロジェクト名統一、テスト修正、セットアップ手順明確化）
