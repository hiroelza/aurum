"""
米国株50銘柄の統計分析・可視化スクリプト
2026年投資候補の詳細評価

実行方法:
python us_stocks_analysis_2026.py
"""

import numpy as np
import sys
import os

# パス設定をインポート
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import IMAGE_DIR
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from typing import Dict, List, Tuple

# 日本語フォント設定
matplotlib.rcParams['font.sans-serif'] = ['MS Gothic', 'Yu Gothic', 'Hiragino Sans', 'DejaVu Sans']
matplotlib.rcParams['axes.unicode_minus'] = False

# 50銘柄データ（評価スコア）
stocks_data = [
    # IT (12銘柄)
    {"ticker": "NVDA", "name": "NVIDIA", "sector": "IT", "score": 440, "price": 202.49, "marketcap": 4930, "allocation": 4.0, "dividend": 0.03, "per": 50},
    {"ticker": "MSFT", "name": "Microsoft", "sector": "IT", "score": 500, "price": 517.81, "marketcap": 3849, "allocation": 5.0, "dividend": 0.8, "per": 35},
    {"ticker": "AAPL", "name": "Apple", "sector": "IT", "score": 476, "price": 270.37, "marketcap": 4012, "allocation": 4.0, "dividend": 0.5, "per": 32},
    {"ticker": "GOOGL", "name": "Alphabet", "sector": "IT", "score": 467, "price": 281.19, "marketcap": 3440, "allocation": 4.0, "dividend": 0.5, "per": 25},
    {"ticker": "AMZN", "name": "Amazon", "sector": "IT", "score": 419, "price": 244.22, "marketcap": 2605, "allocation": 3.5, "dividend": 0.0, "per": 42},
    {"ticker": "AVGO", "name": "Broadcom", "sector": "IT", "score": 487, "price": 369.63, "marketcap": 1746, "allocation": 4.0, "dividend": 1.2, "per": 65},
    {"ticker": "TSM", "name": "Taiwan Semi", "sector": "IT", "score": 477, "price": 300.43, "marketcap": 1558, "allocation": 3.0, "dividend": 1.4, "per": 28},
    {"ticker": "ADBE", "name": "Adobe", "sector": "IT", "score": 412, "price": 490.00, "marketcap": 220, "allocation": 2.5, "dividend": 0.0, "per": 40},
    {"ticker": "CRM", "name": "Salesforce", "sector": "IT", "score": 405, "price": 335.00, "marketcap": 320, "allocation": 2.0, "dividend": 0.0, "per": 45},
    {"ticker": "ASML", "name": "ASML", "sector": "IT", "score": 480, "price": 715.00, "marketcap": 285, "allocation": 3.0, "dividend": 0.9, "per": 38},
    {"ticker": "AMD", "name": "AMD", "sector": "IT", "score": 390, "price": 165.00, "marketcap": 267, "allocation": 2.0, "dividend": 0.0, "per": 55},
    {"ticker": "ORCL", "name": "Oracle", "sector": "IT", "score": 458, "price": 175.00, "marketcap": 480, "allocation": 2.5, "dividend": 1.3, "per": 38},

    # ヘルスケア (8銘柄)
    {"ticker": "UNH", "name": "UnitedHealth", "sector": "Healthcare", "score": 495, "price": 525.00, "marketcap": 490, "allocation": 4.0, "dividend": 1.6, "per": 23},
    {"ticker": "JNJ", "name": "Johnson&Johnson", "sector": "Healthcare", "score": 492, "price": 161.00, "marketcap": 380, "allocation": 4.0, "dividend": 3.0, "per": 20},
    {"ticker": "LLY", "name": "Eli Lilly", "sector": "Healthcare", "score": 461, "price": 880.00, "marketcap": 820, "allocation": 3.0, "dividend": 0.7, "per": 75},
    {"ticker": "ABBV", "name": "AbbVie", "sector": "Healthcare", "score": 492, "price": 195.00, "marketcap": 345, "allocation": 3.5, "dividend": 3.5, "per": 18},
    {"ticker": "MRK", "name": "Merck", "sector": "Healthcare", "score": 496, "price": 108.00, "marketcap": 275, "allocation": 3.5, "dividend": 2.8, "per": 22},
    {"ticker": "PFE", "name": "Pfizer", "sector": "Healthcare", "score": 473, "price": 28.50, "marketcap": 160, "allocation": 3.0, "dividend": 6.1, "per": 12},
    {"ticker": "TMO", "name": "Thermo Fisher", "sector": "Healthcare", "score": 450, "price": 585.00, "marketcap": 225, "allocation": 2.5, "dividend": 0.3, "per": 30},
    {"ticker": "CVS", "name": "CVS Health", "sector": "Healthcare", "score": 456, "price": 58.00, "marketcap": 75, "allocation": 2.5, "dividend": 4.5, "per": 9},

    # 金融 (6銘柄)
    {"ticker": "JPM", "name": "JPMorgan", "sector": "Financials", "score": 498, "price": 220.00, "marketcap": 640, "allocation": 4.0, "dividend": 2.5, "per": 13},
    {"ticker": "BAC", "name": "Bank of America", "sector": "Financials", "score": 496, "price": 43.00, "marketcap": 330, "allocation": 3.5, "dividend": 2.8, "per": 12},
    {"ticker": "WFC", "name": "Wells Fargo", "sector": "Financials", "score": 502, "price": 62.00, "marketcap": 220, "allocation": 4.0, "dividend": 2.9, "per": 11},
    {"ticker": "GS", "name": "Goldman Sachs", "sector": "Financials", "score": 498, "price": 530.00, "marketcap": 180, "allocation": 3.5, "dividend": 2.3, "per": 14},
    {"ticker": "MS", "name": "Morgan Stanley", "sector": "Financials", "score": 502, "price": 125.00, "marketcap": 210, "allocation": 3.5, "dividend": 3.2, "per": 16},
    {"ticker": "V", "name": "Visa", "sector": "Financials", "score": 493, "price": 310.00, "marketcap": 650, "allocation": 3.0, "dividend": 0.8, "per": 32},

    # 一般消費財 (5銘柄)
    {"ticker": "TSLA", "name": "Tesla", "sector": "Consumer Disc.", "score": 363, "price": 456.56, "marketcap": 1518, "allocation": 2.0, "dividend": 0.0, "per": 90},
    {"ticker": "HD", "name": "Home Depot", "sector": "Consumer Disc.", "score": 489, "price": 395.00, "marketcap": 390, "allocation": 3.5, "dividend": 2.4, "per": 25},
    {"ticker": "MCD", "name": "McDonald's", "sector": "Consumer Disc.", "score": 474, "price": 300.00, "marketcap": 220, "allocation": 3.0, "dividend": 2.3, "per": 26},
    {"ticker": "SBUX", "name": "Starbucks", "sector": "Consumer Disc.", "score": 463, "price": 100.00, "marketcap": 115, "allocation": 2.5, "dividend": 2.6, "per": 28},
    {"ticker": "NKE", "name": "Nike", "sector": "Consumer Disc.", "score": 462, "price": 77.00, "marketcap": 115, "allocation": 2.5, "dividend": 1.7, "per": 24},

    # 資本財 (4銘柄)
    {"ticker": "CAT", "name": "Caterpillar", "sector": "Industrials", "score": 488, "price": 395.00, "marketcap": 200, "allocation": 3.5, "dividend": 1.7, "per": 18},
    {"ticker": "HON", "name": "Honeywell", "sector": "Industrials", "score": 490, "price": 215.00, "marketcap": 140, "allocation": 3.0, "dividend": 2.2, "per": 24},
    {"ticker": "RTX", "name": "Raytheon", "sector": "Industrials", "score": 496, "price": 125.00, "marketcap": 180, "allocation": 3.5, "dividend": 2.4, "per": 20},
    {"ticker": "UPS", "name": "UPS", "sector": "Industrials", "score": 472, "price": 135.00, "marketcap": 115, "allocation": 2.5, "dividend": 4.8, "per": 18},

    # エネルギー (3銘柄)
    {"ticker": "XOM", "name": "Exxon Mobil", "sector": "Energy", "score": 483, "price": 120.00, "marketcap": 480, "allocation": 3.5, "dividend": 3.3, "per": 14},
    {"ticker": "CVX", "name": "Chevron", "sector": "Energy", "score": 482, "price": 160.00, "marketcap": 290, "allocation": 3.5, "dividend": 4.0, "per": 13},
    {"ticker": "COP", "name": "ConocoPhillips", "sector": "Energy", "score": 488, "price": 110.00, "marketcap": 135, "allocation": 2.5, "dividend": 3.0, "per": 12},

    # 生活必需品 (6銘柄)
    {"ticker": "PG", "name": "P&G", "sector": "Cons. Staples", "score": 484, "price": 170.00, "marketcap": 400, "allocation": 3.5, "dividend": 2.4, "per": 27},
    {"ticker": "KO", "name": "Coca-Cola", "sector": "Cons. Staples", "score": 482, "price": 64.00, "marketcap": 275, "allocation": 3.5, "dividend": 3.0, "per": 26},
    {"ticker": "PEP", "name": "PepsiCo", "sector": "Cons. Staples", "score": 483, "price": 168.00, "marketcap": 230, "allocation": 3.5, "dividend": 3.0, "per": 24},
    {"ticker": "COST", "name": "Costco", "sector": "Cons. Staples", "score": 463, "price": 905.00, "marketcap": 400, "allocation": 2.5, "dividend": 0.5, "per": 55},
    {"ticker": "WMT", "name": "Walmart", "sector": "Cons. Staples", "score": 484, "price": 87.00, "marketcap": 685, "allocation": 3.0, "dividend": 1.2, "per": 36},
    {"ticker": "MDLZ", "name": "Mondelez", "sector": "Cons. Staples", "score": 476, "price": 68.00, "marketcap": 92, "allocation": 2.5, "dividend": 2.3, "per": 22},

    # 通信 (2銘柄)
    {"ticker": "META", "name": "Meta", "sector": "Comm. Services", "score": 473, "price": 648.35, "marketcap": 1410, "allocation": 3.5, "dividend": 0.3, "per": 28},
    {"ticker": "NFLX", "name": "Netflix", "sector": "Comm. Services", "score": 398, "price": 750.00, "marketcap": 320, "allocation": 2.0, "dividend": 0.0, "per": 45},

    # 公益 (2銘柄)
    {"ticker": "NEE", "name": "NextEra Energy", "sector": "Utilities", "score": 498, "price": 75.00, "marketcap": 155, "allocation": 3.5, "dividend": 2.7, "per": 22},
    {"ticker": "DUK", "name": "Duke Energy", "sector": "Utilities", "score": 480, "price": 115.00, "marketcap": 90, "allocation": 3.0, "dividend": 4.0, "per": 18},

    # 素材 (1銘柄)
    {"ticker": "LIN", "name": "Linde", "sector": "Materials", "score": 500, "price": 470.00, "marketcap": 230, "allocation": 3.5, "dividend": 1.4, "per": 32},

    # 不動産 (1銘柄)
    {"ticker": "PLD", "name": "Prologis", "sector": "Real Estate", "score": 488, "price": 120.00, "marketcap": 111, "allocation": 3.0, "dividend": 3.0, "per": 35},
]

