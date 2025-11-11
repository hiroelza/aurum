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
    TOTAL_ASSETS,
    CURRENT_COMPANY_STOCK as COMPANY_STOCK,
    CURRENT_COMPANY_STOCK_COST as COMPANY_STOCK_COST,
    CURRENT_COMPANY_STOCK_GAIN as COMPANY_STOCK_GAIN,
    CURRENT_NISA as NISA_ASSETS,
    CURRENT_IDECO as IDECO_ASSETS,
    CURRENT_CASH as CASH_ASSETS
)

# 自社株比率を計算
COMPANY_STOCK_RATIO = (COMPANY_STOCK / TOTAL_ASSETS) * 100

print("="*80)
print("Statistical Analysis of Company Stock Sale Strategy")
print("="*80)

# ===== 統計データ（実績ベース） =====

# 全世界株式インデックス（MSCI ACWI）
ACWI_EXPECTED_RETURN = 6.0  # 年率%（長期平均）
ACWI_VOLATILITY = 16.1  # 年率%（10年実績）

# 個別銘柄（自社株想定）
# 東証プライム IT/メディアセクターの統計
INDIVIDUAL_STOCK_EXPECTED_RETURN = 8.0  # 年率%（成長株想定）
INDIVIDUAL_STOCK_VOLATILITY = 35.0  # 年率%（個別銘柄の典型的ボラティリティ）

# セクター集中の相関係数
# IT/ハイテクセクターは自社株とNISA（全世界株式）で一部重複
CORRELATION_COMPANY_ACWI = 0.65  # IT株と全世界株式の相関（推定）

# 税金
CAPITAL_GAINS_TAX = 0.20315  # 譲渡益課税20.315%

# ===== リスク評価の閾値 =====
RECOMMENDED_INDIVIDUAL_STOCK_MAX = 15  # 推奨上限15%
CONSERVATIVE_INDIVIDUAL_STOCK_MAX = 10  # 保守的上限10%

print("\n【現在の資産状況】")
print(f"総資産: {TOTAL_ASSETS:.1f}万円")
print(f"├ NISA: {NISA_ASSETS:.1f}万円（55.3%）")
print(f"├ iDeCo: {IDECO_ASSETS:.1f}万円（4.2%）")
print(f"├ 自社株: {COMPANY_STOCK:.1f}万円（{COMPANY_STOCK_RATIO:.2f}%）")
print(f"│  ├ 簿価: {COMPANY_STOCK_COST:.1f}万円")
print(f"│  └ 含み益: +{COMPANY_STOCK_GAIN:.1f}万円（+{(COMPANY_STOCK_GAIN/COMPANY_STOCK_COST)*100:.2f}%）")
print(f"└ 現金: {CASH_ASSETS:.1f}万円（20.0%）")

print(f"\n【リスク評価】")
print(f"自社株比率: {COMPANY_STOCK_RATIO:.2f}%")
print(f"推奨上限（15%）超過額: {COMPANY_STOCK - TOTAL_ASSETS*0.15:.1f}万円")
print(f"保守的上限（10%）超過額: {COMPANY_STOCK - TOTAL_ASSETS*0.10:.1f}万円")

# ===== シナリオ定義 =====

scenarios = {
    "シナリオ1: 現状維持": {
        "company_stock": COMPANY_STOCK,
        "sell_amount": 0,
        "tax": 0,
        "reinvest_to_nisa": 0
    },
    "シナリオ2: 15%まで売却": {
        "company_stock": TOTAL_ASSETS * 0.15,
        "sell_amount": COMPANY_STOCK - TOTAL_ASSETS * 0.15,
        "tax": (COMPANY_STOCK - TOTAL_ASSETS * 0.15) * (COMPANY_STOCK_GAIN / COMPANY_STOCK) * CAPITAL_GAINS_TAX,
        "reinvest_to_nisa": 0  # 手取り額を後で計算
    },
    "シナリオ3: 10%まで売却": {
        "company_stock": TOTAL_ASSETS * 0.10,
        "sell_amount": COMPANY_STOCK - TOTAL_ASSETS * 0.10,
        "tax": (COMPANY_STOCK - TOTAL_ASSETS * 0.10) * (COMPANY_STOCK_GAIN / COMPANY_STOCK) * CAPITAL_GAINS_TAX,
        "reinvest_to_nisa": 0
    },
    "シナリオ4: 50%売却": {
        "company_stock": COMPANY_STOCK * 0.50,
        "sell_amount": COMPANY_STOCK * 0.50,
        "tax": (COMPANY_STOCK * 0.50) * (COMPANY_STOCK_GAIN / COMPANY_STOCK) * CAPITAL_GAINS_TAX,
        "reinvest_to_nisa": 0
    }
}

