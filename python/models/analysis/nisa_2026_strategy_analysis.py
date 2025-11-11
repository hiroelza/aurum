import numpy as np
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # バックエンドを設定

# 日本語フォントの設定
plt.rcParams['font.sans-serif'] = ['MS Gothic', 'Yu Gothic', 'Hiragino Sans']
plt.rcParams['axes.unicode_minus'] = False

# ===== 個人情報の読み込み =====
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from personal_config import (
    CURRENT_AGE, CURRENT_YEAR, RETIREMENT_AGE, RETIREMENT_YEAR,
    ELDEST_CHILD_AGE,
    CURRENT_NISA, CURRENT_IDECO, CURRENT_COMPANY_STOCK, CURRENT_CASH, TOTAL_ASSETS,
    ANNUAL_INCOME_AFTER_TAX,
    NISA_LIFETIME_REMAINING,
    EDUCATION_COST
)

# 長女の大学入学年（計算）
ELDEST_CHILD_UNIVERSITY_YEAR = CURRENT_YEAR + (18 - ELDEST_CHILD_AGE)

# 2026年NISA枠
NISA_2026_TSUMITATE = 120  # つみたて投資枠
NISA_2026_GROWTH = 240  # 成長投資枠
NISA_2026_TOTAL = NISA_2026_TSUMITATE + NISA_2026_GROWTH

# ===== 過去のパフォーマンスデータ（INVESTMENT_PROFILE.mdより） =====
# 実績リターン（2025年10月時点）
ACTUAL_RETURNS = {
    'S&P500': 34.9,  # 含み益ベース
    'オルカン': 36.4,
    '除く日本': 20.2
}

# ===== 統計データ（みんかぶ・Yahoo!ファイナンスより） =====

# 各インデックスの過去リターン（年率%）
HISTORICAL_RETURNS = {
    'S&P500': {
        '3年': 14.2,
        '5年': 18.5,
        '10年': 14.8
    },
    'オルカン': {
        '3年': 12.8,
        '5年': 15.2,
        '10年': 12.5
    },
    '除く日本': {
        '3年': 13.1,
        '5年': 15.8,
        '10年': 12.8
    }
}

# 各インデックスのボラティリティ（標準偏差%）
VOLATILITY = {
    'S&P500': 18.5,
    'オルカン': 16.1,
    '除く日本': 16.3
}

# シャープレシオ（リスク調整後リターン）
SHARPE_RATIO = {
    'S&P500': 0.80,
    'オルカン': 0.78,
    '除く日本': 0.79
}

# 最大ドローダウン（過去10年）
MAX_DRAWDOWN = {
    'S&P500': -34.0,  # 2022年ハイテク株暴落
    'オルカン': -28.5,
    '除く日本': -29.2
}

# 信託報酬（年率%）
EXPENSE_RATIO = {
    'S&P500': 0.0814,
    'オルカン': 0.05775,
    '除く日本': 0.05775
}

# ===== 選択肢の定義 =====

STRATEGIES = {
    'A': {
        'name': '全額「除く日本」継続（360万円）',
        '除く日本': 360,
        'オルカン': 0,
        'S&P500': 0,
        '配当株・REIT': 0,
        '実験枠': 0
    },
    'B': {
        'name': '「オルカン」に統一（360万円）',
        '除く日本': 0,
        'オルカン': 360,
        'S&P500': 0,
        '配当株・REIT': 0,
        '実験枠': 0
    },
    'C': {
        'name': '「S&P500」に集中（360万円）',
        '除く日本': 0,
        'オルカン': 0,
        'S&P500': 360,
        '配当株・REIT': 0,
        '実験枠': 0
    },
    'D': {
        'name': '2段階戦略（320万円インデックス + 40万円実験枠）',
        '除く日本': 160,
        'オルカン': 160,
        'S&P500': 0,
        '配当株・REIT': 0,
        '実験枠': 40
    },
    'E': {
        'name': '配当戦略（270万円インデックス + 90万円配当株・REIT）',
        '除く日本': 180,
        'オルカン': 90,
        'S&P500': 0,
        '配当株・REIT': 90,
        '実験枠': 0
    }
}

# ===== 評価関数 =====

