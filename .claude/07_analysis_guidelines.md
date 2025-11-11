# データ分析ガイドライン

このファイルは、aurumプロジェクトでのデータ分析・投資判断の標準プロセスを定義します。

**目的:** データに基づく客観的な投資判断を実現する

**参考:** GMO「Claude Codeを使った投資戦略自動生成」（2025年11月6日分析）

---

## 1. 探索的データ分析（EDA）プロセス

### 目的
データの特性を理解し、異常値・トレンド・相関を発見する

### 標準プロセス

#### Step 1: データ取得と前処理
```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# データ読み込み
df = pd.read_csv('data.csv')

# 基本情報の確認
print(df.info())
print(df.describe())

# 欠損値の確認
print(df.isnull().sum())
```

#### Step 2: 基本統計量の算出
```python
# リターンの計算
df['return'] = df['price'].pct_change()

# 基本統計量
print(f"平均リターン: {df['return'].mean():.2%}")
print(f"標準偏差: {df['return'].std():.2%}")
print(f"最小値: {df['return'].min():.2%}")
print(f"最大値: {df['return'].max():.2%}")
```

#### Step 3: 可視化
```python
# ヒストグラム（リターン分布）
plt.figure(figsize=(10, 6))
plt.hist(df['return'].dropna(), bins=50, alpha=0.7, edgecolor='black')
plt.xlabel('Return')
plt.ylabel('Frequency')
plt.title('Return Distribution')
plt.axvline(df['return'].mean(), color='r', linestyle='--', label='Mean')
plt.legend()
plt.show()

# 時系列プロット
plt.figure(figsize=(12, 6))
plt.plot(df['date'], df['price'])
plt.xlabel('Date')
plt.ylabel('Price')
plt.title('Price Time Series')
plt.grid(True)
plt.show()
```

#### Step 4: 異常値検出
```python
# Z-scoreによる異常値検出
from scipy import stats
z_scores = np.abs(stats.zscore(df['return'].dropna()))
outliers = df[z_scores > 3]  # 3σ以上を異常値とする
print(f"異常値の数: {len(outliers)}")
```

#### Step 5: 相関分析
```python
# 相関行列
corr_matrix = df[['asset1', 'asset2', 'asset3']].corr()
print(corr_matrix)

# ヒートマップ
import seaborn as sns
plt.figure(figsize=(8, 6))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1)
plt.title('Correlation Matrix')
plt.show()
```

---

## 2. 定量的評価指標

### 2.1. シャープレシオ（Sharpe Ratio）

**定義:** リスク調整後リターン

**計算式:**
```
シャープレシオ = (平均リターン - 無リスク金利) / リターンの標準偏差
```

**Python実装:**
```python
def sharpe_ratio(returns, risk_free_rate=0.0):
    """
    シャープレシオを計算

    Parameters:
    - returns: リターンのSeries
    - risk_free_rate: 無リスク金利（年率）

    Returns:
    - Sharpe Ratio（年率換算）
    """
    excess_returns = returns - risk_free_rate / 252  # 日次換算
    return np.sqrt(252) * excess_returns.mean() / excess_returns.std()

# 使用例
sr = sharpe_ratio(df['return'])
print(f"シャープレシオ: {sr:.2f}")
```

**解釈:**
- 1.0以上: 良好
- 2.0以上: 優秀
- 0.5未満: 改善が必要

**aurumでの使用:**
- NISA/iDeCoの効率評価
- 複数の投資信託の比較
- リバランス戦略の評価

---

### 2.2. 最大ドローダウン（Maximum Drawdown）

**定義:** ピークからの最大下落率

**計算式:**
```
最大ドローダウン = (谷の価格 - ピークの価格) / ピークの価格
```

**Python実装:**
```python
def max_drawdown(prices):
    """
    最大ドローダウンを計算

    Parameters:
    - prices: 価格のSeries

    Returns:
    - Maximum Drawdown（%）
    - ピークの日付
    - 谷の日付
    """
    cumulative = (1 + prices.pct_change()).cumprod()
    running_max = cumulative.expanding().max()
    drawdown = (cumulative - running_max) / running_max

    max_dd = drawdown.min()
    peak_idx = drawdown.idxmin()
    valley_idx = running_max[:peak_idx].idxmax()

    return max_dd, valley_idx, peak_idx

# 使用例
mdd, peak_date, valley_date = max_drawdown(df['price'])
print(f"最大ドローダウン: {mdd:.2%}")
print(f"ピーク: {peak_date}, 谷: {valley_date}")
```

**解釈:**
- -10%未満: 低リスク
- -20%～-30%: 中リスク（株式インデックスの標準的範囲）
- -50%以上: 高リスク

**aurumでの使用:**
- 教育費確保の安全性評価（2038年、2040年）
- 最悪ケースシナリオの分析
- リスク許容度の確認

---

### 2.3. ボラティリティ（Volatility）

**定義:** リターンの標準偏差（年率換算）