def create_dataframe(stocks_data: List[Dict]) -> pd.DataFrame:
    """銘柄データをDataFrameに変換"""
    df = pd.DataFrame(stocks_data)
    df['allocation_amount'] = df['allocation'] * 10000  # 配分額（円）
    return df

def sector_analysis(df: pd.DataFrame) -> pd.DataFrame:
    """セクター別分析"""
    sector_stats = df.groupby('sector').agg({
        'allocation': 'sum',
        'allocation_amount': 'sum',
        'score': 'mean',
        'dividend': 'mean',
        'per': 'mean',
        'ticker': 'count'
    }).round(2)

    sector_stats.columns = ['配分比率(%)', '配分額(万円)', '平均スコア', '平均配当(%)', '平均PER', '銘柄数']
    sector_stats = sector_stats.sort_values('配分額(万円)', ascending=False)

    return sector_stats

def top_stocks_analysis(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    """上位N銘柄の分析"""
    top_stocks = df.nlargest(n, 'score')[['ticker', 'name', 'sector', 'score', 'allocation', 'dividend', 'per']]
    top_stocks = top_stocks.reset_index(drop=True)
    top_stocks.index = top_stocks.index + 1
    return top_stocks

def dividend_analysis(df: pd.DataFrame) -> Dict:
    """配当分析"""
    total_allocation = df['allocation_amount'].sum()
    weighted_dividend = (df['allocation_amount'] * df['dividend']).sum() / total_allocation

    high_div_stocks = df[df['dividend'] >= 3.0].sort_values('dividend', ascending=False)

    return {
        'weighted_dividend': weighted_dividend,
        'high_dividend_stocks': high_div_stocks[['ticker', 'name', 'dividend', 'allocation']],
        'dividend_kings_count': len(df[df['dividend'] >= 3.0])
    }

def valuation_analysis(df: pd.DataFrame) -> Dict:
    """バリュエーション分析"""
    avg_per = df['per'].mean()
    weighted_per = (df['allocation_amount'] * df['per']).sum() / df['allocation_amount'].sum()

    value_stocks = df[df['per'] <= 20].sort_values('per')
    growth_stocks = df[df['per'] >= 40].sort_values('per', ascending=False)

    return {
        'average_per': avg_per,
        'weighted_per': weighted_per,
        'value_stocks_count': len(value_stocks),
        'growth_stocks_count': len(growth_stocks)
    }

def plot_sector_allocation(df: pd.DataFrame):
    """セクター別配分のパイチャート"""
    sector_allocation = df.groupby('sector')['allocation'].sum().sort_values(ascending=False)

    fig, ax = plt.subplots(figsize=(12, 8))
    colors = plt.cm.Set3(range(len(sector_allocation)))

    wedges, texts, autotexts = ax.pie(
        sector_allocation,
        labels=sector_allocation.index,
        autopct='%1.1f%%',
        startangle=90,
        colors=colors,
        textprops={'fontsize': 11}
    )

    for autotext in autotexts:
        autotext.set_color('black')
        autotext.set_weight('bold')

    ax.set_title('セクター別配分比率（50万円投資）', fontsize=16, fontweight='bold', pad=20)
    plt.tight_layout()
    plt.savefig(os.path.join(IMAGE_DIR, 'sector_allocation.png'), dpi=300, bbox_inches='tight')
    print("[OK] セクター別配分チャート保存: sector_allocation.png")

def plot_score_distribution(df: pd.DataFrame):
    """スコア分布のヒストグラム"""
    fig, ax = plt.subplots(figsize=(12, 6))

    ax.hist(df['score'], bins=20, color='steelblue', edgecolor='black', alpha=0.7)
    ax.axvline(df['score'].mean(), color='red', linestyle='--', linewidth=2, label=f'平均: {df["score"].mean():.1f}')
    ax.axvline(df['score'].median(), color='green', linestyle='--', linewidth=2, label=f'中央値: {df["score"].median():.1f}')

    ax.set_xlabel('総合スコア', fontsize=12)
    ax.set_ylabel('銘柄数', fontsize=12)
    ax.set_title('50銘柄の総合スコア分布', fontsize=16, fontweight='bold')
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(os.path.join(IMAGE_DIR, 'score_distribution.png'), dpi=300, bbox_inches='tight')
    print("[OK] スコア分布グラフ保存: score_distribution.png")

def plot_dividend_vs_score(df: pd.DataFrame):
    """配当利回り vs スコアの散布図"""
    fig, ax = plt.subplots(figsize=(14, 8))

    sectors = df['sector'].unique()
    colors = plt.cm.tab10(range(len(sectors)))
    sector_color_map = dict(zip(sectors, colors))

    for sector in sectors:
        sector_df = df[df['sector'] == sector]
        ax.scatter(
            sector_df['dividend'],
            sector_df['score'],
            s=sector_df['allocation'] * 50,
            alpha=0.6,
            c=[sector_color_map[sector]],
            label=sector,
            edgecolors='black',
            linewidth=0.5
        )

    ax.set_xlabel('配当利回り (%)', fontsize=12)
    ax.set_ylabel('総合スコア', fontsize=12)
    ax.set_title('配当利回り vs 総合スコア（バブルサイズ=配分額）', fontsize=16, fontweight='bold')
    ax.legend(fontsize=9, loc='upper left', ncol=2)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(os.path.join(IMAGE_DIR, 'dividend_vs_score.png'), dpi=300, bbox_inches='tight')
    print("[OK] 配当vsスコア散布図保存: dividend_vs_score.png")

def plot_per_distribution(df: pd.DataFrame):
    """PER分布の箱ひげ図"""
    fig, ax = plt.subplots(figsize=(14, 8))

    sectors = df.groupby('sector')['per'].median().sort_values(ascending=False).index
    sector_data = [df[df['sector'] == sector]['per'].values for sector in sectors]

    bp = ax.boxplot(sector_data, labels=sectors, patch_artist=True, notch=True)

    for patch in bp['boxes']:
        patch.set_facecolor('lightblue')
        patch.set_alpha(0.7)

    ax.set_ylabel('PER (倍)', fontsize=12)
    ax.set_xlabel('セクター', fontsize=12)
    ax.set_title('セクター別PER分布', fontsize=16, fontweight='bold')
    ax.grid(True, alpha=0.3, axis='y')
    plt.xticks(rotation=45, ha='right')

    plt.tight_layout()
    plt.savefig(os.path.join(IMAGE_DIR, 'per_distribution.png'), dpi=300, bbox_inches='tight')
    print("[OK] PER分布グラフ保存: per_distribution.png")

def plot_top10_stocks(df: pd.DataFrame):
    """TOP10銘柄の棒グラフ"""
    top10 = df.nlargest(10, 'score')

    fig, ax = plt.subplots(figsize=(14, 8))

    bars = ax.barh(range(len(top10)), top10['score'], color='steelblue', edgecolor='black')
    ax.set_yticks(range(len(top10)))
    ax.set_yticklabels([f"{row['ticker']}: {row['name']}" for _, row in top10.iterrows()])
    ax.set_xlabel('総合スコア', fontsize=12)
    ax.set_title('TOP10銘柄ランキング', fontsize=16, fontweight='bold')
    ax.grid(True, alpha=0.3, axis='x')

    for i, (_, row) in enumerate(top10.iterrows()):
        ax.text(row['score'] + 5, i, f"{row['score']}", va='center', fontsize=10, fontweight='bold')

    plt.tight_layout()
    plt.savefig(os.path.join(IMAGE_DIR, 'top10_stocks.png'), dpi=300, bbox_inches='tight')
    print("[OK] TOP10ランキンググラフ保存: top10_stocks.png")

def print_statistics(df: pd.DataFrame):
    """統計サマリーの出力"""
    print("\n" + "="*80)
    print("【米国株50銘柄 統計分析サマリー】")
    print("="*80)

    print(f"\n総投資額: 50.0万円")
    print(f"銘柄数: {len(df)}銘柄")
    print(f"セクター数: {df['sector'].nunique()}セクター")

    print(f"\n【スコア統計】")
    print(f"  平均スコア: {df['score'].mean():.1f} / 600点")
    print(f"  中央値: {df['score'].median():.1f}")
    print(f"  最高スコア: {df['score'].max()} ({df.loc[df['score'].idxmax(), 'ticker']})")
    print(f"  最低スコア: {df['score'].min()} ({df.loc[df['score'].idxmin(), 'ticker']})")
    print(f"  標準偏差: {df['score'].std():.1f}")

    print(f"\n【配当統計】")
    weighted_div = (df['allocation_amount'] * df['dividend']).sum() / df['allocation_amount'].sum()
    print(f"  加重平均配当利回り: {weighted_div:.2f}%")
    print(f"  平均配当利回り: {df['dividend'].mean():.2f}%")
    print(f"  高配当株（3%以上）: {len(df[df['dividend'] >= 3.0])}銘柄")
    print(f"  最高配当: {df['dividend'].max()}% ({df.loc[df['dividend'].idxmax(), 'ticker']})")

    print(f"\n【バリュエーション統計】")
    weighted_per = (df['allocation_amount'] * df['per']).sum() / df['allocation_amount'].sum()
    print(f"  加重平均PER: {weighted_per:.1f}倍")
    print(f"  平均PER: {df['per'].mean():.1f}倍")
    print(f"  バリュー株（PER 20以下）: {len(df[df['per'] <= 20])}銘柄")
    print(f"  グロース株（PER 40以上）: {len(df[df['per'] >= 40])}銘柄")

    print(f"\n【時価総額統計】")
    print(f"  平均時価総額: ${df['marketcap'].mean():.0f}億")
    print(f"  中央値時価総額: ${df['marketcap'].median():.0f}億")
    print(f"  メガキャップ（1兆ドル以上）: {len(df[df['marketcap'] >= 1000])}銘柄")

def main():
    """メイン処理"""
    print("\n" + "="*80)
    print("米国株50銘柄の統計分析・可視化")
    print("2026年投資候補の詳細評価")
    print("="*80)

    # データ読み込み
    df = create_dataframe(stocks_data)

    # 統計分析
    print_statistics(df)

    # セクター別分析
    print("\n" + "-"*80)
    print("【セクター別分析】")
    print("-"*80)
    sector_stats = sector_analysis(df)
    print(sector_stats.to_string())

    # TOP10銘柄
    print("\n" + "-"*80)
    print("【TOP10銘柄】")
    print("-"*80)
    top10 = top_stocks_analysis(df, 10)
    print(top10.to_string())

    # 配当分析
    print("\n" + "-"*80)
    print("【高配当銘柄（3%以上）】")
    print("-"*80)
    div_analysis = dividend_analysis(df)
    print(div_analysis['high_dividend_stocks'].to_string())

    # グラフ生成
    print("\n" + "-"*80)
    print("【グラフ生成中...】")
    print("-"*80)

    plot_sector_allocation(df)
    plot_score_distribution(df)
    plot_dividend_vs_score(df)
    plot_per_distribution(df)
    plot_top10_stocks(df)

    print("\n" + "="*80)
    print("[完了] 分析完了！")
    print("="*80)
    print("\n生成されたファイル:")
    print("  1. sector_allocation.png - セクター別配分")
    print("  2. score_distribution.png - スコア分布")
    print("  3. dividend_vs_score.png - 配当vsスコア散布図")
    print("  4. per_distribution.png - PER分布")
    print("  5. top10_stocks.png - TOP10ランキング")
    print("\n")

if __name__ == "__main__":
    main()