def calculate_expected_return(strategy):
    """期待リターン（10年平均）を計算"""
    total_return = 0
    total_amount = 0

    for asset, amount in strategy.items():
        if asset in ['除く日本', 'オルカン', 'S&P500'] and amount > 0:
            return_rate = HISTORICAL_RETURNS[asset]['10年']
            total_return += return_rate * amount
            total_amount += amount

    # 配当株・REITは年率4%想定
    if strategy.get('配当株・REIT', 0) > 0:
        total_return += 4.0 * strategy['配当株・REIT']
        total_amount += strategy['配当株・REIT']

    # 実験枠は年率10%想定（ハイリスク・ハイリターン）
    if strategy.get('実験枠', 0) > 0:
        total_return += 10.0 * strategy['実験枠']
        total_amount += strategy['実験枠']

    return total_return / total_amount if total_amount > 0 else 0

def calculate_risk(strategy):
    """リスク（加重平均ボラティリティ）を計算"""
    total_risk = 0
    total_amount = 0

    for asset, amount in strategy.items():
        if asset in ['除く日本', 'オルカン', 'S&P500'] and amount > 0:
            volatility = VOLATILITY[asset]
            total_risk += (volatility ** 2) * amount
            total_amount += amount

    # 配当株・REITはボラティリティ12%想定（株式より低い）
    if strategy.get('配当株・REIT', 0) > 0:
        total_risk += (12.0 ** 2) * strategy['配当株・REIT']
        total_amount += strategy['配当株・REIT']

    # 実験枠はボラティリティ25%想定（高リスク）
    if strategy.get('実験枠', 0) > 0:
        total_risk += (25.0 ** 2) * strategy['実験枠']
        total_amount += strategy['実験枠']

    return np.sqrt(total_risk / total_amount) if total_amount > 0 else 0

def calculate_sharpe_ratio(expected_return, risk):
    """シャープレシオを計算（リスクフリーレート0.5%想定）"""
    risk_free_rate = 0.5
    return (expected_return - risk_free_rate) / risk if risk > 0 else 0

def calculate_expense_ratio(strategy):
    """加重平均信託報酬を計算"""
    total_expense = 0
    total_amount = 0

    for asset, amount in strategy.items():
        if asset in ['除く日本', 'オルカン', 'S&P500'] and amount > 0:
            expense = EXPENSE_RATIO[asset]
            total_expense += expense * amount
            total_amount += amount

    # 配当株・REITは0.2%想定
    if strategy.get('配当株・REIT', 0) > 0:
        total_expense += 0.2 * strategy['配当株・REIT']
        total_amount += strategy['配当株・REIT']

    # 実験枠は0.8%想定（高コスト）
    if strategy.get('実験枠', 0) > 0:
        total_expense += 0.8 * strategy['実験枠']
        total_amount += strategy['実験枠']

    return total_expense / total_amount if total_amount > 0 else 0

def monte_carlo_education_fund(strategy_allocation, years=13, simulations=10000):
    """教育費達成確率をモンテカルロシミュレーション（2038年時点）"""
    np.random.seed(42)

    success_count = 0
    final_values = []

    for _ in range(simulations):
        # 既存資産の成長（NISA [NISA_ASSETS]万円 + iDeCo [IDECO_ASSETS]万円 + 自社株 300万円）
        existing_value = CURRENT_NISA + CURRENT_IDECO + CURRENT_COMPANY_STOCK

        # 既存資産は「除く日本」と仮定（平均リターン12.8%、ボラティリティ16.3%）
        for year in range(years):
            annual_return = np.random.normal(12.8, 16.3)
            existing_value *= (1 + annual_return / 100)

        # 2026年投資分（360万円）の成長（12年間）
        new_investment_value = 0
        for asset, amount in strategy_allocation.items():
            if amount > 0:
                value = amount
                for year in range(12):  # 2026年投資分は12年間成長
                    if asset == '除く日本':
                        annual_return = np.random.normal(12.8, 16.3)
                    elif asset == 'オルカン':
                        annual_return = np.random.normal(12.5, 16.1)
                    elif asset == 'S&P500':
                        annual_return = np.random.normal(14.8, 18.5)
                    elif asset == '配当株・REIT':
                        annual_return = np.random.normal(4.0, 12.0)
                    elif asset == '実験枠':
                        annual_return = np.random.normal(10.0, 25.0)
                    else:
                        continue

                    value *= (1 + annual_return / 100)

                new_investment_value += value

        # 2027年以降の月次積立（月16.2万円、2027-2038年の12年間）
        monthly_investment = 16.2
        accumulation = 0
        for month in range(144):  # 12年 × 12ヶ月
            annual_return = np.random.normal(12.8, 16.3)
            monthly_return = annual_return / 12 / 100
            accumulation = (accumulation + monthly_investment) * (1 + monthly_return)

        # 妻NISA（月5万円、2028-2038年の11年間）
        wife_accumulation = 0
        for month in range(132):  # 11年 × 12ヶ月
            annual_return = np.random.normal(12.5, 16.1)
            monthly_return = annual_return / 12 / 100
            wife_accumulation = (wife_accumulation + 5.0) * (1 + monthly_return)

        total_value = existing_value + new_investment_value + accumulation + wife_accumulation
        final_values.append(total_value)

        if total_value >= EDUCATION_COST:
            success_count += 1

    success_rate = (success_count / simulations) * 100
    median_value = np.median(final_values)
    percentile_10 = np.percentile(final_values, 10)
    percentile_90 = np.percentile(final_values, 90)

    return success_rate, median_value, percentile_10, percentile_90

