import numpy as np
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

# 日本語フォントの設定
plt.rcParams['font.sans-serif'] = ['MS Gothic', 'Yu Gothic', 'Hiragino Sans']
plt.rcParams['axes.unicode_minus'] = False

print("="*80)
print("2026年NISA枠360万円の最適配分分析")
print("="*80)

# ===== 基本情報 =====
CURRENT_YEAR = 2025
CURRENT_AGE = 41
CURRENT_ASSETS = 1491  # 万円

# 現在の資産詳細（2025年10月31日時点）
CURRENT_NISA = [NISA_ASSETS]  # 個人設定から読み込んでください
CURRENT_IDECO = [IDECO_ASSETS]  # 個人設定から読み込んでください
CURRENT_COMPANY_STOCK = 300
CURRENT_CASH = 300

# NISA保有銘柄（評価額・万円）
NISA_SP500 = 171.2
NISA_ALLCOUNTRY = 38.3
NISA_EXJAPAN = 619.3

# ===== 各銘柄の統計データ（調査結果から） =====

# 1年リターン（2024年10月〜2025年10月）
RETURNS_1Y = {
    'S&P500': 22.37,
    'オルカン': 22.06,
    '除く日本': 22.14
}

# 過去5年の年率リターン（推定）
RETURNS_5Y = {
    'S&P500': 22.5,   # 2019-2024年の実績
    'オルカン': 18.99, # 2019-2024年のトータルリターン
    '除く日本': 22.0   # 調査結果から推定
}

# 標準偏差（ボラティリティ）
VOLATILITY = {
    'S&P500': 17.27,   # S&P500連動商品の平均
    'オルカン': 16.06,  # 5年標準偏差
    '除く日本': 16.1    # MSCI ACWI ex Japanの10年標準偏差（推定）
}

# 手数料（信託報酬）
FEES = {
    'S&P500': 0.0814,
    'オルカン': 0.05775,
    '除く日本': 0.05775
}

# コロナショック時の下落率
MAX_DRAWDOWN = {
    'S&P500': -18.11,
    'オルカン': -19.93,
    '除く日本': -20.5  # 推定（オルカンよりやや大きい）
}

# ===== 教育費目標 =====
EDUCATION_TARGET = 2400  # 万円
YEARS_TO_ELDEST = 13     # 2038年まで
YEARS_TO_YOUNGEST = 15   # 2040年まで

# ===== 2026年NISA枠 =====
NISA_2026_TSUMITATE = 120  # つみたて投資枠
NISA_2026_GROWTH = 240     # 成長投資枠
NISA_2026_TOTAL = 360      # 合計

print(f"\n【現在の資産状況】2025年10月31日時点")
print(f"総資産: {CURRENT_ASSETS}万円")
print(f"  NISA: {CURRENT_NISA}万円")
print(f"    ├ S&P500: {NISA_SP500}万円（{NISA_SP500/CURRENT_NISA*100:.1f}%）")
print(f"    ├ オルカン: {NISA_ALLCOUNTRY}万円（{NISA_ALLCOUNTRY/CURRENT_NISA*100:.1f}%）")
print(f"    └ 除く日本: {NISA_EXJAPAN}万円（{NISA_EXJAPAN/CURRENT_NISA*100:.1f}%）")
print(f"  iDeCo: {CURRENT_IDECO}万円")
print(f"  自社株: {CURRENT_COMPANY_STOCK}万円（{CURRENT_COMPANY_STOCK/CURRENT_ASSETS*100:.1f}%）")
print(f"  現金: {CURRENT_CASH}万円")

print(f"\n【2026年NISA枠】")
print(f"つみたて投資枠: {NISA_2026_TSUMITATE}万円")
print(f"成長投資枠: {NISA_2026_GROWTH}万円")
print(f"合計: {NISA_2026_TOTAL}万円")

# ===== 各選択肢の定義 =====

