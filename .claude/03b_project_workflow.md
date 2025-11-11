# 作業プロセス - プロジェクト管理のワークフロー

このファイルは、temp_n命名規則とプロジェクト管理のワークフローを定義します。

---

## 📚 関連ドキュメント

- **[03_work_process.md](03_work_process.md)** - 基本プロセスと作業開始前の原則
- **[03a_work_levels.md](03a_work_levels.md)** - プロセス省略の例外ルール（Level 1-4）
- **[03c_agent_discussion.md](03c_agent_discussion.md)** - サブエージェント議論フレームワーク

---

## プロジェクト管理のワークフロー ⭐

### temp_n命名規則と自動昇格

**目的:** 作業開始時に命名で悩まない、結論が出てから適切な名前を付ける

---

### Phase 1: 軽量スタート

新規作業開始時は`temp_n.md`形式で1ファイルから開始：

```bash
outputs/reports/working/
└── temp_1.md          ← シンプルな1ファイルで開始
```

**特徴:**
- 連番（temp_1, temp_2, ...）で即座に作業開始
- 命名に悩まない
- メモレベルの簡易作業に最適

---

### Phase 2: 自動ディレクトリ化

2つ目のファイル（CSV、PNG等）を追加する必要が出た時点で、**AIが自動的に**ディレクトリへ変換：

```bash
# AIが検知して自動変換
outputs/reports/working/
└── temp_1/            ← ディレクトリに昇格
    ├── 要件定義.md    ← 元のtemp_1.mdをリネーム
    ├── data.csv       ← 新規追加
    └── graph.png      ← 新規追加
```

**変換タイミング:**
- CSVファイルを追加する時
- 画像ファイルを追加する時
- 2つ目のMarkdownファイルを追加する時

**変換プロセス:**
1. AIが「2ファイル目が必要」と判断
2. `temp_n.md` → `temp_n/` ディレクトリ作成
3. 元のファイルを適切な名前（要件定義.md等）にリネーム
4. 新規ファイルを追加

---

### Phase 3: 完了とリネーム

作業完了時に、AIが内容を分析して**3つの命名候補**を提案：

```bash
# AIからの提案例
候補1: 支出改善アクション_20251103
候補2: 家計見直しプラン_20251103
候補3: 月次支出最適化_20251103
```

ユーザーが選択（または`temp_n`のまま保持）：

```bash
# outputs/reports/completed/へ移動+リネーム
outputs/reports/completed/202511/
└── 20251103_支出改善アクション/  ← 選択した名前
    ├── アクションプラン.md
    ├── 支出データ.csv
    └── グラフ.png
```

---

## 命名ルール

### working/ (作業中)
- 単一ファイル: `temp_n.md`
- ディレクトリ: `temp_n/`

### outputs/reports/completed/ (完了)
- 必ず日付プレフィックス: `yyyymmdd_テーマ/`
- 例: `20251103_支出改善アクション/`

### outputs/reports/working/ (作業中、月別管理)
- 月ディレクトリ必須: `202511/yyyymmdd_テーマ/`
- 例: `202511/20251109_ディレクトリ再構成/`

---

## 実装方法

### 手動運用（現状）
```bash
# 1. 新規作成
touch outputs/reports/working/temp_1.md

# 2. ディレクトリ化が必要になったら
mkdir outputs/reports/working/temp_1
mv outputs/reports/working/temp_1.md outputs/reports/working/temp_1/要件定義.md

# 3. 完了時（月ディレクトリを確認）
mkdir -p outputs/reports/completed/202511
mv outputs/reports/working/temp_1 outputs/reports/completed/202511/20251103_テーマ
```

### AI支援（推奨）
- AIに「temp_1にCSVを追加したい」と伝える
- AIが自動的にディレクトリ化を判断・実行
- 完了時に命名候補を提案

---

## 冪等性の確保

**原則:** 作業の各段階を必ずファイル出力する

**理由:**
- 作業を再現可能にする
- 中断・再開が容易になる
- 過去の判断根拠を追跡できる
- 複数セッションにまたがる作業を管理しやすい

---

**最終更新**: 2025年11月9日（Phase 10: 03_work_process.mdから分割）
