#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase 1 (簡易版): 400銘柄評価アプローチ
- 既存295銘柄(日本株): 3エージェント評価済み → 再利用
- 追加5銘柄(日本株): 300-305位 → 定量評価
- 米国株100銘柄: S&P 500の主要銘柄 → 定量評価

合計: 400銘柄 (日本株300, 米国株100)
実行時間: 約10分

アウトプット:
  1. phase1_400stocks_combined.csv (400銘柄の統合評価)
  2. phase2_top200_candidates.csv (TOP 200銘柄リスト)
"""

import pandas as pd
import yfinance as yf
import time
import numpy as np
from datetime import datetime
import warnings
import sys

warnings.filterwarnings('ignore')

# Windows環境でのUTF-8出力対応
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')


# ===========================
# 1. 既存評価データの統合
# ===========================

def load_existing_evaluations():
    """
    既存の3バッチ（295銘柄）の評価データを統合
    """
    print("📂 既存の評価データを読み込み中...")

    # バッチ1-1: TOP 100
    batch1_1 = pd.read_csv('batch1-1_japan_top100_final_scores.csv')
    print(f"  ✅ Batch 1-1: {len(batch1_1)}銘柄")

    # バッチ1-2: 101-200
    batch1_2 = pd.read_csv('batch1-2_japan_101-200_final_scores.csv')
    print(f"  ✅ Batch 1-2: {len(batch1_2)}銘柄")

    # バッチ1-3: 201-300
    batch1_3 = pd.read_csv('batch1-3_japan_201-300_final_scores.csv')
    print(f"  ✅ Batch 1-3: {len(batch1_3)}銘柄")

    # 統合
    all_existing = pd.concat([batch1_1, batch1_2, batch1_3], ignore_index=True)

    print(f"  📊 合計: {len(all_existing)}銘柄の評価データを統合")
    print()

    # カラム名を標準化
    if 'code' in all_existing.columns:
        all_existing = all_existing.rename(columns={'code': 'ticker'})
    if 'average' in all_existing.columns:
        all_existing = all_existing.rename(columns={'average': 'final_score'})

    # ティッカー形式を修正（数字のみ → XXXX.T形式）
    all_existing['ticker'] = all_existing['ticker'].apply(
        lambda x: f"{x}.T" if not str(x).endswith('.T') and str(x).isdigit() else str(x)
    )

    # 市場タグを追加
    all_existing['market'] = 'JP'
    all_existing['evaluation_type'] = '3agent'  # 3エージェント評価済み

    return all_existing


# ===========================
# 2. 追加銘柄リスト
# ===========================

def get_additional_japan_stocks():
    """
    日本株の追加5銘柄（300-305位）
    """
    return [
        '3402.T',  # 東レ
        '3407.T',  # 旭化成
        '4185.T',  # JSR
        '4922.T',  # コーセー
        '5108.T',  # ブリヂストン
    ]


def get_us_top100_stocks():
    """
    米国株TOP 100銘柄（時価総額順）
    """
    return [
        # Mega Cap (時価総額 1兆ドル以上)
        'AAPL',   # Apple
        'MSFT',   # Microsoft
        'GOOGL',  # Alphabet Class A
        'GOOG',   # Alphabet Class C
        'AMZN',   # Amazon
        'NVDA',   # NVIDIA
        'META',   # Meta Platforms
        'TSLA',   # Tesla

        # Large Cap Tech
        'BRK.B',  # Berkshire Hathaway
        'V',      # Visa
        'UNH',    # UnitedHealth Group
        'JNJ',    # Johnson & Johnson
        'WMT',    # Walmart
        'JPM',    # JPMorgan Chase
        'MA',     # Mastercard
        'PG',     # Procter & Gamble
        'XOM',    # Exxon Mobil
        'HD',     # Home Depot
        'CVX',    # Chevron
        'ABBV',   # AbbVie
        'MRK',    # Merck
        'KO',     # Coca-Cola
        'PEP',    # PepsiCo
        'COST',   # Costco
        'AVGO',   # Broadcom
        'TMO',    # Thermo Fisher Scientific
        'ADBE',   # Adobe
        'ACN',    # Accenture
        'CSCO',   # Cisco Systems
        'NKE',    # Nike
        'ABT',    # Abbott Laboratories
        'DIS',    # Walt Disney
        'CRM',    # Salesforce
        'VZ',     # Verizon
        'CMCSA',  # Comcast
        'NFLX',   # Netflix
        'INTC',   # Intel
        'AMD',    # Advanced Micro Devices
        'QCOM',   # Qualcomm
        'TXN',    # Texas Instruments
        'UNP',    # Union Pacific
        'PM',     # Philip Morris International
        'BA',     # Boeing
        'UPS',    # United Parcel Service
        'HON',    # Honeywell
        'SBUX',   # Starbucks
        'IBM',    # IBM
        'GE',     # General Electric
        'CAT',    # Caterpillar
        'MMM',    # 3M
        'GS',     # Goldman Sachs
        'ORCL',   # Oracle
        'COP',    # ConocoPhillips
        'NEE',    # NextEra Energy
        'LLY',    # Eli Lilly
        'RTX',    # Raytheon Technologies
        'LOW',    # Lowe's
        'MDT',    # Medtronic
        'SPGI',   # S&P Global
        'INTU',   # Intuit
        'ISRG',   # Intuitive Surgical
        'ADP',    # Automatic Data Processing
        'BLK',    # BlackRock
        'TJX',    # TJX Companies
        'BKNG',   # Booking Holdings
        'GILD',   # Gilead Sciences
        'AMGN',   # Amgen
        'VRTX',   # Vertex Pharmaceuticals
        'CI',     # Cigna
        'MDLZ',   # Mondelez International
        'MO',     # Altria Group
        'SYK',    # Stryker
        'REGN',   # Regeneron Pharmaceuticals
        'CVS',    # CVS Health
        'PLD',    # Prologis
        'CB',     # Chubb
        'SO',     # Southern Company
        'DUK',    # Duke Energy
        'ZTS',    # Zoetis
        'BMY',    # Bristol Myers Squibb
        'C',      # Citigroup
        'BDX',    # Becton Dickinson
        'PNC',    # PNC Financial Services
        'USB',    # U.S. Bancorp
        'TFC',    # Truist Financial
        'MS',     # Morgan Stanley
        'CL',     # Colgate-Palmolive
        'BSX',    # Boston Scientific
        'ETN',    # Eaton
        'SCHW',   # Charles Schwab
        'EOG',    # EOG Resources
        'FI',     # Fiserv
        'MU',     # Micron Technology
        'DE',     # Deere & Company
        'AXP',    # American Express
        'MMC',    # Marsh & McLennan
        'EL',     # Estée Lauder
        'NOC',    # Northrop Grumman
        'LMT',    # Lockheed Martin
    ]


# ===========================
# 3. 定量評価
# ===========================

def get_stock_metrics(ticker, market='JP'):
    """
    個別銘柄の定量指標を取得
    """
    try:
        stock = yf.Ticker(ticker)
        info = stock.info

        # 基本情報
        name = info.get('longName', info.get('shortName', ticker))
        market_cap = info.get('marketCap', 0)

        # 収益性指標
        roe = info.get('returnOnEquity', None)
        roa = info.get('returnOnAssets', None)

        # バリュエーション指標
        pe_ratio = info.get('trailingPE', None)
        pb_ratio = info.get('priceToBook', None)

        # 配当指標
        dividend_yield = info.get('dividendYield', 0)
        if dividend_yield:
            dividend_yield = dividend_yield * 100

        # 財務健全性
        debt_to_equity = info.get('debtToEquity', None)
        current_ratio = info.get('currentRatio', None)

        return {
            'ticker': ticker,
            'name': name,
            'market': market,
            'market_cap': market_cap,
            'roe': roe * 100 if roe else None,
            'roa': roa * 100 if roa else None,
            'pe_ratio': pe_ratio,
            'pb_ratio': pb_ratio,
            'dividend_yield': dividend_yield,
            'debt_to_equity': debt_to_equity,
            'current_ratio': current_ratio,
        }

    except Exception as e:
        print(f"\n⚠️ エラー: {ticker} - {str(e)}")
        return {
            'ticker': ticker,
            'name': ticker,
            'market': market,
            'market_cap': 0,
            'roe': None,
            'roa': None,
            'pe_ratio': None,
            'pb_ratio': None,
            'dividend_yield': None,
            'debt_to_equity': None,
            'current_ratio': None,
        }


def calculate_quantitative_score(metrics):
    """
    定量指標からスコア（0-100点）を算出

    評価項目:
    1. 時価総額（20点）
    2. ROE（20点）
    3. 配当利回り（15点）
    4. PER（15点）
    5. PBR（10点）
    6. 財務健全性（20点）
    """
    score = 0

    # 1. 時価総額スコア（20点）
    market_cap = metrics['market_cap']
    if market_cap > 10_000_000_000_000:  # 10兆円/100億ドル以上
        score += 20
    elif market_cap > 1_000_000_000_000:  # 1兆円/10億ドル以上
        score += 15
    elif market_cap > 100_000_000_000:  # 1000億円/1億ドル以上
        score += 10
    elif market_cap > 10_000_000_000:  # 100億円/1000万ドル以上
        score += 5

    # 2. ROEスコア（20点）
    roe = metrics['roe']
    if roe is not None:
        if roe >= 20:
            score += 20
        elif roe >= 15:
            score += 15
        elif roe >= 10:
            score += 10
        elif roe >= 5:
            score += 5

    # 3. 配当利回りスコア（15点）
    dividend_yield = metrics['dividend_yield']
    if dividend_yield is not None:
        if dividend_yield >= 4.0:
            score += 15
        elif dividend_yield >= 3.0:
            score += 12
        elif dividend_yield >= 2.0:
            score += 8
        elif dividend_yield >= 1.0:
            score += 4

    # 4. PERスコア（15点）: 10-20倍が理想
    pe_ratio = metrics['pe_ratio']
    if pe_ratio is not None:
        if 10 <= pe_ratio <= 20:
            score += 15
        elif 5 <= pe_ratio < 10 or 20 < pe_ratio <= 25:
            score += 10
        elif 0 < pe_ratio < 5 or 25 < pe_ratio <= 30:
            score += 5

    # 5. PBRスコア（10点）: 低PBRを優遇
    pb_ratio = metrics['pb_ratio']
    if pb_ratio is not None:
        if pb_ratio < 1.0:
            score += 10
        elif pb_ratio < 1.5:
            score += 8
        elif pb_ratio < 2.0:
            score += 6
        elif pb_ratio < 3.0:
            score += 3

    # 6. 財務健全性スコア（20点）
    debt_to_equity = metrics['debt_to_equity']
    current_ratio = metrics['current_ratio']

    financial_score = 0

    # 負債資本比率（10点）
    if debt_to_equity is not None:
        if debt_to_equity < 50:
            financial_score += 10
        elif debt_to_equity < 100:
            financial_score += 7
        elif debt_to_equity < 150:
            financial_score += 4

    # 流動比率（10点）
    if current_ratio is not None:
        if current_ratio >= 2.0:
            financial_score += 10
        elif current_ratio >= 1.5:
            financial_score += 7
        elif current_ratio >= 1.0:
            financial_score += 4

    score += financial_score

    return score


# ===========================
# 4. メイン処理
# ===========================

def main():
    print("=" * 80)
    print("Phase 1 (簡易版): 400銘柄評価")
    print("=" * 80)
    print()

    # ステップ1: 既存評価データの統合
    existing_data = load_existing_evaluations()
    print(f"✅ 既存評価データ: {len(existing_data)}銘柄")
    print()

    # ステップ2: 追加銘柄の定量評価
    additional_results = []

    # 日本株 追加5銘柄
    print("📊 日本株の追加評価（5銘柄）...")
    japan_additional = get_additional_japan_stocks()
    for i, ticker in enumerate(japan_additional, 1):
        print(f"  [{i}/{len(japan_additional)}] {ticker}", end='\r')
        metrics = get_stock_metrics(ticker, market='JP')
        score = calculate_quantitative_score(metrics)
        metrics['final_score'] = score
        metrics['evaluation_type'] = 'quantitative'
        metrics['hayato'] = None
        metrics['researcher'] = None
        metrics['japanese'] = None
        metrics['sector'] = 'Unknown'
        additional_results.append(metrics)
        time.sleep(0.5)

    print()
    print(f"✅ 日本株追加評価完了: {len(japan_additional)}銘柄")
    print()

    # 米国株 TOP 100
    print("📊 米国株の定量評価（100銘柄）...")
    us_stocks = get_us_top100_stocks()
    for i, ticker in enumerate(us_stocks, 1):
        print(f"  [{i}/{len(us_stocks)}] {ticker}", end='\r')
        metrics = get_stock_metrics(ticker, market='US')
        score = calculate_quantitative_score(metrics)
        metrics['final_score'] = score
        metrics['evaluation_type'] = 'quantitative'
        metrics['hayato'] = None
        metrics['researcher'] = None
        metrics['japanese'] = None
        metrics['sector'] = 'US Stock'
        additional_results.append(metrics)
        time.sleep(0.5)

    print()
    print(f"✅ 米国株評価完了: {len(us_stocks)}銘柄")
    print()

    # ステップ3: データの統合
    print("🔄 データを統合中...")
    additional_df = pd.DataFrame(additional_results)

    # 既存データと統合
    all_data = pd.concat([existing_data, additional_df], ignore_index=True)

    # スコア順にソート
    all_data = all_data.sort_values('final_score', ascending=False).reset_index(drop=True)

    # ランク列を追加（既存のrank列があれば削除）
    if 'rank' in all_data.columns:
        all_data = all_data.drop(columns=['rank'])
    all_data.insert(0, 'rank', range(1, len(all_data) + 1))

    # CSV出力
    output_file = 'phase1_400stocks_combined.csv'
    all_data.to_csv(output_file, index=False, encoding='utf-8-sig')

    print("=" * 80)
    print("✅ Phase 1完了")
    print("=" * 80)
    print(f"📄 出力ファイル: {output_file}")
    print(f"📊 評価銘柄数: {len(all_data)}銘柄")
    print(f"  - 日本株: {len(all_data[all_data['market']=='JP'])}銘柄")
    print(f"  - 米国株: {len(all_data[all_data['market']=='US'])}銘柄")
    print(f"  - 3エージェント評価: {len(existing_data)}銘柄")
    print(f"  - 定量評価のみ: {len(additional_df)}銘柄")
    print()

    # サマリー統計
    print("📈 統合スコア分布:")
    print(f"  平均: {all_data['final_score'].mean():.2f}点")
    print(f"  中央値: {all_data['final_score'].median():.2f}点")
    print(f"  最高: {all_data['final_score'].max():.0f}点")
    print(f"  最低: {all_data['final_score'].min():.0f}点")
    print()

    # 市場別統計
    print("📊 市場別スコア:")
    print(f"  日本株: 平均 {all_data[all_data['market']=='JP']['final_score'].mean():.2f}点")
    print(f"  米国株: 平均 {all_data[all_data['market']=='US']['final_score'].mean():.2f}点")
    print()

    # TOP 10表示
    print("🏆 総合スコア TOP 10:")
    print("-" * 80)
    for _, row in all_data.head(10).iterrows():
        eval_type = "3agent" if row['evaluation_type'] == '3agent' else "quant"
        print(f"{row['rank']:3d}. [{row['market']}] {row['ticker']:10s} {row['name']:30s} {row['final_score']:5.1f}点 [{eval_type}]")
    print()

    # TOP 200抽出
    top200 = all_data.head(200)
    top200_file = 'phase2_top200_candidates.csv'
    top200.to_csv(top200_file, index=False, encoding='utf-8-sig')
    print(f"🎯 Phase 2候補 (TOP 200): {top200_file}")
    print()

    print("✨ 次のステップ:")
    print("  Phase 2: TOP 200銘柄のうち、定量評価のみの銘柄を3エージェント詳細評価")
    print("  （既存の3エージェント評価済み銘柄は再利用）")
    print()


if __name__ == '__main__':
    main()