options = {
    'A': {
        'name': '全額「除く日本」継続',
        'allocation': {'除く日本': 360, 'オルカン': 0, 'S&P500': 0},
        'rationale': '現在の方針を継続、自社株との分散維持'
    },
    'B': {
        'name': '「オルカン」に統一',
        'allocation': {'オルカン': 360, '除く日本': 0, 'S&P500': 0},
        'rationale': '最も分散された選択、日本株も含む'
    },
    'C': {
        'name': '現状維持ミックス',
        'allocation': {'除く日本': 240, 'オルカン': 60, 'S&P500': 60},
        'rationale': '過去の比率を維持（除く日本75%, オルカン5%, S&P500 20%）'
    },
    'D': {
        'name': '「除く日本」メイン + 少額実験',
        'allocation': {'除く日本': 320, 'S&P500': 40, 'オルカン': 0},
        'rationale': '除く日本をコアに、S&P500を少額実験'
    }
}

# ===== 分析関数 =====

def calculate_portfolio_stats(allocation):
    """ポートフォリオの統計指標を計算"""
    total = sum(allocation.values())
    weights = {k: v/total for k, v in allocation.items()}

    # 期待リターン（加重平均、手数料控除後）
    expected_return = sum(weights[k] * (RETURNS_5Y[k] - FEES[k]) for k in weights.keys())

    # ボラティリティ（簡易計算、相関係数を0.9と仮定）
    variance = 0
    correlation = 0.9  # 全世界株式の各地域は高相関

    for k1, w1 in weights.items():
        for k2, w2 in weights.items():
            if k1 == k2:
                variance += (w1 ** 2) * (VOLATILITY[k1] ** 2)
            else:
                variance += 2 * w1 * w2 * correlation * VOLATILITY[k1] * VOLATILITY[k2]

    portfolio_volatility = np.sqrt(variance)

    # シャープレシオ（無リスク金利を0%と仮定）
    sharpe_ratio = expected_return / portfolio_volatility if portfolio_volatility > 0 else 0

    # 最大ドローダウン（加重平均）
    max_dd = sum(weights[k] * MAX_DRAWDOWN[k] for k in weights.keys())

    return {
        'expected_return': expected_return,
        'volatility': portfolio_volatility,
        'sharpe_ratio': sharpe_ratio,
        'max_drawdown': max_dd
    }

def monte_carlo_education_goal(allocation, current_total, target, years, simulations=10000):
    """教育費達成確率のモンテカルロシミュレーション"""
    np.random.seed(42)

    # ポートフォリオ統計
    stats = calculate_portfolio_stats(allocation)
    mean_return = stats['expected_return']
    volatility = stats['volatility']

    success_count = 0
    final_values = []

    for _ in range(simulations):
        value = current_total
        for year in range(years):
            annual_return = np.random.normal(mean_return, volatility)
            value *= (1 + annual_return / 100)

        final_values.append(value)
        if value >= target:
            success_count += 1

    success_rate = (success_count / simulations) * 100
    median = np.median(final_values)
    percentile_10 = np.percentile(final_values, 10)
    percentile_90 = np.percentile(final_values, 90)

    return {
        'success_rate': success_rate,
        'median': median,
        'p10': percentile_10,
        'p90': percentile_90
    }

