# 貢献ガイドライン

aurum プロジェクトへの貢献を検討していただき、ありがとうございます。

このプロジェクトは個人の投資管理ツールとして開発されていますが、改善提案やバグ報告を歓迎します。

## 貢献の種類

以下のような貢献を歓迎します：

### 1. テンプレート改善
- `INVESTMENT_PROFILE.template.md` 等のテンプレートファイルの改善
- プレースホルダーの明確化
- 記入例の追加

### 2. ドキュメント改善
- README.md、setup_guide.md、tutorial.md の誤字修正
- 説明の明確化
- 新しい使用例の追加

### 3. バグ修正
- Python コードのバグ修正
- 計算ロジックの改善
- エラーハンドリングの追加

### 4. 新機能追加
- 新しい分析機能
- スクリーニング手法の追加
- データ可視化の改善

## 貢献の流れ

### 1. Issue を作成する

まず、GitHub Issues で以下を確認してください：

- 同じ問題や提案が既に報告されていないか
- 既存の Issue にコメントして議論に参加できないか

新しい Issue を作成する場合：

- **バグ報告**: 再現手順、期待される動作、実際の動作を記載
- **機能リクエスト**: 背景、具体的な提案、期待される効果を記載

### 2. Fork してブランチを作成する

```bash
# リポジトリを Fork
# GitHub上で "Fork" ボタンをクリック

# ローカルにクローン
git clone https://github.com/YOUR_USERNAME/aurum.git
cd aurum

# 新しいブランチを作成
git checkout -b feature/your-feature-name
```

### 3. 変更を加える

#### コーディング規約

- **Python スタイル**: PEP 8 に準拠してください
- **日本語コメント**: 可（複雑なロジックには推奨）
- **実行起点**: 必ず `aurum/` ディレクトリから実行してください

#### テストの実行

```bash
# 依存パッケージをインストール
pip install -r requirements.txt

# テストを実行
pytest

# 特定のテストのみ実行
pytest tests/unit/test_config_paths.py
```

### 4. コミットする

```bash
# 変更をステージング
git add .

# コミット（わかりやすいメッセージで）
git commit -m "Fix: 投資額計算のバグを修正"
```

コミットメッセージの例：
- `Fix: [バグの内容]`
- `Add: [新機能の内容]`
- `Update: [改善内容]`
- `Docs: [ドキュメント変更内容]`

### 5. Pull Request を作成する

```bash
# 自分の Fork に push
git push origin feature/your-feature-name
```

GitHub上で Pull Request を作成してください。

**Pull Request には以下を記載してください：**
- 変更内容の概要
- 関連する Issue 番号（例: `Fixes #123`）
- テスト結果（pytest の実行結果）
- スクリーンショット（UI変更の場合）

## 機密情報の取り扱い

**重要**: このプロジェクトは個人の金融情報を扱います。

### 絶対にコミットしてはいけないファイル

- `INVESTMENT_PROFILE.md`
- `sources/profile/asset_details.md`
- `sources/profile/investment_history.md`
- `python/config/personal.py`
- `document/PERSONAL_DATA.md`
- `sources/reference/` 配下のすべてのファイル
- `outputs/` 配下のすべてのファイル

これらは `.gitignore` で除外されていますが、念のため確認してください：

```bash
# コミット前に必ず確認
git status
```

### テンプレートファイルのみ変更してください

個人情報を含む可能性のあるファイルは、必ず `.template` ファイルを編集してください：

- ✅ `INVESTMENT_PROFILE.template.md` を編集
- ❌ `INVESTMENT_PROFILE.md` を編集

## 開発環境

### 推奨環境

- Python 3.8 以上（3.13 は未対応）
- Git 2.x 以上
- Claude Code（`.claude/` ディレクトリを活用する場合）

### 依存パッケージ

```bash
pip install -r requirements.txt
```

主要なライブラリ：
- numpy: 数値計算
- pandas: データ分析
- scipy: 統計計算
- matplotlib: データ可視化
- yfinance: 株価データ取得
- pytest: テスト

## レビュープロセス

Pull Request は以下の観点でレビューされます：

1. **機能性**: 意図した通りに動作するか
2. **コード品質**: PEP 8 準拠、適切なコメント
3. **テスト**: 必要に応じてテストが追加されているか
4. **ドキュメント**: README や他のドキュメントの更新が必要か
5. **セキュリティ**: 機密情報が含まれていないか

## 質問や相談

- **バグ報告**: GitHub Issues
- **機能提案**: GitHub Issues
- **セキュリティ脆弱性**: GitHub Issues（プライベート脆弱性報告機能を推奨）

## ライセンス

このプロジェクトに貢献する場合、あなたのコードは MIT License の下でライセンスされることに同意したものとみなされます。

---

**注意**: このプロジェクトは個人の投資管理ツールとして開発されています。大規模な機能追加やアーキテクチャ変更を検討する場合は、事前に Issue で議論してください。