def simulate_60yo_assets(strategy_allocation, years=19, simulations=10000):
    """60歳時点の総資産をシミュレーション"""
    np.random.seed(42)

    final_values = []

    for _ in range(simulations):
        # 既存資産の成長（19年間）
        existing_value = CURRENT_NISA + CURRENT_IDECO + CURRENT_COMPANY_STOCK

        for year in range(years):
            annual_return = np.random.normal(12.8, 16.3)
            existing_value *= (1 + annual_return / 100)

        # 2026年投資分（360万円）の成長（18年間）
        new_investment_value = 0
        for asset, amount in strategy_allocation.items():
            if amount > 0:
                value = amount
                for year in range(18):
                    if asset == '除く日本':
                        annual_return = np.random.normal(12.8, 16.3)
                    elif asset == 'オルカン':
                        annual_return = np.random.normal(12.5, 16.1)
                    elif asset == 'S&P500':
                        annual_return = np.random.normal(14.8, 18.5)
                    elif asset == '配当株・REIT':
                        annual_return = np.random.normal(4.0, 12.0)
                    elif asset == '実験枠':
                        annual_return = np.random.normal(10.0, 25.0)
                    else:
                        continue

                    value *= (1 + annual_return / 100)

                new_investment_value += value

        # 2027年以降の月次積立（月16.2万円、18年間）
        monthly_investment = 16.2
        accumulation = 0
        for month in range(216):  # 18年 × 12ヶ月
            annual_return = np.random.normal(12.8, 16.3)
            monthly_return = annual_return / 12 / 100
            accumulation = (accumulation + monthly_investment) * (1 + monthly_return)

        # 妻NISA（月5万円、2028-2044年の17年間）
        wife_accumulation = 0
        for month in range(204):  # 17年 × 12ヶ月
            annual_return = np.random.normal(12.5, 16.1)
            monthly_return = annual_return / 12 / 100
            wife_accumulation = (wife_accumulation + 5.0) * (1 + monthly_return)

        total_value = existing_value + new_investment_value + accumulation + wife_accumulation
        final_values.append(total_value)

    median_value = np.median(final_values)
    percentile_10 = np.percentile(final_values, 10)
    percentile_90 = np.percentile(final_values, 90)

    return median_value, percentile_10, percentile_90

# ===== 評価の実行 =====

print("="*80)
print("2026年NISA枠360万円の最適な埋め方 - 統計的評価")
print("="*80)
print(f"\n【現在の資産状況（2025年10月31日）】")
print(f"総資産: {TOTAL_ASSETS:.1f}万円")
print(f"  ├ NISA: {CURRENT_NISA:.1f}万円（元本670万円、含み益+{CURRENT_NISA-670:.1f}万円、+{((CURRENT_NISA-670)/670)*100:.1f}%）")
print(f"  ├ iDeCo: {CURRENT_IDECO:.1f}万円（元本51.4万円、含み益+{CURRENT_IDECO-51.4:.1f}万円、+{((CURRENT_IDECO-51.4)/51.4)*100:.1f}%）")
print(f"  ├ 自社株: {CURRENT_COMPANY_STOCK:.1f}万円（[YOUR_COMPANY]、IT/ハイテクセクター）")
print(f"  └ 現金: {CURRENT_CASH:.1f}万円")

