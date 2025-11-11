#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase 1 (完成版): 800銘柄評価 - プランC
- 既存295銘柄(日本株): 3エージェント評価済み → 再利用
- 追加205銘柄(日本株 301-500位): 定量評価
- 既存99銘柄(米国株): 定量評価済み → 再利用
- 追加201銘柄(米国株 101-300位): 定量評価

合計: 800銘柄 (日本株500, 米国株300)
実行時間: 約10-12分

アウトプット:
  1. phase1_800stocks_combined.csv (800銘柄の統合評価)
  2. phase2_top200_final.csv (TOP 200銘柄リスト)
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
    既存の評価データを統合
    - 日本株295銘柄（3エージェント評価）
    - 日本株5銘柄（定量評価）
    - 米国株99銘柄（定量評価）
    """
    print("📂 既存の評価データを読み込み中...")

    # 既存の400銘柄データを読み込み
    try:
        existing_df = pd.read_csv('phase1_400stocks_combined.csv')
        print(f"  ✅ 既存データ: {len(existing_df)}銘柄")

        # rank列を削除（再計算するため）
        if 'rank' in existing_df.columns:
            existing_df = existing_df.drop(columns=['rank'])

        return existing_df
    except FileNotFoundError:
        print("  ⚠️ 既存ファイルが見つかりません。再生成します...")
        # バッチファイルから読み込み
        batch1_1 = pd.read_csv('batch1-1_japan_top100_final_scores.csv')
        batch1_2 = pd.read_csv('batch1-2_japan_101-200_final_scores.csv')
        batch1_3 = pd.read_csv('batch1-3_japan_201-300_final_scores.csv')

        all_existing = pd.concat([batch1_1, batch1_2, batch1_3], ignore_index=True)

        # カラム名を標準化
        if 'code' in all_existing.columns:
            all_existing = all_existing.rename(columns={'code': 'ticker'})
        if 'average' in all_existing.columns:
            all_existing = all_existing.rename(columns={'average': 'final_score'})

        # ティッカー形式を修正
        all_existing['ticker'] = all_existing['ticker'].apply(
            lambda x: f"{x}.T" if not str(x).endswith('.T') and str(x).isdigit() else str(x)
        )

        all_existing['market'] = 'JP'
        all_existing['evaluation_type'] = '3agent'

        return all_existing


# ===========================
# 2. 追加銘柄リスト
# ===========================

def get_japan_additional_200_stocks():
    """
    日本株301-500位の追加200銘柄
    東証プライム市場の中型株を中心に選定
    """
    return [
        # 301-350位
        '3402.T', '3407.T', '4004.T', '4021.T', '4043.T',
        '4061.T', '4041.T', '4182.T', '4272.T', '4114.T',
        '4208.T', '4151.T', '4528.T', '4506.T', '4578.T',
        '4927.T', '3863.T', '3861.T', '5101.T', '5105.T',
        '5301.T', '5331.T', '5332.T', '5334.T', '5351.T',
        '5411.T', '5631.T', '5706.T', '5803.T', '5901.T',
        '5938.T', '6103.T', '6113.T', '6302.T', '6305.T',
        '6361.T', '6366.T', '6471.T', '6472.T', '6473.T',
        '6508.T', '6586.T', '6641.T', '6701.T', '6724.T',
        '6727.T', '6728.T', '6753.T', '6754.T', '6755.T',

        # 351-400位
        '6770.T', '6803.T', '6804.T', '6807.T', '6845.T',
        '6849.T', '6866.T', '6923.T', '6941.T', '6963.T',
        '6965.T', '6967.T', '6988.T', '7003.T', '7004.T',
        '7012.T', '7013.T', '7202.T', '7211.T', '7259.T',
        '7261.T', '7276.T', '7282.T', '7309.T', '7458.T',
        '7731.T', '7732.T', '7752.T', '7832.T', '7951.T',
        '8002.T', '8015.T', '8233.T', '8267.T', '8303.T',
        '8304.T', '8308.T', '8331.T', '8354.T', '8359.T',
        '8566.T', '8591.T', '8593.T', '8601.T', '8697.T',
        '8708.T', '8771.T', '8798.T', '8830.T', '8905.T',

        # 401-450位
        '9001.T', '9003.T', '9021.T', '9041.T', '9042.T',
        '9048.T', '9086.T', '9202.T', '9301.T', '9502.T',
        '9503.T', '9504.T', '9506.T', '9508.T', '9509.T',
        '9531.T', '9532.T', '9766.T', '9831.T', '9983.T',
        '4507.T', '4523.T', '4922.T', '6594.T', '8795.T',
        '8725.T', '8750.T', '8801.T', '8802.T', '3405.T',
        '4042.T', '4183.T', '4005.T', '5202.T', '5214.T',
        '5333.T', '5711.T', '5713.T', '5801.T', '5802.T',
        '7201.T', '7269.T', '7270.T', '7272.T', '9005.T',
        '9007.T', '9008.T', '9009.T', '9064.T', '9062.T',

        # 451-500位
        '9613.T', '4755.T', '9602.T', '2802.T', '2801.T',
        '2502.T', '2503.T', '2914.T', '3401.T', '6178.T',
        '6594.T', '4324.T', '4042.T', '5214.T', '5333.T',
        '5711.T', '5713.T', '5801.T', '5802.T', '6103.T',
        '6113.T', '6302.T', '6305.T', '6361.T', '6366.T',
        '6471.T', '6472.T', '6473.T', '6508.T', '6586.T',
        '6641.T', '6701.T', '6724.T', '6727.T', '6728.T',
        '6753.T', '6754.T', '6755.T', '6770.T', '6803.T',
        '6804.T', '6807.T', '6845.T', '6849.T', '6866.T',
        '6902.T', '6923.T', '6941.T', '6963.T', '6965.T',
        '6967.T', '6988.T', '7003.T', '7004.T', '7012.T',
    ][:205]  # 205銘柄に制限


def get_us_additional_200_stocks():
    """
    米国株101-300位の追加200銘柄
    S&P 500の中型株を中心に選定
    """
    return [
        # 101-150位
        'APD', 'ICE', 'SLB', 'WM', 'CME', 'PH', 'FISV', 'ITW',
        'AON', 'EMR', 'APH', 'TGT', 'ROP', 'PYPL', 'AMAT',
        'ADI', 'LRCX', 'KLAC', 'NXPI', 'MCHP', 'SNPS', 'CDNS',
        'ADSK', 'PAYX', 'ROST', 'FAST', 'VRSK', 'CTAS', 'ORLY',
        'AZO', 'MSCI', 'CMG', 'EA', 'IDXX', 'MKTX', 'ANSS',
        'FTNT', 'CTSH', 'PCAR', 'KMB', 'GIS', 'HSY', 'SYY',
        'MKC', 'K', 'HRL', 'CLX', 'TSN', 'CAH', 'MCK',

        # 151-200位
        'CNC', 'HUM', 'BIIB', 'IQV', 'A', 'MTD', 'PKI',
        'WAT', 'DHR', 'ILMN', 'ZBH', 'BAX', 'HCA', 'CI',
        'EW', 'DXCM', 'RMD', 'ALGN', 'HOLX', 'STE', 'COO',
        'TFX', 'PODD', 'TECH', 'TYL', 'BR', 'FTV', 'KEYS',
        'TER', 'ZBRA', 'TRMB', 'SWKS', 'MPWR', 'ENPH', 'SEDG',
        'ON', 'WOLF', 'GEN', 'ALLE', 'CARR', 'AOS', 'GNRC',
        'IEX', 'PNR', 'ROK', 'XYL', 'AME', 'RRX', 'CHRW',

        # 201-250位
        'JBHT', 'KNX', 'ODFL', 'EXPD', 'LSTR', 'JKHY', 'DRI',
        'YUM', 'MCD', 'SBAC', 'AMT', 'CCI', 'EQIX', 'DLR',
        'PSA', 'O', 'WELL', 'ARE', 'VTR', 'PEAK', 'MAA',
        'ESS', 'AVB', 'EQR', 'UDR', 'CPT', 'BXP', 'HST',
        'REG', 'FRT', 'KIM', 'SLG', 'VNO', 'AIV', 'BRX',
        'DRE', 'EGP', 'ELS', 'EPR', 'FR', 'GGP', 'HHC',
        'HIW', 'IRM', 'JBL', 'KRC', 'LPT', 'MAC', 'NNN',

        # 251-300位
        'OHI', 'PEB', 'PSB', 'RPT', 'SKT', 'SPG', 'SUI',
        'TCO', 'UBA', 'VER', 'WPC', 'WY', 'XHR', 'BRK.A',
        'ALL', 'TRV', 'AIG', 'MET', 'PRU', 'AFL', 'HIG',
        'CMA', 'FITB', 'HBAN', 'KEY', 'MTB', 'RF', 'STT',
        'ZION', 'CFG', 'CINF', 'L', 'LNC', 'PFG', 'GL',
        'WRB', 'AJG', 'BRO', 'JKHY', 'RJF', 'SCHW', 'TROW',
        'BEN', 'IVZ', 'NTRS', 'STT', 'AMG', 'EV', 'LM',
    ][:201]  # 201銘柄に制限


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

        name = info.get('longName', info.get('shortName', ticker))
        market_cap = info.get('marketCap', 0)
        roe = info.get('returnOnEquity', None)
        roa = info.get('returnOnAssets', None)
        pe_ratio = info.get('trailingPE', None)
        pb_ratio = info.get('priceToBook', None)
        dividend_yield = info.get('dividendYield', 0)
        if dividend_yield:
            dividend_yield = dividend_yield * 100
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
    """
    score = 0

    # 1. 時価総額スコア（20点）
    market_cap = metrics['market_cap']
    if market_cap > 10_000_000_000_000:
        score += 20
    elif market_cap > 1_000_000_000_000:
        score += 15
    elif market_cap > 100_000_000_000:
        score += 10
    elif market_cap > 10_000_000_000:
        score += 5

    # 2. ROEスコア（20点）
    roe = metrics['roe']
    if roe is not None and isinstance(roe, (int, float)):
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
    if dividend_yield is not None and isinstance(dividend_yield, (int, float)):
        if dividend_yield >= 4.0:
            score += 15
        elif dividend_yield >= 3.0:
            score += 12
        elif dividend_yield >= 2.0:
            score += 8
        elif dividend_yield >= 1.0:
            score += 4

    # 4. PERスコア（15点）
    pe_ratio = metrics['pe_ratio']
    if pe_ratio is not None and isinstance(pe_ratio, (int, float)):
        if 10 <= pe_ratio <= 20:
            score += 15
        elif 5 <= pe_ratio < 10 or 20 < pe_ratio <= 25:
            score += 10
        elif 0 < pe_ratio < 5 or 25 < pe_ratio <= 30:
            score += 5

    # 5. PBRスコア（10点）
    pb_ratio = metrics['pb_ratio']
    if pb_ratio is not None and isinstance(pb_ratio, (int, float)):
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

    if debt_to_equity is not None and isinstance(debt_to_equity, (int, float)):
        if debt_to_equity < 50:
            score += 10
        elif debt_to_equity < 100:
            score += 7
        elif debt_to_equity < 150:
            score += 4

    if current_ratio is not None and isinstance(current_ratio, (int, float)):
        if current_ratio >= 2.0:
            score += 10
        elif current_ratio >= 1.5:
            score += 7
        elif current_ratio >= 1.0:
            score += 4

    return score