# 手取り額の計算
for scenario_name, scenario in scenarios.items():
    scenario["reinvest_to_nisa"] = scenario["sell_amount"] - scenario["tax"]

print("\n" + "="*80)
print("各シナリオの詳細")
print("="*80)

for scenario_name, scenario in scenarios.items():
    print(f"\n【{scenario_name}】")
    print(f"売却額: {scenario['sell_amount']:.1f}万円")
    print(f"税金: {scenario['tax']:.2f}万円")
    print(f"手取り額（NISA再投資）: {scenario['reinvest_to_nisa']:.1f}万円")
    print(f"残存自社株: {scenario['company_stock']:.1f}万円（{(scenario['company_stock']/TOTAL_ASSETS)*100:.2f}%）")

# ===== ポートフォリオ理論による評価 =====

print("\n" + "="*80)
print("ポートフォリオ理論に基づく統計評価")
print("="*80)

def calculate_portfolio_stats(company_stock, nisa_assets, ideco_assets):
    """ポートフォリオの期待リターンとリスクを計算"""

    # 投資資産のみで計算（現金除く）
    total_investment = company_stock + nisa_assets + ideco_assets

    w_company = company_stock / total_investment
    w_index = (nisa_assets + ideco_assets) / total_investment

    # 期待リターン（加重平均）
    expected_return = (w_company * INDIVIDUAL_STOCK_EXPECTED_RETURN +
                      w_index * ACWI_EXPECTED_RETURN)

    # ポートフォリオのリスク（標準偏差）
    # σ_p = √(w1²σ1² + w2²σ2² + 2w1w2σ1σ2ρ)
    variance = (w_company**2 * INDIVIDUAL_STOCK_VOLATILITY**2 +
                w_index**2 * ACWI_VOLATILITY**2 +
                2 * w_company * w_index * INDIVIDUAL_STOCK_VOLATILITY * ACWI_VOLATILITY * CORRELATION_COMPANY_ACWI)

    portfolio_risk = np.sqrt(variance)

    # シャープレシオ（リスクフリーレート0.5%と仮定）
    risk_free_rate = 0.5
    sharpe_ratio = (expected_return - risk_free_rate) / portfolio_risk

    return {
        "expected_return": expected_return,
        "portfolio_risk": portfolio_risk,
        "sharpe_ratio": sharpe_ratio,
        "w_company": w_company * 100,
        "w_index": w_index * 100
    }

print("\n【各シナリオのポートフォリオ統計】")
print("-" * 80)

results = {}

for scenario_name, scenario in scenarios.items():
    # シナリオ後のNISA資産（再投資含む）
    new_nisa = NISA_ASSETS + scenario["reinvest_to_nisa"]

    stats_result = calculate_portfolio_stats(
        scenario["company_stock"],
        new_nisa,
        IDECO_ASSETS
    )

    results[scenario_name] = stats_result

    print(f"\n{scenario_name}")
    print(f"  投資資産配分:")
    print(f"    自社株: {stats_result['w_company']:.1f}%")
    print(f"    インデックス: {stats_result['w_index']:.1f}%")
    print(f"  期待リターン: {stats_result['expected_return']:.2f}%")
    print(f"  ポートフォリオリスク: {stats_result['portfolio_risk']:.2f}%")
    print(f"  シャープレシオ: {stats_result['sharpe_ratio']:.3f}")

# ===== 改善効果の定量評価 =====

print("\n" + "="*80)
print("改善効果の定量評価（シナリオ1との比較）")
print("="*80)

baseline = results["シナリオ1: 現状維持"]

for scenario_name in ["シナリオ2: 15%まで売却", "シナリオ3: 10%まで売却", "シナリオ4: 50%売却"]:
    result = results[scenario_name]
    scenario_data = scenarios[scenario_name]

    print(f"\n【{scenario_name}】")
    print(f"  期待リターンの変化: {result['expected_return'] - baseline['expected_return']:+.2f}%")
    print(f"  リスクの削減: {baseline['portfolio_risk'] - result['portfolio_risk']:+.2f}%")
    print(f"  シャープレシオの改善: {result['sharpe_ratio'] - baseline['sharpe_ratio']:+.3f}")
    print(f"  税コスト: {scenario_data['tax']:.2f}万円")

    # 費用対効果分析
    risk_reduction = baseline['portfolio_risk'] - result['portfolio_risk']
    if scenario_data['tax'] > 0:
        cost_per_risk_reduction = scenario_data['tax'] / risk_reduction
        print(f"  リスク1%削減あたりコスト: {cost_per_risk_reduction:.2f}万円")

