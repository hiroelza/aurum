#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Japanese Stocks Statistical Analysis
日本株式の統計分析とシミュレーション
"""

import pandas as pd
import numpy as np
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print("="*100)
print("日本株式の統計分析とシミュレーション")
print("作成日: 2025年11月1日")
print("="*100)

# ===== 1. PER/PBRの統計分析 =====
print("\n" + "="*100)
print("1. バリュエーション指標の統計分析")
print("="*100)

# 半導体セクターのバリュエーション
semiconductor_valuations = {
    '銘柄': ['東京エレクトロン', 'レーザーテック', 'ソシオネクスト'],
    'PER': [35.27, 42.71, 58.69],
    'PBR': [8.43, 12.21, 4.78]
}

df_val = pd.DataFrame(semiconductor_valuations)

print("\n【半導体セクターのバリュエーション統計】")
print("-" * 80)
print(f"PER平均: {df_val['PER'].mean():.1f}倍")
print(f"PER中央値: {df_val['PER'].median():.1f}倍")
print(f"PER標準偏差: {df_val['PER'].std():.1f}倍")
print(f"PER最大値: {df_val['PER'].max():.1f}倍（ソシオネクスト）")
print(f"PER最小値: {df_val['PER'].min():.1f}倍（東京エレクトロン）")
print(f"\nPBR平均: {df_val['PBR'].mean():.2f}倍")
print(f"PBR中央値: {df_val['PBR'].median():.2f}倍")
print(f"PBR標準偏差: {df_val['PBR'].std():.2f}倍")

print("\n【統計的評価】")
print("-" * 80)
print(f"PER > 40倍: 市場平均(20-25倍)の1.5-2倍以上")
print(f"  → 超成長を織り込んでいるが、調整リスク高い")
print(f"\nPBR > 10倍: 日本株平均(1.1-1.3倍)の8-10倍")
print(f"  → 異常に高いバリュエーション")
print(f"  → レーザーテック(12.2倍)は特にリスク")

# ===== 2. 高配当株のリスク・リターン分析 =====
print("\n" + "="*100)
print("2. 高配当株の利回り分析")
print("="*100)

dividend_data = {
    '銘柄': ['日本たばこ', '三井住友FG', 'JFE鋼鉄', '住友化学'],
    '配当利回り': [7.5, 4.5, 4.2, 4.8],
    'セクター': ['消費財', '金融', '鉄鋼', '化学'],
    'ボラティリティ': [0.15, 0.18, 0.25, 0.20]  # 想定される年率変動率
}

df_div = pd.DataFrame(dividend_data)

print("\n【高配当株の利回り分析】")
print("-" * 80)
print(f"配当利回り平均: {df_div['配当利回り'].mean():.1f}%")
print(f"配当利回り中央値: {df_div['配当利回り'].median():.1f}%")
print(f"配当利回り範囲: {df_div['配当利回り'].min():.1f}% - {df_div['配当利回り'].max():.1f}%")

print("\n【セクター別の特性】")
print("-" * 80)
for sector in df_div['セクター'].unique():
    sector_data = df_div[df_div['セクター'] == sector]
    avg_yield = sector_data['配当利回り'].mean()
    avg_volatility = sector_data['ボラティリティ'].mean()
    print(f"{sector}: 利回り{avg_yield:.1f}%, ボラティリティ{avg_volatility:.0%}")

# ===== 3. リスク・リターン比較 =====
print("\n" + "="*100)
print("3. リスク・リターン比較（期待値分析）")
print("="*100)

print("\n【シナリオ別の期待リターン】")
print("-" * 80)

strategies = {
    'ポートフォリオ': ['成長重視', 'バランス型', 'インカム重視'],
    '期待リターン': [18, 12, 4.5],
    'ボラティリティ': [25, 15, 8],
    '最悪ケース': [-40, -20, -5],
    'ベストケース': [50, 35, 10]
}

df_strat = pd.DataFrame(strategies)

print("\n" + df_strat.to_string(index=False))

# リスク・リターン比の計算（シャープレシオ的な評価）
# 無リスク利率を2%と仮定
risk_free_rate = 2.0

print("\n【リスク調整後のリターン評価】")
print("-" * 80)

for idx, row in df_strat.iterrows():
    # シャープレシオ的な指標: (期待リターン - 無リスク利率) / ボラティリティ
    risk_adjusted = (row['期待リターン'] - risk_free_rate) / row['ボラティリティ']
    print(f"\n{row['ポートフォリオ']}")
    print(f"  期待リターン: {row['期待リターン']:.1f}%")
    print(f"  ボラティリティ: {row['ボラティリティ']:.0f}%")
    print(f"  リスク調整後: {risk_adjusted:.2f}")
    if risk_adjusted > 0.5:
        evaluation = "[推奨] バランスが良い"
    elif risk_adjusted > 0.3:
        evaluation = "[検討] 許容範囲"
    else:
        evaluation = "[注意] リスク高い"
    print(f"  評価: {evaluation}")

# ===== 4. モンテカルロシミュレーション =====
print("\n" + "="*100)
print("4. 1年後のリターン分布（モンテカルロシミュレーション）")
print("="*100)

np.random.seed(42)
simulations = 10000

print(f"\nシミュレーション回数: {simulations:,}回")

# 成長重視型のシミュレーション
print("\n【成長重視型（半導体2銘柄）】")
print("-" * 80)
growth_returns = np.random.normal(18, 25, simulations)  # 平均18%, 標準偏差25%
growth_positive = (growth_returns > 0).sum() / simulations * 100
growth_negative_20 = (growth_returns < -20).sum() / simulations * 100

print(f"平均リターン: {growth_returns.mean():.1f}%")
print(f"中央値: {np.median(growth_returns):.1f}%")
print(f"標準偏差: {growth_returns.std():.1f}%")
print(f"利益を得る確率: {growth_positive:.1f}%")
print(f"損失が-20%以下の確率: {growth_negative_20:.1f}%")
print(f"\nパーセンタイル:")
print(f"  10%タイル（悪い方から10%）: {np.percentile(growth_returns, 10):.1f}%")
print(f"  25%タイル: {np.percentile(growth_returns, 25):.1f}%")
print(f"  75%タイル: {np.percentile(growth_returns, 75):.1f}%")
print(f"  90%タイル（良い方から10%）: {np.percentile(growth_returns, 90):.1f}%")

# バランス型のシミュレーション
print("\n【バランス型（ルネサス + 日本たばこ）】")
print("-" * 80)
balanced_returns = np.random.normal(12, 15, simulations)  # 平均12%, 標準偏差15%
balanced_positive = (balanced_returns > 0).sum() / simulations * 100
balanced_negative_15 = (balanced_returns < -15).sum() / simulations * 100

print(f"平均リターン: {balanced_returns.mean():.1f}%")
print(f"中央値: {np.median(balanced_returns):.1f}%")
print(f"標準偏差: {balanced_returns.std():.1f}%")
print(f"利益を得る確率: {balanced_positive:.1f}%")
print(f"損失が-15%以下の確率: {balanced_negative_15:.1f}%")
print(f"\nパーセンタイル:")
print(f"  10%タイル: {np.percentile(balanced_returns, 10):.1f}%")
print(f"  25%タイル: {np.percentile(balanced_returns, 25):.1f}%")
print(f"  75%タイル: {np.percentile(balanced_returns, 75):.1f}%")
print(f"  90%タイル: {np.percentile(balanced_returns, 90):.1f}%")

# インカム重視型のシミュレーション
print("\n【インカム重視型（日本たばこ）】")
print("-" * 80)
income_returns = np.random.normal(4.5, 8, simulations)  # 平均4.5%, 標準偏差8%
income_positive = (income_returns > 0).sum() / simulations * 100
income_negative_10 = (income_returns < -10).sum() / simulations * 100

print(f"平均リターン: {income_returns.mean():.1f}%")
print(f"中央値: {np.median(income_returns):.1f}%")
print(f"標準偏差: {income_returns.std():.1f}%")
print(f"利益を得る確率: {income_positive:.1f}%")
print(f"損失が-10%以下の確率: {income_negative_10:.1f}%")
print(f"\nパーセンタイル:")
print(f"  10%タイル: {np.percentile(income_returns, 10):.1f}%")
print(f"  25%タイル: {np.percentile(income_returns, 25):.1f}%")
print(f"  75%タイル: {np.percentile(income_returns, 75):.1f}%")
print(f"  90%タイル: {np.percentile(income_returns, 90):.1f}%")

# ===== 5. 50万円投資の実例計算 =====
print("\n" + "="*100)
print("5. 50万円投資の1年後の資産予測")
print("="*100)

initial_capital = 500000

print("\n【成長重視型】")
print("-" * 80)
growth_1yr = initial_capital * (1 + growth_returns / 100)
print(f"期待資産額: {growth_1yr.mean():,.0f}円（＋{growth_1yr.mean() - initial_capital:,.0f}円）")
print(f"10%タイル（損失時）: {np.percentile(growth_1yr, 10):,.0f}円")
print(f"90%タイル（好調時）: {np.percentile(growth_1yr, 90):,.0f}円")
print(f"最悪ケース（1%タイル）: {np.percentile(growth_1yr, 1):,.0f}円")

print("\n【バランス型（推奨）】")
print("-" * 80)
balanced_1yr = initial_capital * (1 + balanced_returns / 100)
print(f"期待資産額: {balanced_1yr.mean():,.0f}円（＋{balanced_1yr.mean() - initial_capital:,.0f}円）")
print(f"10%タイル（損失時）: {np.percentile(balanced_1yr, 10):,.0f}円")
print(f"90%タイル（好調時）: {np.percentile(balanced_1yr, 90):,.0f}円")
print(f"最悪ケース（1%タイル）: {np.percentile(balanced_1yr, 1):,.0f}円")

print("\n【インカム重視型】")
print("-" * 80)
income_1yr = initial_capital * (1 + income_returns / 100)
print(f"期待資産額: {income_1yr.mean():,.0f}円（＋{income_1yr.mean() - initial_capital:,.0f}円）")
print(f"10%タイル（損失時）: {np.percentile(income_1yr, 10):,.0f}円")
print(f"90%タイル（好調時）: {np.percentile(income_1yr, 90):,.0f}円")
print(f"最悪ケース（1%タイル）: {np.percentile(income_1yr, 1):,.0f}円")

# ===== 6. 現状のポートフォリオ評価 =====
print("\n" + "="*100)
print("6. 現状のポートフォリオとの比較評価")
print("="*100)

print("\n【現在の資産構成】")
print("-" * 80)
print("NISA: [NISA_ASSETS]万円（全世界株式）")
print("iDeCo: [IDECO_ASSETS]万円（株式）")
print("自社株: [COMPANY_STOCK]万円")
print("現金: [CASH]万円")
print("合計: [TOTAL_ASSETS]万円")

print("\n【評価】")
print("-" * 80)
print("[OK] 全世界株式への投資: 分散が十分")
print("[WARNING] 自社株[COMPANY_STOCK]万円(21%): 推奨上限5-10%に対して過剰")
print("[NG] 現金[CASH]万円(21%): 保有比率は適正だが、配置が非効率")

print("\n【改善提案】")
print("-" * 80)
print("1. 現状の月12.3万円投資(NISA月10万円)を継続")
print("2. 2027年iDeCo増額(月6.2万円)で資金効率化")
print("3. 2028年妻NISA開始(月5万円)で投資範囲拡大")
print("4. 自社株の段階的売却（年30-50万円）で分散化")
print("5. 現金[CASH]万円は緊急資金として確保")

# ===== 7. 税制優遇の比較 =====
print("\n" + "="*100)
print("7. NISA制度の活用による税制優遇")
print("="*100)

print("\n【NISA（新）での投資効率化】")
print("-" * 80)
nisa_annual = 360 * 10000  # 年間360万円
nisa_20years = nisa_annual * 20  # 20年間の最大積立額

print(f"年間NISA枠: 360万円")
print(f"生涯非課税投資額（生涯枠）: 1,800万円")
print(f"20年間の最大積立: {nisa_20years:,}円")

# 配当と値上がり益の課税比較
dividend = 100000  # 10万円の配当
dividend_tax = dividend * 0.20315  # 源泉徴収税（20.315%）
dividend_nisa = 0  # NISA内は非課税

capital_gain = 500000  # 50万円の値上がり益
capital_tax = capital_gain * 0.20315
capital_nisa = 0

print(f"\n配当10万円の場合:")
print(f"  通常口座: 税金{dividend_tax:,.0f}円 → 手取り{dividend - dividend_tax:,.0f}円")
print(f"  NISA口座: 税金0円 → 手取り{dividend_nisa + dividend:,.0f}円")
print(f"  NISA利益: {dividend_tax:,.0f}円/年")

print(f"\n値上がり益50万円の場合:")
print(f"  通常口座: 税金{capital_tax:,.0f}円 → 手取り{capital_gain - capital_tax:,.0f}円")
print(f"  NISA口座: 税金0円 → 手取り{capital_nisa + capital_gain:,.0f}円")
print(f"  NISA利益: {capital_tax:,.0f}円/回")

print("\n" + "="*100)
print("統計分析完了")
print("="*100)