def simulate_60yo_assets(allocation, simulations=10000):
    """60歳時点の総資産シミュレーション"""
    np.random.seed(42)

    stats = calculate_portfolio_stats(allocation)
    mean_return = stats['expected_return']
    volatility = stats['volatility']

    years = 19  # 2025-2044年

    # 既存資産の成長
    existing_nisa = CURRENT_NISA
    existing_ideco = CURRENT_IDECO
    existing_stock = CURRENT_COMPANY_STOCK

    # 新規投資
    monthly_nisa_2025_2026 = 10.0
    monthly_nisa_2027_onwards = 10.0
    monthly_ideco_2025_2026 = 2.3
    monthly_ideco_2027_onwards = 6.2
    wife_monthly_nisa = 5.0  # 2028年から

    results = {'conservative': {}, 'standard': {}, 'optimistic': {}}
    scenarios = {'conservative': 5.0, 'standard': 6.0, 'optimistic': 7.0}

    for scenario_name, scenario_return in scenarios.items():
        # 既存資産の成長
        existing_growth = (existing_nisa + existing_ideco + existing_stock) * ((1 + scenario_return/100) ** years)

        # NISA新規積立（2025-2026: 2年、2027-2044: 18年）
        nisa_accumulation_2025_2026 = monthly_nisa_2025_2026 * 12 * ((((1 + scenario_return/100/12) ** 24) - 1) / (scenario_return/100/12))
        nisa_accumulation_2027_onwards = monthly_nisa_2027_onwards * 12 * ((((1 + scenario_return/100/12) ** 216) - 1) / (scenario_return/100/12))

        # iDeCo新規積立
        ideco_accumulation_2025_2026 = monthly_ideco_2025_2026 * 12 * ((((1 + scenario_return/100/12) ** 24) - 1) / (scenario_return/100/12))
        ideco_accumulation_2027_onwards = monthly_ideco_2027_onwards * 12 * ((((1 + scenario_return/100/12) ** 204) - 1) / (scenario_return/100/12))

        # 妻NISA（2028-2044: 17年）
        wife_accumulation = wife_monthly_nisa * 12 * ((((1 + scenario_return/100/12) ** 204) - 1) / (scenario_return/100/12))

        total = existing_growth + nisa_accumulation_2025_2026 + nisa_accumulation_2027_onwards + \
                ideco_accumulation_2025_2026 + ideco_accumulation_2027_onwards + wife_accumulation

        after_education = total - EDUCATION_TARGET

        results[scenario_name] = {
            'total': total,
            'after_education': after_education
        }

    return results

# ===== 各選択肢の評価 =====

print("\n" + "="*80)
print("各選択肢の統計的評価")
print("="*80)

evaluation_results = {}

for option_key, option_data in options.items():
    print(f"\n{'='*80}")
    print(f"選択肢{option_key}: {option_data['name']}")
    print(f"{'='*80}")
    print(f"戦略: {option_data['rationale']}")

    allocation = option_data['allocation']
    print(f"\n【配分】")
    for fund, amount in allocation.items():
        if amount > 0:
            print(f"  {fund}: {amount}万円（{amount/NISA_2026_TOTAL*100:.1f}%）")

    # 統計指標
    stats = calculate_portfolio_stats(allocation)
    print(f"\n【統計指標】")
    print(f"期待年率リターン: {stats['expected_return']:.2f}%")
    print(f"年率ボラティリティ: {stats['volatility']:.2f}%")
    print(f"シャープレシオ: {stats['sharpe_ratio']:.2f}")
    print(f"最大ドローダウン（推定）: {stats['max_drawdown']:.2f}%")

    # 2026年投資後のNISA総額
    future_nisa = CURRENT_NISA + NISA_2026_TOTAL
    print(f"\n【2026年投資後のNISA総額】{future_nisa:.1f}万円")

    # 2026年投資後のポートフォリオ構成
    print(f"\n【2026年投資後のポートフォリオ構成】")
    new_sp500 = NISA_SP500 + allocation.get('S&P500', 0)
    new_allcountry = NISA_ALLCOUNTRY + allocation.get('オルカン', 0)
    new_exjapan = NISA_EXJAPAN + allocation.get('除く日本', 0)

    print(f"  S&P500: {new_sp500:.1f}万円（{new_sp500/future_nisa*100:.1f}%）")
    print(f"  オルカン: {new_allcountry:.1f}万円（{new_allcountry/future_nisa*100:.1f}%）")
    print(f"  除く日本: {new_exjapan:.1f}万円（{new_exjapan/future_nisa*100:.1f}%）")

    # 教育費達成確率（2038年）
    print(f"\n【教育費達成確率】2038年時点で2,400万円")
    education_sim = monte_carlo_education_goal(
        allocation,
        future_nisa,
        EDUCATION_TARGET,
        YEARS_TO_ELDEST,
        simulations=10000
    )
    print(f"  達成確率: {education_sim['success_rate']:.1f}%")
    print(f"  中央値: {education_sim['median']:.0f}万円")
    print(f"  10%タイル値: {education_sim['p10']:.0f}万円")
    print(f"  90%タイル値: {education_sim['p90']:.0f}万円")

    if education_sim['success_rate'] >= 90:
        education_eval = "[OK] 非常に高い確率で達成"
    elif education_sim['success_rate'] >= 75:
        education_eval = "[OK] 高い確率で達成"
    elif education_sim['success_rate'] >= 50:
        education_eval = "[WARNING] 達成可能だが不確実性あり"
    else:
        education_eval = "[NG] 達成困難"

    print(f"  評価: {education_eval}")

    # 60歳時点の資産予測
    print(f"\n【60歳時点の総資産予測】2044年")
    assets_60 = simulate_60yo_assets(allocation)

    for scenario_name, scenario_label in [('conservative', '保守的'), ('standard', '標準'), ('optimistic', '楽観的')]:
        scenario_data = assets_60[scenario_name]
        print(f"\n  {scenario_label}シナリオ:")
        print(f"    総資産: {scenario_data['total']:.0f}万円")
        print(f"    教育費控除後: {scenario_data['after_education']:.0f}万円")

        if scenario_data['after_education'] >= 5000:
            eval_60 = "[OK] 目標達成"
        elif scenario_data['after_education'] >= 3000:
            eval_60 = "[WARNING] やや不足"
        else:
            eval_60 = "[NG] 大幅不足"

        print(f"    評価: {eval_60}")

    # 総合評価点の計算
    score = 0

    # リターン（最大30点）
    score += min(30, stats['expected_return'] * 1.5)

    # シャープレシオ（最大20点）
    score += min(20, stats['sharpe_ratio'] * 10)

    # 教育費達成確率（最大30点）
    score += min(30, education_sim['success_rate'] * 0.3)

    # 低コスト（最大10点）
    avg_fee = sum(allocation[k]/NISA_2026_TOTAL * FEES[k] for k in allocation.keys())
    score += 10 - avg_fee * 100

    # 分散性（最大10点、単一銘柄集中はマイナス）
    num_funds = sum(1 for v in allocation.values() if v > 0)
    score += num_funds * 3

    print(f"\n【総合評価】")
    print(f"評価点数: {score:.1f}/100点")

    # 支持度の計算
    support = education_sim['success_rate']  # 教育費達成確率をベースに
    print(f"支持度: {support:.1f}%")

    # 結果を保存
    evaluation_results[option_key] = {
        'name': option_data['name'],
        'score': score,
        'support': support,
        'expected_return': stats['expected_return'],
        'volatility': stats['volatility'],
        'sharpe_ratio': stats['sharpe_ratio'],
        'education_success': education_sim['success_rate'],
        'median_2038': education_sim['median'],
        'assets_60_standard': assets_60['standard']['total'],
        'assets_60_after_education': assets_60['standard']['after_education']
    }

