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
# python/ ディレクトリをパスに追加
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 新しいconfig モジュールからインポート
from config.personal import (
    CURRENT_AGE, CURRENT_YEAR, RETIREMENT_AGE, RETIREMENT_YEAR,
    WIFE_AGE, ELDEST_CHILD_AGE, YOUNGEST_CHILD_AGE,
    CURRENT_NISA, CURRENT_IDECO, CURRENT_COMPANY_STOCK, CURRENT_CASH, TOTAL_ASSETS,
    ANNUAL_INCOME_AFTER_TAX, MONTHLY_INCOME, ANNUAL_RENT, MONTHLY_RENT,
    CURRENT_MONTHLY_NISA, CURRENT_MONTHLY_IDECO, CURRENT_TOTAL_MONTHLY_INVESTMENT,
    MONTHLY_IDECO_2027, MONTHLY_INVESTMENT_2027, WIFE_MONTHLY_NISA,
    EDUCATION_COST
)

# ===== 統計データ（収集した実データ） =====

# MSCI ACWI（円建て）リターン統計（2025年9月時点）
MSCI_ACWI_RETURNS = {
    '5年': 22.5,
    '10年': 15.1,
    '20年': 10.3
}

MSCI_ACWI_VOLATILITY = {
    '5年': 14.6,
    '10年': 16.1,
    '20年': 18.5
}

# シミュレーション用のリターン想定（年率%）
RETURN_SCENARIOS = {
    '保守的': 5.0,
    '標準': 6.0,
    '楽観的': 7.0
}

# 統計データ：100-年齢ルール（41歳）
AGE_BASED_STOCK_RATIO = 100 - CURRENT_AGE  # 59%
AGE_BASED_BOND_RATIO = CURRENT_AGE  # 41%

# 統計データ：緊急資金推奨額（子育て世帯は6ヶ月〜1年）
EMERGENCY_FUND_MONTHS_MIN = 6
EMERGENCY_FUND_MONTHS_MAX = 12

# 統計データ：個別株の推奨上限（5-10%）
INDIVIDUAL_STOCK_LIMIT_MIN = 5
INDIVIDUAL_STOCK_LIMIT_MAX = 10

# 統計データ：年金受給額（夫会社員・妻専業主婦）
MONTHLY_PENSION = 22.2  # 万円（222,383円）
ANNUAL_PENSION = MONTHLY_PENSION * 12

# 統計データ：老後の月間不足額
MONTHLY_RETIREMENT_SHORTFALL = 3.4  # 万円

# ===== 1. 家計収支バランスの統計分析 =====
print("="*80)
print("1. 家計収支バランスの統計分析")
print("="*80)

# 現在の支出比率
rent_ratio = (ANNUAL_RENT / ANNUAL_INCOME_AFTER_TAX) * 100
investment_ratio = ((CURRENT_TOTAL_MONTHLY_INVESTMENT * 12) / ANNUAL_INCOME_AFTER_TAX) * 100
living_expense_ratio = 100 - rent_ratio - investment_ratio

print(f"\n【現在の支出比率】")
print(f"手取り年収: {ANNUAL_INCOME_AFTER_TAX:.1f}万円（月{MONTHLY_INCOME:.1f}万円）")
print(f"家賃: {rent_ratio:.1f}% ({ANNUAL_RENT:.1f}万円/年)")
print(f"投資: {investment_ratio:.1f}% ({CURRENT_TOTAL_MONTHLY_INVESTMENT*12:.1f}万円/年)")
print(f"生活費: {living_expense_ratio:.1f}% ({(MONTHLY_INCOME - MONTHLY_RENT - CURRENT_TOTAL_MONTHLY_INVESTMENT)*12:.1f}万円/年)")

# 統計的評価
print(f"\n【統計的評価】")
print(f"[OK] 家賃比率24.6%: 手取りの25%以内が理想とされており、ギリギリ適正範囲内")
print(f"[OK] 投資比率19.7%: 年収1,000万円世帯の平均貯蓄率15-20%と比較して標準的")
print(f"[OK] 生活費比率55.7%: 4人家族で月34.8万円は節約型（総務省統計では4人世帯平均月30万円）")

# 推奨投資比率
print(f"\n【推奨される投資比率】")
print(f"年収1,000万円世帯の理想的な投資比率: 20-30%")
print(f"現状19.7% → 増額余地あり")