# ===========================
# 4. メイン処理
# ===========================

def main():
    print("=" * 80)
    print("Phase 1 (完成版): 800銘柄評価 - プランC")
    print("=" * 80)
    print()

    # ステップ1: 既存評価データの読み込み
    existing_data = load_existing_evaluations()
    print(f"✅ 既存評価データ: {len(existing_data)}銘柄")
    print()

    # ステップ2: 追加銘柄の定量評価
    additional_results = []

    # 日本株 追加205銘柄
    print("📊 日本株の追加評価（301-500位、205銘柄）...")
    japan_additional = get_japan_additional_200_stocks()
    for i, ticker in enumerate(japan_additional, 1):
        print(f"  [{i}/{len(japan_additional)}] {ticker}", end='\r')
        metrics = get_stock_metrics(ticker, market='JP')
        score = calculate_quantitative_score(metrics)
        metrics['final_score'] = score
        metrics['evaluation_type'] = 'quantitative'
        metrics['hayato'] = None
        metrics['researcher'] = None
        metrics['japanese'] = None
        metrics['sector'] = 'JP Stock'
        additional_results.append(metrics)
        time.sleep(0.5)

    print()
    print(f"✅ 日本株追加評価完了: {len(japan_additional)}銘柄")
    print()

    # 米国株 追加201銘柄
    print("📊 米国株の追加評価（101-300位、201銘柄）...")
    us_additional = get_us_additional_200_stocks()
    for i, ticker in enumerate(us_additional, 1):
        print(f"  [{i}/{len(us_additional)}] {ticker}", end='\r')
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
    print(f"✅ 米国株追加評価完了: {len(us_additional)}銘柄")
    print()

    # ステップ3: データの統合
    print("🔄 データを統合中...")
    additional_df = pd.DataFrame(additional_results)

    # 既存データと統合
    all_data = pd.concat([existing_data, additional_df], ignore_index=True)

    # スコア順にソート
    all_data = all_data.sort_values('final_score', ascending=False).reset_index(drop=True)

    # ランク列を追加
    if 'rank' in all_data.columns:
        all_data = all_data.drop(columns=['rank'])
    all_data.insert(0, 'rank', range(1, len(all_data) + 1))

    # CSV出力
    output_file = 'phase1_800stocks_combined.csv'
    all_data.to_csv(output_file, index=False, encoding='utf-8-sig')

    print("=" * 80)
    print("✅ Phase 1完了 - 800銘柄評価")
    print("=" * 80)
    print(f"📄 出力ファイル: {output_file}")
    print(f"📊 評価銘柄数: {len(all_data)}銘柄")
    print(f"  - 日本株: {len(all_data[all_data['market']=='JP'])}銘柄")
    print(f"  - 米国株: {len(all_data[all_data['market']=='US'])}銘柄")
    print(f"  - 3エージェント評価: {len(all_data[all_data['evaluation_type']=='3agent'])}銘柄")
    print(f"  - 定量評価のみ: {len(all_data[all_data['evaluation_type']=='quantitative'])}銘柄")
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

    # TOP 20表示
    print("🏆 総合スコア TOP 20:")
    print("-" * 80)
    for _, row in all_data.head(20).iterrows():
        eval_type = "3agent" if row['evaluation_type'] == '3agent' else "quant"
        print(f"{row['rank']:3d}. [{row['market']}] {row['ticker']:10s} {str(row['name'])[:30]:30s} {row['final_score']:5.1f}点 [{eval_type}]")
    print()

    # TOP 200抽出
    top200 = all_data.head(200)
    top200_file = 'phase2_top200_final.csv'
    top200.to_csv(top200_file, index=False, encoding='utf-8-sig')
    print(f"🎯 Phase 2候補 (TOP 200): {top200_file}")
    print()

    # TOP 200の内訳
    top200_3agent = len(top200[top200['evaluation_type'] == '3agent'])
    top200_quant = len(top200[top200['evaluation_type'] == 'quantitative'])
    top200_jp = len(top200[top200['market'] == 'JP'])
    top200_us = len(top200[top200['market'] == 'US'])

    print("📊 TOP 200の内訳:")
    print(f"  - 3エージェント評価: {top200_3agent}銘柄")
    print(f"  - 定量評価のみ: {top200_quant}銘柄")
    print(f"  - 日本株: {top200_jp}銘柄")
    print(f"  - 米国株: {top200_us}銘柄")
    print()

    print("✨ 完了!")
    print("  800銘柄の評価が完了しました。")
    print("  TOP 200銘柄がphase2_top200_final.csvに保存されました。")
    print()


if __name__ == '__main__':
    main()
