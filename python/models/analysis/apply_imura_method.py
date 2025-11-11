#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
井村氏手法を1,091銘柄に適用

井村氏3基準:
1. 成長率÷PER ≧ 1.0
2. 配当利回り ≧ 3%
3. 5年以上連続増配（データなし、スキップ）
"""

import pandas as pd
import numpy as np

print("="*80)
print("井村氏手法適用 - 1,091銘柄（売上成長率データ付き）")
print("="*80)

# CSVを読み込み
input_csv = "./phase1_1100stocks_with_growth.csv"
print(f"\n📂 読み込み中: {input_csv}")
df = pd.read_csv(input_csv, encoding='utf-8-sig')
print(f"✅ 読み込み完了: {len(df)}銘柄")

# データ品質チェック
print(f"\n📊 データ品質:")
print(f"  PERデータあり: {df['pe_ratio'].notna().sum()}銘柄")
print(f"  売上成長率（3年平均）あり: {df['revenue_growth_3y'].notna().sum()}銘柄")
print(f"  配当利回りあり: {df['dividend_yield'].notna().sum()}銘柄")

# 成長率÷PERを計算
print(f"\n🔄 成長率÷PERを計算中...")
df['growth_per_ratio'] = df['revenue_growth_3y'] / df['pe_ratio']

# 井村氏手法の各基準をチェック
print(f"\n{'='*80}")
print("【基準1】成長率÷PER ≧ 1.0")
print(f"{'='*80}")

valid_data = df[(df['pe_ratio'].notna()) & (df['revenue_growth_3y'].notna())].copy()
print(f"有効データ: {len(valid_data)}銘柄（PERと成長率の両方あり）")

condition_growth_per = valid_data['growth_per_ratio'] >= 1.0
count_growth_per = condition_growth_per.sum()
print(f"✅ 該当銘柄数: {count_growth_per}銘柄 / {len(valid_data)}銘柄")
print(f"   比率: {count_growth_per/len(valid_data)*100:.1f}%")

if count_growth_per > 0:
    print(f"\n🏆 成長率÷PER TOP30:")
    print("-"*80)
    top30 = valid_data[condition_growth_per].nlargest(30, 'growth_per_ratio')
    for i, row in enumerate(top30.itertuples(), 1):
        market_flag = "🇯🇵" if row.market == "JP" else "🇺🇸"
        print(f"{i:2d}. {market_flag} {row.ticker:12s} {row.name[:35]:35s} "
              f"成長率{row.revenue_growth_3y:6.1f}% / PER{row.pe_ratio:5.1f} "
              f"= {row.growth_per_ratio:.2f}")

print(f"\n{'='*80}")
print("【基準2】配当利回り ≧ 3%")
print(f"{'='*80}")

# 配当利回りが100倍されている（167.0 = 1.67%）
condition_dividend = df['dividend_yield'] >= 300
count_dividend = condition_dividend.sum()
print(f"✅ 該当銘柄数: {count_dividend}銘柄 / {len(df)}銘柄")
print(f"   比率: {count_dividend/len(df)*100:.1f}%")

print(f"\n{'='*80}")
print("【複合条件】成長率÷PER ≧ 1.0 AND 配当利回り ≧ 3%")
print(f"{'='*80}")

# 複合条件
imura_qualified = df[
    (df['growth_per_ratio'] >= 1.0) &
    (df['dividend_yield'] >= 300) &
    (df['pe_ratio'].notna()) &
    (df['revenue_growth_3y'].notna())
].copy()

count_imura = len(imura_qualified)
print(f"✅ 井村氏手法該当銘柄: {count_imura}銘柄 / {len(df)}銘柄")
print(f"   比率: {count_imura/len(df)*100:.1f}%")

if count_imura > 0:
    # 市場別内訳
    print(f"\n📊 市場別内訳:")
    print(f"  日本株: {len(imura_qualified[imura_qualified['market']=='JP'])}銘柄")
    print(f"  米国株: {len(imura_qualified[imura_qualified['market']=='US'])}銘柄")

    # ソート（成長率÷PERの降順）
    imura_qualified = imura_qualified.sort_values('growth_per_ratio', ascending=False)

    print(f"\n🏆 井村氏手法該当銘柄TOP30:")
    print("-"*80)
    for i, row in enumerate(imura_qualified.head(30).itertuples(), 1):
        market_flag = "🇯🇵" if row.market == "JP" else "🇺🇸"
        div_pct = row.dividend_yield / 100
        print(f"{i:2d}. {market_flag} {row.ticker:12s} {row.name[:30]:30s} "
              f"成長{row.revenue_growth_3y:5.1f}%/PER{row.pe_ratio:4.1f}={row.growth_per_ratio:4.2f} "
              f"配当{div_pct:4.1f}%")

    # CSVに保存
    output_csv = "./imura_method_qualified_full.csv"
    print(f"\n💾 保存中: {output_csv}")
    imura_qualified.to_csv(output_csv, index=False, encoding='utf-8-sig')
    print(f"✅ 保存完了: {len(imura_qualified)}銘柄")

    # 統計情報
    print(f"\n📈 該当銘柄の統計:")
    print(f"  成長率÷PER 平均: {imura_qualified['growth_per_ratio'].mean():.2f}")
    print(f"  成長率÷PER 中央値: {imura_qualified['growth_per_ratio'].median():.2f}")
    print(f"  成長率÷PER 最大: {imura_qualified['growth_per_ratio'].max():.2f}")
    print(f"  成長率÷PER 最小: {imura_qualified['growth_per_ratio'].min():.2f}")

    print(f"\n  売上成長率（3年平均） 平均: {imura_qualified['revenue_growth_3y'].mean():.2f}%")
    print(f"  PER 平均: {imura_qualified['pe_ratio'].mean():.2f}倍")
    print(f"  配当利回り 平均: {(imura_qualified['dividend_yield']/100).mean():.2f}%")

else:
    print(f"\n⚠️  該当銘柄がありません")

print(f"\n{'='*80}")
print("井村氏手法適用完了")
print(f"{'='*80}")
