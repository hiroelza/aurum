# CLAUDE.md - aurum プロジェクト設定

## プロジェクト概要

**aurum（アウルム）** は、個人の資産運用・人生設計を統計的に分析し、データに基づいた投資判断を支援するプロジェクトです。

**プロジェクト名の由来**: aurum はラテン語で「金（Gold）」を意味し、時間を経ても変わらない価値を表現しています。

## 重要: Claude Code 初回セットアップ

このプロジェクトには詳細な設定ファイルが `.claude/` ディレクトリに格納されています。Claude Codeで作業を開始する前に、**必ず以下のファイルを読んでください**：

### 必読ファイル（優先順）

1. **`.claude/01_project_overview.md`** - プロジェクト全体像・投資哲学
2. **`.claude/02_directory_structure.md`** - ディレクトリ構造の詳細
3. **`.claude/03_work_process.md`** - 作業プロセス
4. **`.claude/00_work_checklist.md`** - 作業チェックリスト

### 追加の設定ファイル

- **`.claude/04_python_guide.md`** - Python開発ガイド
- **`.claude/06a_three_agent_overview.md`** - 3エージェント評価システム
- **`.claude/07_analysis_guidelines.md`** - 分析ガイドライン

**セットアップ手順**: [README.md](README.md) または [document/setup_guide.md](document/setup_guide.md) を参照してください。

## プロジェクトルール

### 1. 機密情報管理（重要）

このプロジェクトには個人の金融情報が含まれます。以下のファイルは `.gitignore` で除外されています：

- `INVESTMENT_PROFILE.md` - 投資プロフィール
- `sources/profile/asset_details.md` - 資産詳細
- `sources/profile/investment_history.md` - 投資履歴
- `sources/reference/` 配下のすべてのファイル（CSV、PDF、画像）
- `outputs/` 配下のすべてのファイル（**グラフ、レポート、実データ含む**）
- `document/PERSONAL_DATA.md` - 個人データ
- `python/config/personal.py` - 個人設定（**年齢、資産額、収入など**）

#### ⚠️ Claude Codeを使用する際の注意

Claude Codeで作業する際、以下の点に注意してください：

1. **ファイル内容の参照**: Claude Codeは質問に答えるため、プロジェクト内のファイルを読む場合があります。`personal.py` や `INVESTMENT_PROFILE.md` には実データが含まれるため、外部に共有しないでください。

2. **Git操作の確認**: Claude Codeがgitコマンドを実行する際、**必ず `git status` の結果を確認**してください。機密ファイルがステージングされていないことを確認してからコミットしてください。

3. **スクリーンショット共有時の注意**: ブログやSNSでClaude Codeとの会話やコード実行結果を共有する際、以下を削除してください：
   - 具体的な金額、年齢、資産額
   - ファイルパス内のユーザー名
   - `outputs/` フォルダ内のグラフや数値データ

#### 実行起点ルール（重要）

**必ず `aurum/` ディレクトリから実行してください。**

```bash
# ✅ 正しい
cd aurum
python python/controllers/investment_analysis.py

# ❌ 間違い
cd aurum/python/controllers
python investment_analysis.py
```

### 2. 投資哲学の原則

このプロジェクトは**伊藤ハヤト氏の投資哲学**を基本とします：

- 低コスト・インデックス投資
- 最大限の分散（全世界株式）
- 市場タイミングを取らない
- 長期保有

詳細は `.claude/01_project_overview.md` を参照してください。

### 3. 3エージェント評価システム

重要な投資判断は、以下の3つの視点で評価します：

1. **哲学エージェント**: 投資哲学との整合性
2. **統計エージェント**: 過去データに基づく統計的妥当性
3. **税制エージェント**: 税制上の最適性

詳細は `.claude/06a_three_agent_overview.md` を参照してください。

## 参考資料

- [README.md](README.md) - セットアップ、ディレクトリ構造、使い方、外部リンク
- [document/setup_guide.md](document/setup_guide.md) - 詳細セットアップ
- `.claude/` ディレクトリ配下の設定ファイル

## ライセンス

MIT License

## 免責事項

**重要**: このツールは投資助言ではありません。すべての投資判断は自己責任で行ってください。

詳細な免責事項は [README.md](README.md#免責事項disclaimer) を参照してください。

---

**最終更新**: 2025年11月11日