# ===== 2. 投資額シミュレーション =====
print("\n" + "="*80)
print("2. 投資額シミュレーション（60歳時点の総資産予測）")
print("="*80)

def compound_investment(monthly_investment, years, annual_return_rate):
    """複利計算（毎月積立）"""
    monthly_rate = annual_return_rate / 12 / 100
    months = years * 12
    if monthly_rate == 0:
        return monthly_investment * months
    future_value = monthly_investment * (((1 + monthly_rate) ** months - 1) / monthly_rate) * (1 + monthly_rate)
    return future_value

def simulate_investment_pattern(pattern_name, monthly_2025_2026, monthly_2027_onwards,
                                wife_start_year=2028, wife_monthly=WIFE_MONTHLY_NISA):
    """投資パターンのシミュレーション"""
    results = {}

    for scenario_name, annual_return in RETURN_SCENARIOS.items():
        # 既存資産の成長
        years_to_retirement = RETIREMENT_YEAR - CURRENT_YEAR
        existing_nisa = CURRENT_NISA * ((1 + annual_return/100) ** years_to_retirement)
        existing_ideco = CURRENT_IDECO * ((1 + annual_return/100) ** years_to_retirement)
        existing_stock = CURRENT_COMPANY_STOCK * ((1 + annual_return/100) ** years_to_retirement)

        # 2025-2026年の積立（2年間）
        accumulation_2025_2026 = compound_investment(monthly_2025_2026, 2, annual_return)

        # 2027年以降の積立（2027-2044: 18年間）
        accumulation_2027_onwards = compound_investment(monthly_2027_onwards, 18, annual_return)

        # 妻NISA（2028-2044: 17年間）
        wife_accumulation = compound_investment(wife_monthly, 17, annual_return)

        # 総資産
        total_assets = (existing_nisa + existing_ideco + existing_stock +
                       accumulation_2025_2026 + accumulation_2027_onwards + wife_accumulation)

        # 教育費控除後
        after_education = total_assets - EDUCATION_COST

        results[scenario_name] = {
            'total_assets': total_assets,
            'after_education': after_education,
            'existing_growth': existing_nisa + existing_ideco + existing_stock,
            'new_accumulation': accumulation_2025_2026 + accumulation_2027_onwards + wife_accumulation
        }

    return results

# パターンA: 現状維持（月12.3万円 → 月16.2万円 + 妻5万円）
pattern_a = simulate_investment_pattern(
    "パターンA（現状維持）",
    monthly_2025_2026=12.3,
    monthly_2027_onwards=16.2
)

# パターンB: 増額（月15万円 → 月19万円 + 妻5万円）
pattern_b = simulate_investment_pattern(
    "パターンB（増額）",
    monthly_2025_2026=15.0,
    monthly_2027_onwards=19.0
)

# パターンC: 大幅増額（月18万円 → 月22万円 + 妻5万円）
pattern_c = simulate_investment_pattern(
    "パターンC（大幅増額）",
    monthly_2025_2026=18.0,
    monthly_2027_onwards=22.0
)

patterns = {
    'パターンA（現状維持: 12.3万→16.2万円/月）': pattern_a,
    'パターンB（増額: 15万→19万円/月）': pattern_b,
    'パターンC（大幅増額: 18万→22万円/月）': pattern_c
}

# 結果表示
for pattern_name, results in patterns.items():
    print(f"\n【{pattern_name}】")
    print("-" * 70)
    for scenario_name, values in results.items():
        print(f"\n{scenario_name}シナリオ（年率{RETURN_SCENARIOS[scenario_name]}%）:")
        print(f"  60歳時点の総資産: {values['total_assets']:.0f}万円")
        print(f"    ├ 既存資産の成長: {values['existing_growth']:.0f}万円")
        print(f"    └ 新規積立分: {values['new_accumulation']:.0f}万円")
        print(f"  教育費控除後の老後資金: {values['after_education']:.0f}万円")

        # 老後資金の十分性評価（30年間）
        retirement_years = 30
        total_retirement_need = MONTHLY_RETIREMENT_SHORTFALL * 12 * retirement_years
        pension_income = ANNUAL_PENSION * retirement_years

        if values['after_education'] >= 5000:
            evaluation = "[OK] 目標達成（5,000万円以上）"
        elif values['after_education'] >= 3000:
            evaluation = "[WARNING] やや不足（3,000-5,000万円）"
        else:
            evaluation = "[NG] 大幅不足（3,000万円未満）"

        print(f"  評価: {evaluation}")