print(f"\n【NISA保有銘柄の実績リターン】")
for fund, return_rate in ACTUAL_RETURNS.items():
    print(f"  {fund}: +{return_rate:.1f}%")

print(f"\n【2026年NISA枠】")
print(f"つみたて投資枠: {NISA_2026_TSUMITATE:.0f}万円")
print(f"成長投資枠: {NISA_2026_GROWTH:.0f}万円")
print(f"合計: {NISA_2026_TOTAL:.0f}万円")
print(f"NISA生涯残り枠: {NISA_LIFETIME_REMAINING:.0f}万円")

print("\n" + "="*80)
print("選択肢の統計的評価")
print("="*80)

results = {}

for strategy_id, strategy_data in STRATEGIES.items():
    strategy_name = strategy_data['name']
    allocation = {k: v for k, v in strategy_data.items() if k != 'name'}

    print(f"\n{'='*80}")
    print(f"選択肢{strategy_id}: {strategy_name}")
    print(f"{'='*80}")

    print(f"\n【資産配分】")
    for asset, amount in allocation.items():
        if amount > 0:
            print(f"  {asset}: {amount:.0f}万円（{amount/NISA_2026_TOTAL*100:.1f}%）")

    # 期待リターン
    expected_return = calculate_expected_return(allocation)

    # リスク（ボラティリティ）
    risk = calculate_risk(allocation)

    # シャープレシオ
    sharpe = calculate_sharpe_ratio(expected_return, risk)

    # 信託報酬
    expense = calculate_expense_ratio(allocation)

    print(f"\n【統計的指標】")
    print(f"期待リターン（年率）: {expected_return:.2f}%")
    print(f"リスク（標準偏差）: {risk:.2f}%")
    print(f"シャープレシオ: {sharpe:.3f}")
    print(f"信託報酬（年率）: {expense:.4f}%")

    # 教育費達成確率（2038年時点）
    edu_success_rate, edu_median, edu_p10, edu_p90 = monte_carlo_education_fund(allocation)

    print(f"\n【教育費達成確率（2038年、2,400万円目標）】")
    print(f"シミュレーション回数: 10,000回")
    print(f"達成確率: {edu_success_rate:.1f}%")
    print(f"中央値: {edu_median:.0f}万円")
    print(f"10%タイル値（悪い方から10%）: {edu_p10:.0f}万円")
    print(f"90%タイル値（良い方から10%）: {edu_p90:.0f}万円")

    if edu_success_rate >= 95:
        edu_evaluation = "[OK] 極めて高い確率で達成"
    elif edu_success_rate >= 85:
        edu_evaluation = "[OK] 高い確率で達成"
    elif edu_success_rate >= 70:
        edu_evaluation = "[WARNING] やや不安あり"
    else:
        edu_evaluation = "[NG] 達成困難"

    print(f"評価: {edu_evaluation}")

    # 60歳時点の資産予測
    asset_60_median, asset_60_p10, asset_60_p90 = simulate_60yo_assets(allocation)

    print(f"\n【60歳時点の資産予測（2044年）】")
    print(f"中央値（標準シナリオ）: {asset_60_median:.0f}万円")
    print(f"保守的シナリオ（10%タイル値）: {asset_60_p10:.0f}万円")
    print(f"楽観的シナリオ（90%タイル値）: {asset_60_p90:.0f}万円")
    print(f"教育費控除後（中央値）: {asset_60_median - EDUCATION_COST:.0f}万円")

    if asset_60_median - EDUCATION_COST >= 5000:
        asset_evaluation = "[OK] 目標達成（5,000万円以上）"
    elif asset_60_median - EDUCATION_COST >= 3000:
        asset_evaluation = "[WARNING] やや不足（3,000-5,000万円）"
    else:
        asset_evaluation = "[NG] 大幅不足（3,000万円未満）"

    print(f"評価: {asset_evaluation}")

    # 総合評価点数の計算（0-100点）
    # 期待リターン（30点）
    return_score = min(expected_return / 15.0 * 30, 30)

    # リスク調整後リターン（30点）
    sharpe_score = min(sharpe / 1.0 * 30, 30)

    # 教育費達成確率（30点）
    edu_score = edu_success_rate / 100 * 30

    # コスト（10点、低いほど良い）
    cost_score = max(10 - expense * 10, 0)

    total_score = return_score + sharpe_score + edu_score + cost_score

    # 支持度（%）
    support = min(total_score / 100 * 100, 100)

    print(f"\n【総合評価】")
    print(f"評価点数: {total_score:.1f}/100点")
    print(f"  ├ リターン評価: {return_score:.1f}/30点")
    print(f"  ├ リスク調整後評価: {sharpe_score:.1f}/30点")
    print(f"  ├ 教育費達成評価: {edu_score:.1f}/30点")
    print(f"  └ コスト評価: {cost_score:.1f}/10点")
    print(f"支持度: {support:.1f}%")

    # 伊藤ハヤト氏の投資哲学との整合性評価
    philosophy_score = 0
    philosophy_reasons = []

    # 低コスト（最大20点）
    if expense < 0.1:
        philosophy_score += 20
        philosophy_reasons.append("[OK] 極めて低コスト（0.1%未満）")
    elif expense < 0.2:
        philosophy_score += 15
        philosophy_reasons.append("[OK] 低コスト（0.2%未満）")
    else:
        philosophy_score += 10
        philosophy_reasons.append("[WARNING] やや高コスト")

    # 分散投資（最大30点）
    num_assets = sum(1 for v in allocation.values() if v > 0)
    if allocation.get('除く日本', 0) > 0 or allocation.get('オルカン', 0) > 0:
        philosophy_score += 30
        philosophy_reasons.append("[OK] 全世界分散投資")
    elif allocation.get('S&P500', 0) > 0:
        philosophy_score += 20
        philosophy_reasons.append("[WARNING] 米国集中（分散不足）")

    # パッシブ運用（最大20点）
    if allocation.get('実験枠', 0) == 0:
        philosophy_score += 20
        philosophy_reasons.append("[OK] 完全パッシブ運用")
    elif allocation.get('実験枠', 0) <= 40:
        philosophy_score += 15
        philosophy_reasons.append("[WARNING] 一部アクティブ要素あり（許容範囲）")
    else:
        philosophy_score += 5
        philosophy_reasons.append("[NG] アクティブ要素が大きい")

    # シンプルさ（最大15点）
    if num_assets == 1:
        philosophy_score += 15
        philosophy_reasons.append("[OK] 極めてシンプル（1銘柄）")
    elif num_assets == 2:
        philosophy_score += 12
        philosophy_reasons.append("[OK] シンプル（2銘柄）")
    elif num_assets <= 3:
        philosophy_score += 8
        philosophy_reasons.append("[WARNING] やや複雑（3銘柄）")
    else:
        philosophy_score += 5
        philosophy_reasons.append("[WARNING] 複雑（4銘柄以上）")

    # セクター集中回避（最大15点）
    if allocation.get('S&P500', 0) == 0 and allocation.get('実験枠', 0) == 0:
        philosophy_score += 15
        philosophy_reasons.append("[OK] 自社株考慮でセクター集中回避")
    elif allocation.get('S&P500', 0) > 0:
        philosophy_score += 5
        philosophy_reasons.append("[NG] 米国ハイテク集中リスク")

    print(f"\n【伊藤ハヤト氏の投資哲学との整合性】")
    print(f"哲学スコア: {philosophy_score:.0f}/100点")
    for reason in philosophy_reasons:
        print(f"  {reason}")

    # 結果を保存
    results[strategy_id] = {
        'name': strategy_name,
        'expected_return': expected_return,
        'risk': risk,
        'sharpe_ratio': sharpe,
        'expense_ratio': expense,
        'edu_success_rate': edu_success_rate,
        'edu_median': edu_median,
        'edu_p10': edu_p10,
        'edu_p90': edu_p90,
        'asset_60_median': asset_60_median,
        'asset_60_p10': asset_60_p10,
        'asset_60_p90': asset_60_p90,
        'total_score': total_score,
        'support': support,
        'philosophy_score': philosophy_score
    }