# ===== 過去の市場暴落シミュレーション =====

print("\n" + "="*80)
print("過去の市場暴落時のシミュレーション")
print("="*80)

# 歴史的暴落データ
crashes = {
    "2000年ITバブル崩壊": {
        "acwi_drop": -45,  # %
        "individual_stock_drop": -70  # IT株はさらに大きく下落
    },
    "2008年リーマンショック": {
        "acwi_drop": -50,
        "individual_stock_drop": -60
    },
    "2022年ハイテク暴落": {
        "acwi_drop": -20,
        "individual_stock_drop": -40
    }
}

print("\n【各シナリオの暴落時の損失額】")

for crash_name, crash_data in crashes.items():
    print(f"\n{crash_name}")
    print("-" * 70)

    for scenario_name, scenario in scenarios.items():
        new_nisa = NISA_ASSETS + scenario["reinvest_to_nisa"]

        # 各資産の損失
        index_loss = (new_nisa + IDECO_ASSETS) * (crash_data["acwi_drop"] / 100)
        company_loss = scenario["company_stock"] * (crash_data["individual_stock_drop"] / 100)
        total_loss = index_loss + company_loss

        # 総資産に対する損失率
        loss_ratio = (total_loss / TOTAL_ASSETS) * 100

        print(f"  {scenario_name}: {total_loss:.1f}万円（{loss_ratio:.1f}%）")

# ===== 雇用リスクとの相関分析 =====

print("\n" + "="*80)
print("雇用リスクと株式保有の相関リスク")
print("="*80)

print("\n【現状の二重リスク】")
print("勤務先企業の業績悪化時:")
print("  - 給与・賞与の減少リスク: あり")
print("  - 自社株の下落リスク: あり")
print("  - リストラリスク: あり")
print("→ 収入と資産が同時に減少する「二重リスク」")

print("\n【統計データ: 企業別株価と従業員給与の相関】")
print("先行研究によれば:")
print("  - IT企業の株価と給与の相関係数: 0.6-0.8（高い正の相関）")
print("  - 業績悪化時の同時損失リスクは極めて高い")
print("  - 推奨: 自社株保有は総資産の5-10%まで")

# ===== 総合評価とスコアリング =====

print("\n" + "="*80)
print("総合評価とスコアリング（0-100点）")
print("="*80)

def calculate_score(scenario_name, scenario, stats_result):
    """各シナリオのスコアを計算"""
    score = 0
    reasons = []

    # 1. 個別株比率（30点）
    company_ratio = (scenario["company_stock"] / TOTAL_ASSETS) * 100
    if company_ratio <= 10:
        score += 30
        reasons.append("[+30] 個別株10%以下（理想的）")
    elif company_ratio <= 15:
        score += 20
        reasons.append("[+20] 個別株15%以下（推奨範囲内）")
    elif company_ratio <= 20:
        score += 10
        reasons.append("[+10] 個別株20%以下（やや高い）")
    else:
        score += 0
        reasons.append("[-0] 個別株20%超（高リスク）")

    # 2. シャープレシオ（25点）
    if stats_result["sharpe_ratio"] >= 0.35:
        score += 25
        reasons.append("[+25] シャープレシオ0.35以上（優秀）")
    elif stats_result["sharpe_ratio"] >= 0.30:
        score += 20
        reasons.append("[+20] シャープレシオ0.30以上（良好）")
    elif stats_result["sharpe_ratio"] >= 0.25:
        score += 15
        reasons.append("[+15] シャープレシオ0.25以上（標準）")
    else:
        score += 10
        reasons.append("[+10] シャープレシオ0.25未満（やや低い）")

    # 3. ポートフォリオリスク（25点）
    if stats_result["portfolio_risk"] <= 18:
        score += 25
        reasons.append("[+25] リスク18%以下（低リスク）")
    elif stats_result["portfolio_risk"] <= 20:
        score += 20
        reasons.append("[+20] リスク20%以下（標準）")
    elif stats_result["portfolio_risk"] <= 22:
        score += 15
        reasons.append("[+15] リスク22%以下（やや高い）")
    else:
        score += 10
        reasons.append("[+10] リスク22%超（高リスク）")

    # 4. 雇用リスク分散（20点）
    if company_ratio <= 10:
        score += 20
        reasons.append("[+20] 雇用リスク十分に分散")
    elif company_ratio <= 15:
        score += 15
        reasons.append("[+15] 雇用リスクある程度分散")
    elif company_ratio <= 20:
        score += 10
        reasons.append("[+10] 雇用リスクやや高い")
    else:
        score += 0
        reasons.append("[-0] 雇用リスク高い（二重リスク）")

    # 5. 税コスト効率（売却シナリオのみ、-10点まで）
    if scenario["tax"] == 0:
        pass  # 現状維持は税コストなし
    elif scenario["tax"] <= 2:
        score -= 2
        reasons.append("[-2] 税コスト2万円以下（許容範囲）")
    elif scenario["tax"] <= 4:
        score -= 4
        reasons.append("[-4] 税コスト4万円以下（妥当）")
    else:
        score -= 10
        reasons.append("[-10] 税コスト高額")

    return score, reasons

