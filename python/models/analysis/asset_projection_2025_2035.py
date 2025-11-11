"""
60歳時点の資産予測シミュレーション（2025-2035年マクロ経済見通し対応）

ニッセイ基礎研究所「中期経済見通し（2025-2035年度）」に基づく資産予測
"""

import numpy as np
import pandas as pd

# ===== 基本パラメータ =====
CURRENT_YEAR = 2025
RETIREMENT_YEAR = 2044
YEARS_TO_RETIREMENT = RETIREMENT_YEAR - CURRENT_YEAR  # 19年

# 現在の資産（万円）
CURRENT_NISA = [NISA_ASSETS]  # 個人設定から読み込んでください
CURRENT_IDECO = [IDECO_ASSETS]  # 個人設定から読み込んでください
CURRENT_INVESTMENT_TOTAL = CURRENT_NISA + CURRENT_IDECO  # 891.4万円

# 月次積立額（万円）
MONTHLY_NISA_2025 = 10.0
MONTHLY_IDECO_2025 = 2.3
MONTHLY_TOTAL_2025 = MONTHLY_NISA_2025 + MONTHLY_IDECO_2025  # 12.3万円

# 2027年以降（iDeCo増額）
MONTHLY_IDECO_2027 = 6.2
MONTHLY_TOTAL_2027 = MONTHLY_NISA_2025 + MONTHLY_IDECO_2027  # 16.2万円

# マクロ経済前提
INFLATION_RATE_OLD = 1.7 / 100  # 旧：1.7%
INFLATION_RATE_NEW = 2.0 / 100  # 新：2.0%

# 名目リターンシナリオ
NOMINAL_RETURN_CONSERVATIVE = 5.0 / 100  # 5%
NOMINAL_RETURN_NEUTRAL = 6.0 / 100        # 6%
NOMINAL_RETURN_OPTIMISTIC = 7.0 / 100     # 7%

# ===== 関数定義 =====

def calculate_future_value(current_assets, monthly_contribution, years, annual_return):
    """
    複利計算による将来価値の算出

    Parameters:
    - current_assets: 現在の資産額（万円）
    - monthly_contribution: 月次積立額（万円）
    - years: 運用年数
    - annual_return: 年間リターン率（小数）

    Returns:
    - 将来価値（万円）
    """
    # 現在資産の複利計算
    future_value_current = current_assets * ((1 + annual_return) ** years)

    # 月次積立の複利計算（年複利に変換）
    monthly_rate = (1 + annual_return) ** (1/12) - 1
    months = years * 12

    if monthly_rate > 0:
        future_value_contributions = monthly_contribution * (((1 + monthly_rate) ** months - 1) / monthly_rate)
    else:
        future_value_contributions = monthly_contribution * months

    return future_value_current + future_value_contributions


def calculate_with_schedule(current_assets, scenario_return, inflation_rate):
    """
    積立スケジュールを考慮した資産予測

    2025-2026: 月12.3万円
    2027-2044: 月16.2万円（iDeCo増額）
    """
    assets = current_assets

    # Phase 1: 2025-2026（2年間、月12.3万円）
    years_phase1 = 2
    assets = calculate_future_value(assets, MONTHLY_TOTAL_2025, years_phase1, scenario_return)

    # Phase 2: 2027-2044（17年間、月16.2万円）
    years_phase2 = YEARS_TO_RETIREMENT - years_phase1
    assets = calculate_future_value(assets, MONTHLY_TOTAL_2027, years_phase2, scenario_return)

    # 実質価値への変換（インフレ調整）
    real_assets = assets / ((1 + inflation_rate) ** YEARS_TO_RETIREMENT)

    return {
        'nominal': assets,
        'real': real_assets,
        'inflation_multiplier': (1 + inflation_rate) ** YEARS_TO_RETIREMENT
    }


# ===== メイン計算 =====

print("="*80)
print("60歳時点の資産予測シミュレーション")
print("="*80)
print(f"\n現在の資産: {CURRENT_INVESTMENT_TOTAL:,.1f}万円")
print(f"月次積立: {MONTHLY_TOTAL_2025:,.1f}万円（2025-2026）")
print(f"月次積立: {MONTHLY_TOTAL_2027:,.1f}万円（2027-2044、iDeCo増額後）")
print(f"運用期間: {YEARS_TO_RETIREMENT}年")

# 旧前提（インフレ率1.7%）
print("\n" + "="*80)
print("旧前提（2024-2034年見通し、インフレ率1.7%）")
print("="*80)

scenarios_old = {}
for name, nominal_return in [('保守的', NOMINAL_RETURN_CONSERVATIVE),
                              ('中立的', NOMINAL_RETURN_NEUTRAL),
                              ('楽観的', NOMINAL_RETURN_OPTIMISTIC)]:
    real_return_old = nominal_return - INFLATION_RATE_OLD
    result = calculate_with_schedule(CURRENT_INVESTMENT_TOTAL, nominal_return, INFLATION_RATE_OLD)
    scenarios_old[name] = result

    print(f"\n【{name}シナリオ】")
    print(f"  名目リターン: {nominal_return*100:.1f}%")
    print(f"  実質リターン: {real_return_old*100:.1f}%")
    print(f"  資産（実質）: {result['real']:,.0f}万円")
    print(f"  資産（名目）: {result['nominal']:,.0f}万円")