**Python実装:**
```python
def annualized_volatility(returns, periods_per_year=252):
    """
    年率ボラティリティを計算

    Parameters:
    - returns: リターンのSeries
    - periods_per_year: 年間の期間数（日次=252、月次=12）

    Returns:
    - Annualized Volatility（%）
    """
    return returns.std() * np.sqrt(periods_per_year)

# 使用例
vol = annualized_volatility(df['return'])
print(f"年率ボラティリティ: {vol:.2%}")
```

**aurumでの使用:**
- MSCI ACWI: 16.1%（既に使用中）
- ポートフォリオ全体のリスク評価

---

### 2.4. リターン分布の統計量

**Python実装:**
```python
from scipy import stats

def return_statistics(returns):
    """
    リターンの統計量を計算

    Returns:
    - 平均、標準偏差、歪度、尖度
    """
    return {
        'mean': returns.mean(),
        'std': returns.std(),
        'skewness': stats.skew(returns.dropna()),  # 歪度（正規分布=0）
        'kurtosis': stats.kurtosis(returns.dropna())  # 尖度（正規分布=0）
    }

# 使用例
stats_dict = return_statistics(df['return'])
print(stats_dict)
```

**解釈:**
- **歪度（Skewness）**:
  - 負: 左裾が長い（大きな損失が稀に発生）
  - 正: 右裾が長い（大きな利益が稀に発生）
- **尖度（Kurtosis）**:
  - 正: ファットテール（極端な値が多い）
  - 負: 正規分布より平坦

---

## 3. バックテストの実施方法

### 3.1. 訓練/テスト分割

**目的:** 過学習を防ぎ、戦略の汎用性を検証する

**標準手法:**
```python
def train_test_split_timeseries(df, train_ratio=0.8):
    """
    時系列データを訓練/テストに分割

    Parameters:
    - df: DataFrame
    - train_ratio: 訓練データの割合（0.7-0.8が標準）

    Returns:
    - train_df, test_df
    """
    split_idx = int(len(df) * train_ratio)
    train_df = df.iloc[:split_idx]
    test_df = df.iloc[split_idx:]

    print(f"訓練期間: {train_df.index[0]} - {train_df.index[-1]}")
    print(f"テスト期間: {test_df.index[0]} - {test_df.index[-1]}")

    return train_df, test_df

# 使用例
train, test = train_test_split_timeseries(df, train_ratio=0.8)
```

**重要な注意事項:**
- 時系列データは**ランダムシャッフル禁止**（時間順序を保持）
- 訓練データのみで戦略を開発
- テストデータでの評価は**1回のみ**（複数回評価すると過学習）

---

### 3.2. データリーク防止

**データリークとは:**
未来の情報が訓練データに混入すること（過学習の原因）

**よくあるデータリークの例:**
```python
# ❌ 間違い: 全期間の統計量を使用
df['z_score'] = (df['price'] - df['price'].mean()) / df['price'].std()

# ✅ 正しい: 過去データのみで計算
df['z_score'] = df['price'].rolling(window=20).apply(
    lambda x: (x.iloc[-1] - x.mean()) / x.std()
)
```

**チェックリスト:**
- [ ] 訓練データとテストデータを明確に分離したか？
- [ ] 統計量（平均、標準偏差）は訓練データのみで計算したか？
- [ ] 「シグナル生成後、次のバーで約定」の遅延を考慮したか？
- [ ] 将来情報（earnings発表日等）を使っていないか？

---

### 3.3. バックテストの評価指標

**標準的な評価項目:**
```python
def backtest_summary(returns):
    """
    バックテストの評価指標を出力
    """
    total_return = (1 + returns).prod() - 1
    annualized_return = (1 + total_return) ** (252 / len(returns)) - 1
    sharpe = sharpe_ratio(returns)
    mdd, _, _ = max_drawdown((1 + returns).cumprod())

    print("=== Backtest Summary ===")
    print(f"総リターン: {total_return:.2%}")
    print(f"年率リターン: {annualized_return:.2%}")
    print(f"シャープレシオ: {sharpe:.2f}")
    print(f"最大ドローダウン: {mdd:.2%}")
    print(f"勝率: {(returns > 0).sum() / len(returns):.2%}")
```

---

## 4. aurumプロジェクトへの適用例

### 4.1. NISAポートフォリオの評価

```python
# データ読み込み
nisa_df = pd.read_csv(CSV_DIR / 'nisa_portfolio.csv')

# EDA
print(nisa_df.describe())

# シャープレシオ計算
sr = sharpe_ratio(nisa_df['return'])
print(f"NISAシャープレシオ: {sr:.2f}")

# 最大ドローダウン
mdd, _, _ = max_drawdown(nisa_df['value'])
print(f"NISA最大ドローダウン: {mdd:.2%}")
```

**判断基準:**
- シャープレシオ1.0以上 → 効率的
- 最大ドローダウン-30%以内 → 許容範囲

---

### 4.2. リバランス戦略のバックテスト

**検証する戦略:**
- 戦略A: 年1回リバランス
- 戦略B: 年2回リバランス
- 戦略C: 5%以上の乖離で閾値ベースリバランス