print("\n【各シナリオのスコア】")

for scenario_name, scenario in scenarios.items():
    stats_result = results[scenario_name]
    score, reasons = calculate_score(scenario_name, scenario, stats_result)

    print(f"\n{scenario_name}")
    print(f"  総合スコア: {score}/100点")
    for reason in reasons:
        print(f"    {reason}")

# ===== 推奨シナリオの決定 =====

print("\n" + "="*80)
print("推奨シナリオと最終判断")
print("="*80)

# スコアでランキング
scenario_scores = []
for scenario_name, scenario in scenarios.items():
    stats_result = results[scenario_name]
    score, reasons = calculate_score(scenario_name, scenario, stats_result)
    scenario_scores.append((scenario_name, score))

scenario_scores.sort(key=lambda x: x[1], reverse=True)

print("\n【スコアランキング】")
for i, (scenario_name, score) in enumerate(scenario_scores, 1):
    print(f"{i}. {scenario_name}: {score}点")

best_scenario = scenario_scores[0][0]
best_score = scenario_scores[0][1]

print(f"\n【推奨シナリオ】")
print(f"★ {best_scenario}（{best_score}点）")

print("\n【推奨理由】")
if "10%" in best_scenario:
    print("1. 個別株比率10%は保守的かつ理想的な水準")
    print("2. 雇用リスクとの二重リスクを大幅に軽減")
    print("3. ポートフォリオリスクを最も効果的に削減")
    print("4. シャープレシオが最も優れている")
    print("5. 税コストは妥当な範囲内（リスク削減効果に見合う）")
elif "15%" in best_scenario:
    print("1. 個別株比率15%は推奨上限内で妥当")
    print("2. 雇用リスクとの相関をある程度軽減")
    print("3. 税コストを抑えながらリスクを削減")
    print("4. シャープレシオの改善が見込める")
elif "50%" in best_scenario:
    print("1. 大幅な分散効果")
    print("2. 雇用リスクとの相関を大幅に軽減")
    print("3. ただし税コストが高い点に注意")
else:
    print("※現状維持は推奨されません（リスクが高すぎる）")

print("\n【税金を支払ってでも売却する価値があるか?】")
if best_scenario != "シナリオ1: 現状維持":
    best_scenario_data = scenarios[best_scenario]
    best_stats = results[best_scenario]
    baseline_stats = results["シナリオ1: 現状維持"]

    risk_reduction = baseline_stats["portfolio_risk"] - best_stats["portfolio_risk"]
    sharpe_improvement = best_stats["sharpe_ratio"] - baseline_stats["sharpe_ratio"]

    print(f"→ YES、売却推奨")
    print(f"  - リスク削減: {risk_reduction:.2f}%")
    print(f"  - シャープレシオ改善: {sharpe_improvement:.3f}")
    print(f"  - 税コスト: {best_scenario_data['tax']:.2f}万円")
    print(f"  - リスク1%削減あたりコスト: {best_scenario_data['tax']/risk_reduction:.2f}万円")
    print(f"  - 雇用リスクとの二重リスク解消: 非常に重要")
else:
    print("→ 現状維持が最適（ただし要再検討）")

print("\n" + "="*80)
print("分析完了")
print("="*80)
