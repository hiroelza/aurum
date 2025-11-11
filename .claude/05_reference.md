# リファレンス

このファイルは、aurumプロジェクトでのテスト手順、トラブルシューティング、今後の拡張予定を記載します。

## テスト手順

### Pythonスクリプトの動作確認

#### 基本動作テスト

```bash
# 投資分析が正常に実行されるか確認
cd .
python python/main/investment_analysis.py

# 終了コードを確認（0が返ればOK）
echo $?
```

#### 出力ファイルの確認

```bash
# 画像ファイルが生成されているか
ls -l image/*.png
ls -l image/*.jpg

# CSVファイルが生成されているか
ls -l data/csv/*.csv

# 最新の出力を確認
ls -lt image/ | head -3
ls -lt data/csv/ | head -3
```

#### パス設定の確認

```bash
# config.pyが正しく読み込めるか
python -c "import sys; sys.path.append('python'); from config import IMAGE_DIR, CSV_DIR; print('IMAGE_DIR:', IMAGE_DIR); print('CSV_DIR:', CSV_DIR)"

# 各ディレクトリが存在するか
python -c "import os; from python.config import IMAGE_DIR, CSV_DIR; print('IMAGE_DIR exists:', os.path.exists(IMAGE_DIR)); print('CSV_DIR exists:', os.path.exists(CSV_DIR))"
```

### 新規スクリプトのテストチェックリスト

新しいPythonスクリプトを作成したら、以下を確認してください：

- [ ] `aurum/` ディレクトリから実行できるか
- [ ] `config.py` を使ってパス取得しているか
- [ ] 画像は `IMAGE_DIR` に保存されるか
- [ ] CSVは `CSV_DIR` に保存されるか
- [ ] 日本語が正しく表示されるか（Matplotlib）
- [ ] エラーハンドリングが適切か
- [ ] 実行後に不要なファイルが残らないか

#### テストコマンド例

```bash
# 1. ディレクトリ確認
pwd  # aurum/ にいることを確認

# 2. スクリプト実行
python python/[category]/your_script.py

# 3. 出力確認
ls -l image/  # 新しい画像が生成されたか
ls -l data/csv/  # 新しいCSVが生成されたか

# 4. 内容確認
head -20 data/csv/your_output.csv  # CSVの先頭20行を確認
```

### 統合テスト（月次レビュー時）

```bash
# 1. 主要スクリプトを順次実行
python python/main/investment_analysis.py
python python/main/company_stock_analysis.py

# 2. 出力の一貫性確認
ls -l output/image/
ls -l output/csv/
ls -l outputs/reports/completed/

# 3. INVESTMENT_PROFILE.mdの更新確認
git diff INVESTMENT_PROFILE.md
```

---

## トラブルシューティング

### Matplotlibの日本語表示エラー

**症状:**
グラフの日本語ラベルが文字化けする

**解決方法:**
```python
# フォント設定を確認
plt.rcParams['font.sans-serif'] = ['MS Gothic', 'Yu Gothic', 'Hiragino Sans']
plt.rcParams['axes.unicode_minus'] = False
```

---

### モンテカルロシミュレーションが遅い

**症状:**
`investment_analysis.py`の実行に時間がかかる

**解決方法:**
- `simulations=10000`を`simulations=1000`に減らす（精度は若干低下）
- より高速なマシンで実行

**該当箇所:**
```python
# python/main/investment_analysis.py内
success_rate, achievement_distribution = monte_carlo_education_fund_simulation(
    total_investment_60,
    education_fund_needed=2400,
    years=19,
    simulations=10000  # ← この値を1000に変更
)
```

---

### パス関連エラー

**症状:**
`FileNotFoundError`や画像・CSVが保存されない

**原因:**
`aurum/`ディレクトリ以外から実行している

**解決方法:**
```bash
# 必ずaurum/ディレクトリから実行
cd .
python python/main/investment_analysis.py
```

---

### config.pyがimportできない

**症状:**
`ImportError: No module named 'config'`

**原因:**
sys.pathにpython/ディレクトリが追加されていない

**解決方法:**
```python
import sys
import os

# スクリプトの先頭に追加
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import IMAGE_DIR, CSV_DIR
```

---

### Windows環境でのEditツール動作（Windows Defender除外設定推奨）

**背景:**
WindowsでClaude Codeを使用する場合、Editツールが「File has been unexpectedly modified」エラーを出すことがあります。

**原因:**
- Windows Defenderがファイルをスキャン
- ファイルのタイムスタンプが変更される
- Editツールの変更検出が誤検出

**解決方法（推奨）:**
Windows Defenderの除外設定を行う：

1. 設定 → 更新とセキュリティ → Windows セキュリティ
2. ウイルスと脅威の防止 → 設定の管理
3. 除外 → 除外の追加 → フォルダー
4. . を追加

**効果:**
- エラー発生率が大幅に減少（85%以上の成功率）
- ファイル操作が高速化

**注意:**
- Claudeが自動的にエラーをハンドリングするため、ユーザー側の対応は不要
- エラーが出てもBashコマンドで自動的にリトライされます
- 除外設定は任意ですが、推奨されます

**技術的な補足:**
- Edit直後（1秒以内）の連続Editは失敗する可能性あり
- 2秒待機すれば解決
- これはWindowsファイルシステムの仕様
- Claudeが自動的に対処するため、意識する必要はありません

**検証日:** 2025年11月5日

---
## 今後の拡張予定

- [ ] 自動レポート生成（PDF出力）
- [ ] 資産推移のグラフ可視化
- [ ] 税金計算機能の追加
- [ ] 月次レポート自動生成
- [ ] 配当収入シミュレーション

---

## 主要ファイルの説明

### INVESTMENT_PROFILE.md
🔴 **CRITICAL** - 人生設計の基盤ファイル

**内容:**
- 個人・家族の基本情報
- 資産状況の詳細（NISA、iDeCo、自社株、現金）
- 投資方針と哲学（伊藤ハヤト氏の投資哲学）
- 投資判断履歴と3エージェント評価
- 教育費・老後資金の計画

**更新タイミング:**
- 投資判断・資産状況変更時に必ず更新
- 3エージェント評価実施時に記録追加
- 月次資産状況確認時

---

### 家計の状況_妻向け.md
家族共有用資料

**内容:**
- 家計状況の可視化
- 家事分担の記録
- 外部サービス利用の検討

---

**最終更新**: 2025年11月9日（Windows Defender除外設定、Editツール動作確認）
