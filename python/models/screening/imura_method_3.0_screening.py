#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
井村氏手法3.0 - スクリーニング実装

統計・実証研究に基づく改善版
- Growth/PER基準を廃止
- モメンタム基準を追加
- スコアリング方式を導入
- 配当利回り範囲を設定（2.5-6.0%）
"""

import pandas as pd
import numpy as np
from datetime import datetime

# =============================================================================
# 【Tier 1】必須基準（除外基準）
# =============================================================================

def apply_tier1_filters(df):
    """
    Tier 1: 必須基準（除外基準）

    基本的な財務健全性と流動性を確保
    """
    print("="*80)
    print("【Tier 1】必須基準（除外基準）の適用")
    print("="*80)

    initial_count = len(df)

    # フィルタを適用
    filters = {
        'PER 5-30倍': (df['pe_ratio'] >= 5) & (df['pe_ratio'] <= 30),
        '配当利回り 2.5-6.0%': (df['dividend_yield'] >= 250) & (df['dividend_yield'] <= 600),
        'ROE ≥ 8%': df['roe'] >= 8.0,
        'D/E比率 < 200%': df['debt_equity_ratio'] < 200,
        'フリーCF > 0': df['free_cash_flow'] > 0,
        '時価総額 ≥ 300億円': df['market_cap'] >= 30000,  # 単位: 百万円
        '1日出来高 ≥ 1億円': df['avg_volume'] >= 100000000,
    }

    # 各フィルタの結果を表示
    for filter_name, condition in filters.items():
        passed = condition.sum()
        print(f"{filter_name:30s}: {passed:5d}銘柄 / {initial_count}銘柄 ({passed/initial_count*100:5.1f}%)")

    # 全フィルタを適用
    combined_filter = pd.Series(True, index=df.index)
    for condition in filters.values():
        combined_filter &= condition

    df_filtered = df[combined_filter].copy()

    print(f"\n✅ Tier 1通過銘柄: {len(df_filtered)}銘柄 / {initial_count}銘柄 ({len(df_filtered)/initial_count*100:.1f}%)")

    return df_filtered


# =============================================================================
# 【Tier 2】スコアリング基準（110点満点）
# =============================================================================

def calculate_value_score(row):
    """バリューファクタースコア（40点満点）"""
    score = 0

    # PER（20点満点）
    per = row['pe_ratio']
    if per < 10:
        score += 20
    elif per < 15:
        score += 15
    elif per < 20:
        score += 10
    elif per < 30:
        score += 5

    # PBR（10点満点）
    pbr = row.get('price_book_ratio', np.nan)
    if not np.isnan(pbr):
        if pbr < 1.0:
            score += 10
        elif pbr < 1.5:
            score += 5

    # 配当利回り（10点満点）
    div_yield = row['dividend_yield'] / 100  # パーセント換算
    if 4.0 <= div_yield <= 6.0:
        score += 10
    elif 3.0 <= div_yield < 4.0:
        score += 5

    return score


def calculate_quality_score(row):
    """クオリティファクタースコア（40点満点）"""
    score = 0

    # ROE（15点満点）
    roe = row['roe']
    if roe >= 30:
        score += 15
    elif roe >= 15:
        score += 10
    elif roe >= 10:
        score += 5

    # D/E比率（10点満点）
    de_ratio = row.get('debt_equity_ratio', np.nan)
    if not np.isnan(de_ratio):
        if de_ratio < 50:
            score += 10
        elif de_ratio < 100:
            score += 5

    # 営業利益率（10点満点）
    operating_margin = row.get('operating_margin', np.nan)
    if not np.isnan(operating_margin):
        if operating_margin >= 15:
            score += 10
        elif operating_margin >= 10:
            score += 5

    # フリーCF/売上高（5点満点）
    fcf_ratio = row.get('fcf_to_sales', np.nan)
    if not np.isnan(fcf_ratio):
        if fcf_ratio >= 10:
            score += 5

    return score


def calculate_momentum_score(row):
    """モメンタムファクタースコア（20点満点）"""
    score = 0

    # 6ヶ月株価上昇率（10点満点）
    price_change_6m = row.get('price_change_6m', np.nan)
    if not np.isnan(price_change_6m):
        if price_change_6m > 20:
            score += 10
        elif price_change_6m > 10:
            score += 7
        elif price_change_6m > 0:
            score += 5

    # 52週高値からの乖離率（10点満点）
    distance_from_high = row.get('distance_from_52w_high', np.nan)
    if not np.isnan(distance_from_high):
        if distance_from_high < 10:
            score += 10
        elif distance_from_high < 20:
            score += 5

    return score


def calculate_other_score(row):
    """その他のスコア（10点満点）"""
    score = 0

    # 連続増配年数（5点満点）
    consecutive_dividend_years = row.get('consecutive_dividend_years', 0)
    if consecutive_dividend_years >= 5:
        score += 5

    # アナリスト推奨（5点満点）
    analyst_rating = row.get('analyst_rating', np.nan)
    if not np.isnan(analyst_rating):
        if analyst_rating >= 3.5:
            score += 5

    return score


def calculate_tier2_scores(df):
    """
    Tier 2: スコアリング基準（110点満点）

    各ファクターのスコアを計算
    """
    print("\n" + "="*80)
    print("【Tier 2】スコアリング基準（110点満点）の計算")
    print("="*80)

    df['value_score'] = df.apply(calculate_value_score, axis=1)
    df['quality_score'] = df.apply(calculate_quality_score, axis=1)
    df['momentum_score'] = df.apply(calculate_momentum_score, axis=1)
    df['other_score'] = df.apply(calculate_other_score, axis=1)

    # 総合スコア
    df['total_score'] = (
        df['value_score'] +
        df['quality_score'] +
        df['momentum_score'] +
        df['other_score']
    )

    # 統計情報
    print(f"\n📊 スコア統計:")
    print(f"  バリューファクター（40点満点）:")
    print(f"    平均: {df['value_score'].mean():.1f}点")
    print(f"    最大: {df['value_score'].max():.0f}点")
    print(f"  クオリティファクター（40点満点）:")
    print(f"    平均: {df['quality_score'].mean():.1f}点")
    print(f"    最大: {df['quality_score'].max():.0f}点")
    print(f"  モメンタムファクター（20点満点）:")
    print(f"    平均: {df['momentum_score'].mean():.1f}点")
    print(f"    最大: {df['momentum_score'].max():.0f}点")
    print(f"  その他（10点満点）:")
    print(f"    平均: {df['other_score'].mean():.1f}点")
    print(f"    最大: {df['other_score'].max():.0f}点")
    print(f"\n  総合スコア（110点満点）:")
    print(f"    平均: {df['total_score'].mean():.1f}点")
    print(f"    中央値: {df['total_score'].median():.1f}点")
    print(f"    最大: {df['total_score'].max():.0f}点")
    print(f"    最小: {df['total_score'].min():.0f}点")

    return df


# =============================================================================
# 【Tier 3】分散基準
# =============================================================================

def apply_tier3_diversification(df, max_stocks=50):
    """
    Tier 3: 分散基準

    - セクター上限: 10%
    - 最低セクター数: 6セクター
    - 単一銘柄上限: 5%
    """
    print("\n" + "="*80)
    print("【Tier 3】分散基準の適用")
    print("="*80)

    # スコア順にソート
    df_sorted = df.sort_values('total_score', ascending=False).reset_index(drop=True)

    selected_stocks = []
    sector_counts = {}
    sectors_used = set()

    sector_limit = int(max_stocks * 0.10)  # セクター上限10%

    for idx, row in df_sorted.iterrows():
        sector = row.get('sector', 'Unknown')

        # セクター上限チェック
        if sector_counts.get(sector, 0) >= sector_limit:
            continue

        # 選択
        selected_stocks.append(row)
        sector_counts[sector] = sector_counts.get(sector, 0) + 1
        sectors_used.add(sector)

        # 50銘柄に到達したらチェック
        if len(selected_stocks) >= max_stocks:
            # 最低6セクター必要
            if len(sectors_used) >= 6:
                break

    df_selected = pd.DataFrame(selected_stocks)

    print(f"\n✅ 最終選定銘柄数: {len(df_selected)}銘柄")
    print(f"✅ セクター数: {len(sectors_used)}セクター")
    print(f"\n📊 セクター別内訳:")
    for sector, count in sorted(sector_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"  {sector:30s}: {count:3d}銘柄 ({count/len(df_selected)*100:5.1f}%)")

    return df_selected


# =============================================================================
# メイン処理
# =============================================================================

def main():
    """メイン処理"""
    print("="*80)
    print("井村氏手法3.0 - スクリーニング")
    print("="*80)
    print(f"実行日時: {datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}")

    # CSVファイルを読み込み
    input_csv = "./phase1_1100stocks_with_growth.csv"
    print(f"\n📂 読み込み中: {input_csv}")

    try:
        df = pd.read_csv(input_csv, encoding='utf-8-sig')
        print(f"✅ 読み込み完了: {len(df)}銘柄")
    except FileNotFoundError:
        print(f"❌ ファイルが見つかりません: {input_csv}")
        print("\n代替として、サンプルデータで実行します。")
        df = create_sample_data()

    # 市場別内訳
    print(f"\n📊 市場別内訳:")
    market_counts = df['market'].value_counts()
    for market, count in market_counts.items():
        print(f"  {market}: {count}銘柄")

    # Tier 1: 必須基準（除外基準）
    df_tier1 = apply_tier1_filters(df)

    if len(df_tier1) == 0:
        print("\n❌ Tier 1通過銘柄がありません。")
        return

    # Tier 2: スコアリング基準
    df_tier2 = calculate_tier2_scores(df_tier1)

    # Tier 3: 分散基準
    df_final = apply_tier3_diversification(df_tier2, max_stocks=50)

    # 結果を表示
    print("\n" + "="*80)
    print("🏆 井村氏手法3.0 - TOP50銘柄")
    print("="*80)

    for i, row in enumerate(df_final.head(50).itertuples(), 1):
        market_flag = "🇯🇵" if row.market == "JP" else "🇺🇸"
        div_pct = row.dividend_yield / 100

        print(f"{i:2d}. {market_flag} {row.ticker:12s} {row.name[:30]:30s} "
              f"総合{row.total_score:3.0f}点 "
              f"(V{row.value_score:2.0f} Q{row.quality_score:2.0f} M{row.momentum_score:2.0f} O{row.other_score:2.0f}) "
              f"PER{row.pe_ratio:5.1f} ROE{row.roe:5.1f}% 配{div_pct:4.1f}%")

    # CSVに保存
    output_csv = "./imura_method_3.0_top50.csv"
    print(f"\n💾 保存中: {output_csv}")
    df_final.to_csv(output_csv, index=False, encoding='utf-8-sig')
    print(f"✅ 保存完了: {len(df_final)}銘柄")

    # スコア分布を保存
    score_distribution_csv = "./imura_method_3.0_score_distribution.csv"
    df_tier2[['ticker', 'name', 'market', 'total_score', 'value_score',
              'quality_score', 'momentum_score', 'other_score']].to_csv(
        score_distribution_csv, index=False, encoding='utf-8-sig'
    )
    print(f"💾 スコア分布を保存: {score_distribution_csv}")

    print("\n" + "="*80)
    print("スクリーニング完了")
    print("="*80)


def create_sample_data():
    """サンプルデータ作成（テスト用）"""
    np.random.seed(42)
    n = 1000

    data = {
        'ticker': [f'TICK{i:04d}' for i in range(n)],
        'name': [f'Company {i}' for i in range(n)],
        'market': np.random.choice(['JP', 'US'], n),
        'sector': np.random.choice(['Tech', 'Finance', 'Healthcare', 'Consumer',
                                   'Industrial', 'Energy', 'Materials', 'Utilities'], n),
        'pe_ratio': np.random.uniform(5, 40, n),
        'dividend_yield': np.random.uniform(0, 800, n),
        'roe': np.random.uniform(0, 50, n),
        'debt_equity_ratio': np.random.uniform(0, 300, n),
        'free_cash_flow': np.random.uniform(-100, 500, n),
        'market_cap': np.random.uniform(10000, 100000, n),
        'avg_volume': np.random.uniform(50000000, 500000000, n),
        'price_book_ratio': np.random.uniform(0.5, 3.0, n),
        'operating_margin': np.random.uniform(0, 30, n),
        'fcf_to_sales': np.random.uniform(0, 20, n),
        'price_change_6m': np.random.uniform(-30, 50, n),
        'distance_from_52w_high': np.random.uniform(0, 50, n),
        'consecutive_dividend_years': np.random.randint(0, 15, n),
        'analyst_rating': np.random.uniform(1, 5, n),
    }

    return pd.DataFrame(data)


if __name__ == "__main__":
    main()