# ===== 最終推奨 =====

print("\n" + "="*80)
print("最終推奨")
print("="*80)

# 総合スコア順にソート
sorted_results = sorted(results.items(), key=lambda x: x[1]['total_score'], reverse=True)

print(f"\n【総合評価ランキング】")
print(f"\n{'順位':<4} {'選択肢':<4} {'評価点':<8} {'支持度':<8} {'哲学':<8} {'期待リターン':<12} {'教育費達成':<12}")
print("-" * 80)

for rank, (strategy_id, data) in enumerate(sorted_results, 1):
    print(f"{rank:<4} {strategy_id:<4} {data['total_score']:>6.1f}点 {data['support']:>6.1f}% {data['philosophy_score']:>6.0f}点 {data['expected_return']:>10.2f}% {data['edu_success_rate']:>10.1f}%")

# 最優秀選択肢
best_strategy_id = sorted_results[0][0]
best_strategy = results[best_strategy_id]

print(f"\n" + "="*80)
print(f"統計的に最も優れた選択肢: 選択肢{best_strategy_id}")
print(f"="*80)

print(f"\n【選択肢{best_strategy_id}: {best_strategy['name']}】")
print(f"\n総合評価点: {best_strategy['total_score']:.1f}/100点（第1位）")
print(f"支持度: {best_strategy['support']:.1f}%")
print(f"投資哲学スコア: {best_strategy['philosophy_score']:.0f}/100点")

