#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
井村氏手法を1,091銘柄に適用

井村氏3基準:
1. 成長率÷PER ≧ 1.0
2. 配当利回り ≧ 3%
3. 5年以上連続増配

現在のデータで確認できるもの:
- 配当利回り ≧ 3% (dividend_yield ≧ 300と仮定)
- PER (pe_ratio)
- ROE (roe)

※成長率と連続増配年数のデータは含まれていません
"""

import pandas as pd
import numpy as np

def analyze_imura_method(csv_path):
    """井村氏手法の分析"""
    print("="*80)
    print("井村氏手法 - 1,091銘柄分析")
    print("="*80)

    # CSVを読み込み
    df = pd.read_csv(csv_path, encoding='utf-8-sig')

    print(f"\n📊 総銘柄数: {len(df)}銘柄")
    print(f"  - 日本株: {len(df[df['market']=='JP'])}銘柄")
    print(f"  - 米国株: {len(df[df['market']=='US'])}銘柄")

    # データ品質チェック
    print(f"\n📊 データ品質:")
    print(f"  - PERデータあり: {df['pe_ratio'].notna().sum()}銘柄")
    print(f"  - ROEデータあり: {df['roe'].notna().sum()}銘柄")
    print(f"  - 配当利回りデータあり: {df['dividend_yield'].notna().sum()}銘柄")

    # 配当利回りの単位を確認
    div_sample = df[df['dividend_yield'].notna()]['dividend_yield'].head(10)
    print(f"\n📊 配当利回りサンプル: {div_sample.tolist()}")

    # 配当利回りが100倍されている場合を想定 (167.0 = 1.67%)
    # 井村氏基準: 配当利回り≧3% → dividend_yield ≧ 300

    # 基準1: 配当利回り≧3%
    condition_dividend = df['dividend_yield'] >= 300
    count_dividend_3pct = condition_dividend.sum()

    print(f"\n{'='*80}")
    print("【基準1】配当利回り ≧ 3%")
    print(f"{'='*80}")
    print(f"✅ 該当銘柄数: {count_dividend_3pct}銘柄 / {len(df)}銘柄")
    print(f"   比率: {count_dividend_3pct/len(df)*100:.1f}%")

    # 配当利回り≧3%の銘柄の市場別内訳
    dividend_3pct_stocks = df[condition_dividend]
    print(f"\n📊 市場別内訳:")
    print(f"  - 日本株: {len(dividend_3pct_stocks[dividend_3pct_stocks['market']=='JP'])}銘柄")
    print(f"  - 米国株: {len(dividend_3pct_stocks[dividend_3pct_stocks['market']=='US'])}銘柄")

    # 配当利回りTOP20
    print(f"\n🏆 配当利回りTOP20:")
    print("-"*80)
    top_dividend = df[df['dividend_yield'].notna()].nlargest(20, 'dividend_yield')
    for i, row in enumerate(top_dividend.itertuples(), 1):
        div_pct = row.dividend_yield / 100
        market_flag = "🇯🇵" if row.market == "JP" else "🇺🇸"
        print(f"{i:2d}. {market_flag} {row.ticker:12s} {row.name:40s} {div_pct:5.2f}%")

    # 基準2: ROE ≧ 10% (井村氏手法の追加フィルタとして)
    print(f"\n{'='*80}")
    print("【基準2】ROE ≧ 10% (財務健全性)")
    print(f"{'='*80}")
    condition_roe = df['roe'] >= 10.0
    count_roe_10pct = condition_roe.sum()
    print(f"✅ 該当銘柄数: {count_roe_10pct}銘柄 / {len(df)}銘柄")
    print(f"   比率: {count_roe_10pct/len(df)*100:.1f}%")

    # 基準3: PER 5-20倍 (割安範囲)
    print(f"\n{'='*80}")
    print("【基準3】PER 5-20倍 (割安範囲)")
    print(f"{'='*80}")
    condition_per = (df['pe_ratio'] >= 5) & (df['pe_ratio'] <= 20)
    count_per_range = condition_per.sum()
    print(f"✅ 該当銘柄数: {count_per_range}銘柄 / {len(df)}銘柄")
    print(f"   比率: {count_per_range/len(df)*100:.1f}%")

    # 複合条件: 配当3%以上 AND ROE10%以上
    print(f"\n{'='*80}")
    print("【複合条件A】配当≧3% AND ROE≧10%")
    print(f"{'='*80}")
    condition_a = condition_dividend & condition_roe
    count_a = condition_a.sum()
    print(f"✅ 該当銘柄数: {count_a}銘柄 / {len(df)}銘柄")
    print(f"   比率: {count_a/len(df)*100:.1f}%")

    # 複合条件B: 配当3%以上 AND ROE10%以上 AND PER 5-20倍
    print(f"\n{'='*80}")
    print("【複合条件B】配当≧3% AND ROE≧10% AND PER 5-20倍")
    print(f"{'='*80}")
    condition_b = condition_dividend & condition_roe & condition_per
    count_b = condition_b.sum()
    print(f"✅ 該当銘柄数: {count_b}銘柄 / {len(df)}銘柄")
    print(f"   比率: {count_b/len(df)*100:.1f}%")

    # 複合条件Bを満たす銘柄の詳細
    if count_b > 0:
        print(f"\n🏆 複合条件B該当銘柄TOP30:")
        print("-"*80)
        qualified_b = df[condition_b].copy()
        qualified_b['div_pct'] = qualified_b['dividend_yield'] / 100
        qualified_b = qualified_b.sort_values('div_pct', ascending=False).head(30)

        for i, row in enumerate(qualified_b.itertuples(), 1):
            market_flag = "🇯🇵" if row.market == "JP" else "🇺🇸"
            print(f"{i:2d}. {market_flag} {row.ticker:12s} {row.name:35s} "
                  f"配当{row.div_pct:4.1f}% ROE{row.roe:5.1f}% PER{row.pe_ratio:5.1f}倍")

    # 成長率のデータがないことを明記
    print(f"\n{'='*80}")
    print("⚠️  データ制約")
    print(f"{'='*80}")
    print("井村氏手法の完全な適用には以下のデータが不足しています:")
    print("  ❌ 成長率 (売上成長率または利益成長率)")
    print("  ❌ 連続増配年数")
    print("\n現在のデータで確認できるのは:")
    print("  ✅ 配当利回り ≧ 3%")
    print("  ✅ ROE (財務健全性)")
    print("  ✅ PER (バリュエーション)")
    print("\n完全な井村氏手法の適用には、追加のデータ取得が必要です。")

    # 結果をCSVに保存
    output_path = "./imura_qualified_stocks.csv"
    if count_b > 0:
        qualified_b_full = df[condition_b].copy()
        qualified_b_full['div_pct'] = qualified_b_full['dividend_yield'] / 100
        qualified_b_full = qualified_b_full.sort_values('div_pct', ascending=False)
        qualified_b_full.to_csv(output_path, index=False, encoding='utf-8-sig')
        print(f"\n📄 結果を保存: {output_path}")
        print(f"   保存銘柄数: {len(qualified_b_full)}銘柄")

    print(f"\n{'='*80}")
    print("分析完了")
    print(f"{'='*80}")

    return {
        'total': len(df),
        'dividend_3pct': count_dividend_3pct,
        'roe_10pct': count_roe_10pct,
        'per_5_20': count_per_range,
        'condition_a': count_a,
        'condition_b': count_b
    }

if __name__ == "__main__":
    csv_path = "./phase1_1100stocks_growth_combined.csv"
    results = analyze_imura_method(csv_path)