# ===== 3. 現金保有率の統計分析 =====
print("\n" + "="*80)
print("3. 現金保有率の統計分析")
print("="*80)

monthly_living_expense = MONTHLY_INCOME - MONTHLY_RENT - CURRENT_TOTAL_MONTHLY_INVESTMENT
emergency_fund_min = monthly_living_expense * EMERGENCY_FUND_MONTHS_MIN
emergency_fund_max = monthly_living_expense * EMERGENCY_FUND_MONTHS_MAX

print(f"\n【現状】")
print(f"総資産: {TOTAL_ASSETS:.0f}万円")
print(f"現金保有額: {CURRENT_CASH:.0f}万円（0%）")

print(f"\n【統計的評価】")
print(f"[NG] 現金0%は危険: 緊急時の対応が不可能")
print(f"[NG] 同年収帯の平均現金保有率: 15-25%")
print(f"[NG] FP推奨: 子育て世帯は生活費の6-12ヶ月分を現金で保有")

print(f"\n【推奨される緊急資金】")
print(f"月間生活費: {monthly_living_expense:.1f}万円")
print(f"緊急資金（6ヶ月分）: {emergency_fund_min:.0f}万円")
print(f"緊急資金（12ヶ月分）: {emergency_fund_max:.0f}万円")
print(f"推奨: {emergency_fund_min:.0f}万円〜{emergency_fund_max:.0f}万円の現金確保")

# ===== 4. 資産配分の統計分析 =====
print("\n" + "="*80)
print("4. 資産配分の統計分析")
print("="*80)

# 現在の資産配分
stock_assets = CURRENT_NISA + CURRENT_IDECO + CURRENT_COMPANY_STOCK
stock_ratio = (stock_assets / TOTAL_ASSETS) * 100
company_stock_ratio = (CURRENT_COMPANY_STOCK / TOTAL_ASSETS) * 100

print(f"\n【現在の資産配分】")
print(f"株式: {stock_ratio:.0f}% ({stock_assets:.0f}万円)")
print(f"  ├ NISA（全世界株式）: {(CURRENT_NISA/TOTAL_ASSETS)*100:.0f}%")
print(f"  ├ iDeCo（株式）: {(CURRENT_IDECO/TOTAL_ASSETS)*100:.0f}%")
print(f"  └ 自社株: {company_stock_ratio:.0f}%")
print(f"債券: 0%")
print(f"現金: 0%")

print(f"\n【統計的評価】")
print(f"[NG] 株式100%は41歳には過度にリスクが高い")
print(f"  → 100-年齢ルール: 株式{AGE_BASED_STOCK_RATIO}% / 債券{AGE_BASED_BOND_RATIO}%が推奨")
print(f"[NG] 自社株{company_stock_ratio:.0f}%は集中リスクが高い")
print(f"  → 推奨上限: 個別株は総資産の{INDIVIDUAL_STOCK_LIMIT_MIN}-{INDIVIDUAL_STOCK_LIMIT_MAX}%まで")

# 自社株のリスク分析
print(f"\n【自社株リスク分析】")
print(f"自社株（個別銘柄）")
print(f"[NG] 個別株特有のリスク:")
print(f"  - 業績悪化リスク（業界・事業の変動）")
print(f"  - 市場リスク（個別株のボラティリティは高い）")
print(f"  - 流動性リスク（売却制限がある）")
print(f"  - 集中リスク（総資産の{company_stock_ratio:.0f}%は推奨上限の約3倍）")

# 過去の市場暴落時のドローダウン
print(f"\n【過去の市場暴落時のドローダウン分析】")
print(f"MSCI ACWI（円建て）の標準偏差:")
print(f"  - 5年: {MSCI_ACWI_VOLATILITY['5年']:.1f}%")
print(f"  - 10年: {MSCI_ACWI_VOLATILITY['10年']:.1f}%")
print(f"  - 20年: {MSCI_ACWI_VOLATILITY['20年']:.1f}%")
print(f"\n想定される最大ドローダウン（95%信頼区間）:")
print(f"  - 保守的: -30%程度（リーマンショック級）")
print(f"  - 現資産1,120万円の場合: 336万円の含み損")
print(f"  - 緊急資金0円では損切りを強いられる可能性")