# 新前提（インフレ率2.0%）
print("\n" + "="*80)
print("新前提（2025-2035年見通し、インフレ率2.0%）")
print("="*80)

scenarios_new = {}
for name, nominal_return in [('保守的', NOMINAL_RETURN_CONSERVATIVE),
                              ('中立的', NOMINAL_RETURN_NEUTRAL),
                              ('楽観的', NOMINAL_RETURN_OPTIMISTIC)]:
    real_return_new = nominal_return - INFLATION_RATE_NEW
    result = calculate_with_schedule(CURRENT_INVESTMENT_TOTAL, nominal_return, INFLATION_RATE_NEW)
    scenarios_new[name] = result

    print(f"\n【{name}シナリオ】")
    print(f"  名目リターン: {nominal_return*100:.1f}%")
    print(f"  実質リターン: {real_return_new*100:.1f}%")
    print(f"  資産（実質）: {result['real']:,.0f}万円")
    print(f"  資産（名目）: {result['nominal']:,.0f}万円")

# 比較
print("\n" + "="*80)
print("新旧比較（実質ベース）")
print("="*80)

for name in ['保守的', '中立的', '楽観的']:
    old_real = scenarios_old[name]['real']
    new_real = scenarios_new[name]['real']
    diff = new_real - old_real
    diff_pct = (diff / old_real) * 100

    print(f"\n【{name}シナリオ】")
    print(f"  旧: {old_real:,.0f}万円")
    print(f"  新: {new_real:,.0f}万円")
    print(f"  差分: {diff:+,.0f}万円（{diff_pct:+.1f}%）")

# サマリーテーブル作成
print("\n" + "="*80)
print("サマリーテーブル（新前提：2025-2035年）")
print("="*80)

data = []
for name, nominal_return in [('保守的', NOMINAL_RETURN_CONSERVATIVE),
                              ('中立的', NOMINAL_RETURN_NEUTRAL),
                              ('楽観的', NOMINAL_RETURN_OPTIMISTIC)]:
    real_return = nominal_return - INFLATION_RATE_NEW
    result = scenarios_new[name]

    data.append({
        'シナリオ': name,
        '名目リターン': f"{nominal_return*100:.1f}%",
        '実質リターン': f"{real_return*100:.1f}%",
        '資産（実質）': f"{result['real']:,.0f}万円",
        '資産（名目）': f"{result['nominal']:,.0f}万円"
    })

df = pd.DataFrame(data)
print("\n", df.to_string(index=False))

# 目標達成確認
print("\n" + "="*80)
print("目標達成確認")
print("="*80)

TARGET_RETIREMENT = 5000  # 万円

for name in ['保守的', '中立的', '楽観的']:
    real_assets = scenarios_new[name]['real']
    surplus = real_assets - TARGET_RETIREMENT

    if surplus >= 0:
        status = "✅ 達成"
    else:
        status = "❌ 未達"

    print(f"{name}: {real_assets:,.0f}万円（目標5,000万円）→ {status}（{surplus:+,.0f}万円）")

# 教育費の名目額計算
print("\n" + "="*80)
print("教育費の名目額計算")
print("="*80)

EDUCATION_REAL = 2400  # 実質2,400万円（1,200万円×2人）
YEARS_TO_DAUGHTER = 2038 - 2025  # 13年
YEARS_TO_SON = 2040 - 2025  # 15年

daughter_nominal_old = EDUCATION_REAL / 2 * ((1 + INFLATION_RATE_OLD) ** YEARS_TO_DAUGHTER)
son_nominal_old = EDUCATION_REAL / 2 * ((1 + INFLATION_RATE_OLD) ** YEARS_TO_SON)
total_old = daughter_nominal_old + son_nominal_old

daughter_nominal_new = EDUCATION_REAL / 2 * ((1 + INFLATION_RATE_NEW) ** YEARS_TO_DAUGHTER)
son_nominal_new = EDUCATION_REAL / 2 * ((1 + INFLATION_RATE_NEW) ** YEARS_TO_SON)
total_new = daughter_nominal_new + son_nominal_new

print(f"\n実質ベース: {EDUCATION_REAL:,.0f}万円（各{EDUCATION_REAL/2:,.0f}万円）")
print(f"\n旧前提（インフレ1.7%）:")
print(f"  第1子: {daughter_nominal_old:,.0f}万円")
print(f"  第2子: {son_nominal_old:,.0f}万円")
print(f"  合計: {total_old:,.0f}万円")

print(f"\n新前提（インフレ2.0%）:")
print(f"  第1子: {daughter_nominal_new:,.0f}万円")
print(f"  第2子: {son_nominal_new:,.0f}万円")
print(f"  合計: {total_new:,.0f}万円")

print(f"\n差分: {total_new - total_old:+,.0f}万円（{((total_new - total_old) / total_old * 100):+.1f}%）")

print("\n" + "="*80)
print("シミュレーション完了")
print("="*80)