# ===== 比較表 =====

print("\n" + "="*80)
print("選択肢の比較表")
print("="*80)

comparison_df = pd.DataFrame(evaluation_results).T
comparison_df = comparison_df.sort_values('score', ascending=False)

print("\n【評価点数ランキング】")
print(comparison_df[['name', 'score', 'support']].to_string())

print("\n【統計指標の比較】")
print(comparison_df[['name', 'expected_return', 'volatility', 'sharpe_ratio']].to_string())

print("\n【教育費・老後資金の比較】")
print(comparison_df[['name', 'education_success', 'median_2038', 'assets_60_standard']].to_string())

# ===== 最終推奨 =====

print("\n" + "="*80)
print("最終推奨")
print("="*80)

best_option_key = comparison_df.index[0]
best_option = evaluation_results[best_option_key]

print(f"\n【統計的に最も優れた選択肢】")
print(f"選択肢{best_option_key}: {best_option['name']}")
print(f"評価点数: {best_option['score']:.1f}/100点")
print(f"支持度: {best_option['support']:.1f}%")

print(f"\n【推奨理由】")
print(f"1. 期待年率リターン: {best_option['expected_return']:.2f}%")
print(f"2. リスク調整後リターン（シャープレシオ）: {best_option['sharpe_ratio']:.2f}")
print(f"3. 教育費達成確率: {best_option['education_success']:.1f}%")
print(f"4. 2038年時点の予想資産（中央値）: {best_option['median_2038']:.0f}万円")
print(f"5. 60歳時点の総資産（標準シナリオ）: {best_option['assets_60_standard']:.0f}万円")

print("\n" + "="*80)
print("分析完了")
print("="*80)