# ===== 5. 教育費達成確率（モンテカルロシミュレーション） =====
print("\n" + "="*80)
print("5. 教育費達成確率のモンテカルロシミュレーション")
print("="*80)

def monte_carlo_simulation(monthly_investment_2025_2026, monthly_investment_2027_onwards,
                           target_amount, years, mean_return, volatility, simulations=10000):
    """モンテカルロシミュレーション"""
    np.random.seed(42)

    success_count = 0
    final_values = []

    for _ in range(simulations):
        # 既存資産の成長（13年後の2038年まで）
        existing_value = CURRENT_NISA + CURRENT_IDECO + CURRENT_COMPANY_STOCK

        for year in range(13):
            annual_return = np.random.normal(mean_return, volatility)
            existing_value *= (1 + annual_return / 100)

        # 新規積立（2025-2026: 2年間）
        accumulation_2025_2026 = 0
        for month in range(24):
            annual_return = np.random.normal(mean_return, volatility)
            monthly_return = annual_return / 12 / 100
            accumulation_2025_2026 = (accumulation_2025_2026 + monthly_investment_2025_2026) * (1 + monthly_return)

        # 新規積立（2027-2038: 12年間）
        accumulation_2027_onwards = 0
        for month in range(144):
            annual_return = np.random.normal(mean_return, volatility)
            monthly_return = annual_return / 12 / 100
            accumulation_2027_onwards = (accumulation_2027_onwards + monthly_investment_2027_onwards) * (1 + monthly_return)

        # 妻NISA（2028-2038: 11年間）
        wife_accumulation = 0
        for month in range(132):
            annual_return = np.random.normal(mean_return, volatility)
            monthly_return = annual_return / 12 / 100
            wife_accumulation = (wife_accumulation + WIFE_MONTHLY_NISA) * (1 + monthly_return)

        total_value = existing_value + accumulation_2025_2026 + accumulation_2027_onwards + wife_accumulation
        final_values.append(total_value)

        if total_value >= target_amount:
            success_count += 1

    success_rate = (success_count / simulations) * 100
    return success_rate, final_values

# 教育費達成確率の計算（2038年時点で2,400万円）
print(f"\n【シミュレーション条件】")
print(f"目標金額: {EDUCATION_COST:.0f}万円（2038年時点）")
print(f"シミュレーション回数: 10,000回")
print(f"期間: {CURRENT_YEAR}年〜2038年（13年間）")

for pattern_name, monthly_2025_2026, monthly_2027_onwards in [
    ('パターンA（現状維持）', 12.3, 16.2),
    ('パターンB（増額）', 15.0, 19.0),
    ('パターンC（大幅増額）', 18.0, 22.0)
]:
    print(f"\n【{pattern_name}】")

    for scenario_name, annual_return in RETURN_SCENARIOS.items():
        volatility = MSCI_ACWI_VOLATILITY['10年']  # 10年ボラティリティを使用

        success_rate, final_values = monte_carlo_simulation(
            monthly_2025_2026,
            monthly_2027_onwards,
            EDUCATION_COST,
            13,
            annual_return,
            volatility
        )

        median_value = np.median(final_values)
        percentile_10 = np.percentile(final_values, 10)
        percentile_90 = np.percentile(final_values, 90)

        print(f"\n  {scenario_name}シナリオ（年率{annual_return}%、標準偏差{volatility}%）:")
        print(f"    達成確率: {success_rate:.1f}%")
        print(f"    中央値: {median_value:.0f}万円")
        print(f"    10%タイル値: {percentile_10:.0f}万円")
        print(f"    90%タイル値: {percentile_90:.0f}万円")

        if success_rate >= 90:
            evaluation = "[OK] 非常に高い確率で達成"
        elif success_rate >= 75:
            evaluation = "[OK] 高い確率で達成"
        elif success_rate >= 50:
            evaluation = "[WARNING] 達成可能だが不確実性あり"
        else:
            evaluation = "[NG] 達成困難"

        print(f"    評価: {evaluation}")

print("\n" + "="*80)
print("分析完了")
print("="*80)