**実装例:**
```python
def backtest_rebalance_strategy(df, strategy='annual'):
    """
    リバランス戦略のバックテスト
    """
    # 訓練/テスト分割
    train, test = train_test_split_timeseries(df, train_ratio=0.8)

    # 訓練データで戦略開発
    # ... (省略)

    # テストデータで評価
    test_returns = calculate_returns(test, strategy)
    backtest_summary(test_returns)

    return test_returns
```

---

### 4.3. 教育費達成確率のロバストネス検証

**現状の問題:**
- 「年率6%のリターン」を前提にしているが、過去データで検証していない

**改善案:**
```python
def historical_simulation(df, investment_years=19):
    """
    過去データで「同じ戦略を実行したらどうなったか」を検証
    """
    results = []

    # ローリングウィンドウで検証（例: 2000-2019, 2001-2020, ...）
    for start_year in range(2000, 2025 - investment_years):
        end_year = start_year + investment_years
        period_df = df[(df['year'] >= start_year) & (df['year'] < end_year)]

        final_value = simulate_investment(period_df)
        results.append({
            'start_year': start_year,
            'end_year': end_year,
            'final_value': final_value
        })

    results_df = pd.DataFrame(results)
    print(f"平均: {results_df['final_value'].mean():.0f}万円")
    print(f"最悪: {results_df['final_value'].min():.0f}万円")
    print(f"5%ile: {results_df['final_value'].quantile(0.05):.0f}万円")

    return results_df
```

---

## 5. 標準テンプレート

### 5.1. 新規投資信託の評価テンプレート

```python
"""
投資信託評価テンプレート
"""

# 1. データ取得
fund_df = fetch_fund_data('fund_code')

# 2. EDA
print(fund_df.describe())
plot_time_series(fund_df)
plot_return_distribution(fund_df)

# 3. 定量評価
sr = sharpe_ratio(fund_df['return'])
mdd, _, _ = max_drawdown(fund_df['price'])
vol = annualized_volatility(fund_df['return'])

print(f"シャープレシオ: {sr:.2f}")
print(f"最大ドローダウン: {mdd:.2%}")
print(f"ボラティリティ: {vol:.2%}")

# 4. 比較分析（既存ファンドとの比較）
compare_with_benchmark(fund_df, benchmark='MSCI_ACWI')

# 5. 結論
if sr >= 1.0 and mdd >= -0.3:
    print("評価: 投資候補として適格")
else:
    print("評価: 要検討")
```

---

### 5.2. 月次ポートフォリオレビューテンプレート

```python
"""
月次ポートフォリオレビュー
"""

# 1. 当月のパフォーマンス
monthly_return = calculate_monthly_return()
print(f"当月リターン: {monthly_return:.2%}")

# 2. 累積パフォーマンス
cumulative_return = calculate_cumulative_return()
print(f"累積リターン: {cumulative_return:.2%}")

# 3. リスク指標
current_vol = annualized_volatility(recent_returns)
current_mdd = max_drawdown(portfolio_value)[0]
print(f"ボラティリティ: {current_vol:.2%}")
print(f"最大ドローダウン: {current_mdd:.2%}")

# 4. アセットアロケーション確認
check_asset_allocation()

# 5. リバランスの必要性判断
if needs_rebalancing():
    print("リバランス推奨")
else:
    print("現状維持")
```

---

## 6. データリーク防止のチェックリスト

投資判断・シミュレーション実施時に必ず確認：

- [ ] 訓練データとテストデータを分離したか？
- [ ] 統計量（平均、標準偏差）は訓練データのみで計算したか？
- [ ] 将来情報を使用していないか？
- [ ] 「シグナル生成→執行」の遅延を考慮したか？
- [ ] 過学習していないか？（テストデータでの評価は1回のみ）

---

## 7. 参考資料

### 学術的根拠
- **シャープレシオ**: William F. Sharpe (1966) "Mutual Fund Performance"
- **効率的市場仮説**: Eugene Fama (1970) "Efficient Capital Markets"
- **モンテカルロシミュレーション**: Metropolis & Ulam (1949)

### 実装例
- GMO「Claude Codeを使った投資戦略自動生成」（2025年）
- `outputs/reports/working/temp_1.md` (GMO記事分析)

---

## 8. よくある質問

### Q1: バックテストと将来予測の違いは？
**A:** バックテストは過去データでの検証、将来予測は未来の期待値を計算。aurumでは「過去データで同じ戦略がどう機能したか」を検証（バックテスト）してから、将来予測を行うべき。

### Q2: シャープレシオが高ければ良い投資？
**A:** 必ずしもそうではない。シャープレシオは「リスク調整後リターン」を測る指標だが、最大ドローダウンやリターン分布の歪度も考慮する必要がある。

### Q3: データリークを完全に防ぐ方法は？
**A:** 訓練/テスト分割を厳格に守り、統計量は常に「過去データのみ」で計算すること。また、テストデータでの評価は1回のみとし、「何度もテストして最良のパラメータを選ぶ」ことを避ける。

---

**最終更新:** 2025年11月6日
**次回レビュー:** 実際のバックテスト実施後（2025年11月中旬予定）