print(f"\n【推奨理由】")

# 推奨理由の自動生成
reasons = []

if best_strategy['expected_return'] >= 13.0:
    reasons.append(f"[OK] 高い期待リターン（年率{best_strategy['expected_return']:.2f}%）")
elif best_strategy['expected_return'] >= 12.0:
    reasons.append(f"[OK] 十分な期待リターン（年率{best_strategy['expected_return']:.2f}%）")

if best_strategy['sharpe_ratio'] >= 0.75:
    reasons.append(f"[OK] 優れたリスク調整後リターン（シャープレシオ{best_strategy['sharpe_ratio']:.3f}）")

if best_strategy['edu_success_rate'] >= 95:
    reasons.append(f"[OK] 教育費達成確率が極めて高い（{best_strategy['edu_success_rate']:.1f}%）")
elif best_strategy['edu_success_rate'] >= 85:
    reasons.append(f"[OK] 教育費達成確率が高い（{best_strategy['edu_success_rate']:.1f}%）")

if best_strategy['expense_ratio'] < 0.1:
    reasons.append(f"[OK] 極めて低コスト（信託報酬{best_strategy['expense_ratio']:.4f}%）")

if best_strategy['asset_60_median'] - EDUCATION_COST >= 5000:
    reasons.append(f"[OK] 老後資金も十分確保（60歳時点で{best_strategy['asset_60_median'] - EDUCATION_COST:.0f}万円）")

if best_strategy['philosophy_score'] >= 85:
    reasons.append("[OK] 伊藤ハヤト氏の投資哲学に完全整合")
elif best_strategy['philosophy_score'] >= 70:
    reasons.append("[OK] 伊藤ハヤト氏の投資哲学におおむね整合")

for reason in reasons:
    print(reason.encode('utf-8', errors='replace').decode('utf-8'))

print(f"\n【期待される成果】")
print(f"教育費目標時点:")
print(f"  中央値: {best_strategy['edu_median']:.0f}万円")
print(f"  達成確率: {best_strategy['edu_success_rate']:.1f}%")

print(f"\n退職時点:")
print(f"  保守的: {best_strategy['asset_60_p10']:.0f}万円")
print(f"  標準的: {best_strategy['asset_60_median']:.0f}万円")
print(f"  楽観的: {best_strategy['asset_60_p90']:.0f}万円")
print(f"  教育費控除後: {best_strategy['asset_60_median'] - EDUCATION_COST:.0f}万円")

print("\n" + "="*80)
print("分析完了")
print("="*80)

# 結果をCSV出力
df = pd.DataFrame(results).T
df.to_csv('nisa_2026_strategy_comparison.csv', encoding='utf-8-sig')
print("\n詳細な比較表を 'nisa_2026_strategy_comparison.csv' に出力しました。")
