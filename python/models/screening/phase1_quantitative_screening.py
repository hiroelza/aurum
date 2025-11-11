#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase 1: 定量スクリーニング（1000銘柄）
- 日本株500銘柄 + 米国株500銘柄 = 1000銘柄
- 定量指標のみで自動評価（トークン消費ゼロ）
- 評価項目: 時価総額、ROE、配当利回り、PER/PBR、財務健全性
- 出力: phase1_quantitative_scores_1000stocks.csv
"""

import pandas as pd
import yfinance as yf
import time
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# ===========================
# 1. 銘柄リストの準備
# ===========================

def get_japan_top500_tickers():
    """
    日本株時価総額TOP 500のティッカーシンボルを取得
    実際には東証プライム市場の主要銘柄を想定
    """
    # 日本株TOP 500のティッカーリスト（東証コード.T形式）
    # 実際には、日経225 + TOPIX Core30 + その他主要銘柄で500銘柄を構成

    # 日経225銘柄（一部抜粋、実際は225銘柄）
    nikkei225_base = [
        '7203.T',  # トヨタ自動車
        '6758.T',  # ソニーグループ
        '9984.T',  # ソフトバンクグループ
        '6861.T',  # キーエンス
        '8306.T',  # 三菱UFJフィナンシャル・グループ
        '9433.T',  # KDDI
        '4063.T',  # 信越化学工業
        '4502.T',  # 武田薬品工業
        '6098.T',  # リクルートホールディングス
        '8035.T',  # 東京エレクトロン
        '6902.T',  # デンソー
        '4503.T',  # アステラス製薬
        '9432.T',  # 日本電信電話
        '6954.T',  # ファナック
        '6501.T',  # 日立製作所
        '8031.T',  # 三井物産
        '4568.T',  # 第一三共
        '8058.T',  # 三菱商事
        '7974.T',  # 任天堂
        '6367.T',  # ダイキン工業
        '4519.T',  # 中外製薬
        '6273.T',  # SMC
        '9735.T',  # セコム
        '6857.T',  # アドバンテスト
        '8001.T',  # 伊藤忠商事
        '8316.T',  # 三井住友フィナンシャルグループ
        '6971.T',  # 京セラ
        '4543.T',  # テルモ
        '6762.T',  # TDK
        '6141.T',  # DMG森精機
        '4661.T',  # オリエンタルランド
        '6976.T',  # 太陽誘電
        '6301.T',  # コマツ
        '2413.T',  # エムスリー
        '6645.T',  # オムロン
        '6952.T',  # カシオ計算機
        '8053.T',  # 住友商事
        '6506.T',  # 安川電機
        '6326.T',  # クボタ
        '5108.T',  # ブリヂストン
        '7267.T',  # ホンダ
        '9434.T',  # ソフトバンク
        '6702.T',  # 富士通
        '6479.T',  # ミネベアミツミ
        '6503.T',  # 三菱電機
        '4452.T',  # 花王
        '6841.T',  # 横河電機
        '4704.T',  # トレンドマイクロ
        '6178.T',  # 日本郵政
        '7751.T',  # キヤノン
        # 以下、100銘柄まで拡張（実際は500銘柄）
    ]

    # TOPIX 100に含まれる主要銘柄を追加
    topix_additional = [
        '8411.T',  # みずほフィナンシャルグループ
        '8309.T',  # 三井住友トラスト・ホールディングス
        '8766.T',  # 東京海上ホールディングス
        '8604.T',  # 野村ホールディングス
        '7011.T',  # 三菱重工業
        '5401.T',  # 日本製鉄
        '6752.T',  # パナソニック ホールディングス
        '6981.T',  # 村田製作所
        '3382.T',  # セブン&アイ・ホールディングス
        '9101.T',  # 日本郵船
        '9107.T',  # 川崎汽船
        '9104.T',  # 商船三井
        '9020.T',  # JR東日本
        '9022.T',  # JR東海
        '5020.T',  # ENEOS ホールディングス
        '3659.T',  # ネクソン
        '4911.T',  # 資生堂
        '4901.T',  # 富士フイルムホールディングス
        '7733.T',  # オリンパス
        '6920.T',  # レーザーテック
        '4324.T',  # 電通グループ
        '4188.T',  # 三菱ケミカルグループ
        '6479.T',  # ミネベアミツミ
        '3086.T',  # J.フロント リテイリング
        '8252.T',  # 丸井グループ
    ]

    # 東証プライム主要銘柄をさらに追加（計500銘柄を目指す）
    # ※実際の運用では、時価総額ランキングTOP500を取得するAPIを使用
    # ここでは代表的な銘柄を手動で列挙（簡略化のため100銘柄程度に限定）

    japan_500 = nikkei225_base + topix_additional

    # 重複削除
    japan_500 = list(set(japan_500))

    # 500銘柄に満たない場合、追加銘柄を生成（ダミーデータとして）
    # 実際の運用では、証券会社APIやスクレイピングで取得
    if len(japan_500) < 500:
        print(f"⚠️ 日本株リストが{len(japan_500)}銘柄しかありません。500銘柄に拡張してください。")

    return japan_500[:500]  # 最大500銘柄


def get_us_sp500_tickers():
    """
    米国S&P 500銘柄のティッカーシンボルを取得
    """
    # S&P 500の代表的な銘柄（実際は500銘柄）
    sp500_base = [
        'AAPL',   # Apple
        'MSFT',   # Microsoft
        'GOOGL',  # Alphabet (Google)
        'AMZN',   # Amazon
        'NVDA',   # NVIDIA
        'TSLA',   # Tesla
        'META',   # Meta (Facebook)
        'BRK.B',  # Berkshire Hathaway
        'V',      # Visa
        'UNH',    # UnitedHealth
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
        'TMO',    # Thermo Fisher
        'ADBE',   # Adobe
        'ACN',    # Accenture
        'CSCO',   # Cisco
        'NKE',    # Nike
        'ABT',    # Abbott
        'DIS',    # Disney
        'CRM',    # Salesforce
        'VZ',     # Verizon
        'CMCSA',  # Comcast
        'NFLX',   # Netflix
        'INTC',   # Intel
        'AMD',    # AMD
        'QCOM',   # Qualcomm
        'TXN',    # Texas Instruments
        'UNP',    # Union Pacific
        'PM',     # Philip Morris
        'BA',     # Boeing
        'UPS',    # UPS
        'HON',    # Honeywell
        'SBUX',   # Starbucks
        'IBM',    # IBM
        'GE',     # General Electric
        'CAT',    # Caterpillar
        'MMM',    # 3M
        'GS',     # Goldman Sachs
        # 以下、100銘柄まで拡張（実際は500銘柄）
    ]

    # NASDAQ 100の主要銘柄を追加
    nasdaq_additional = [
        'GOOG',   # Alphabet Class C
        'ASML',   # ASML
        'AZN',    # AstraZeneca
        'ORCL',   # Oracle
        'COP',    # ConocoPhillips
        'NEE',    # NextEra Energy
        'LLY',    # Eli Lilly
        'RTX',    # Raytheon
        'LOW',    # Lowe's
        'MDT',    # Medtronic
        'SPGI',   # S&P Global
        'INTU',   # Intuit
        'ISRG',   # Intuitive Surgical
        'ADP',    # ADP
        'BLK',    # BlackRock
        'TJX',    # TJX Companies
        'BKNG',   # Booking Holdings
        'GILD',   # Gilead Sciences
        'AMGN',   # Amgen
        'VRTX',   # Vertex Pharmaceuticals
        'CI',     # Cigna
        'MDLZ',   # Mondelez
        'MO',     # Altria
        'SYK',    # Stryker
        'REGN',   # Regeneron
    ]

    us_500 = sp500_base + nasdaq_additional
    us_500 = list(set(us_500))

    if len(us_500) < 500:
        print(f"⚠️ 米国株リストが{len(us_500)}銘柄しかありません。500銘柄に拡張してください。")

    return us_500[:500]


# ===========================
# 2. 定量指標の取得
# ===========================

def get_stock_metrics(ticker, market='JP'):
    """
    個別銘柄の定量指標を取得

    Args:
        ticker: ティッカーシンボル
        market: 'JP' (日本株) or 'US' (米国株)

    Returns:
        dict: 定量指標の辞書
    """
    try:
        stock = yf.Ticker(ticker)
        info = stock.info

        # 基本情報
        name = info.get('longName', ticker)
        market_cap = info.get('marketCap', 0)

        # 収益性指標
        roe = info.get('returnOnEquity', None)  # ROE（自己資本利益率）
        roa = info.get('returnOnAssets', None)  # ROA（総資産利益率）

        # バリュエーション指標
        pe_ratio = info.get('trailingPE', None)  # PER（株価収益率）
        pb_ratio = info.get('priceToBook', None)  # PBR（株価純資産倍率）

        # 配当指標
        dividend_yield = info.get('dividendYield', 0)  # 配当利回り
        if dividend_yield:
            dividend_yield = dividend_yield * 100  # パーセント表示

        # 財務健全性
        debt_to_equity = info.get('debtToEquity', None)  # 負債資本比率
        current_ratio = info.get('currentRatio', None)  # 流動比率

        # 成長性
        revenue_growth = info.get('revenueGrowth', None)  # 売上成長率
        earnings_growth = info.get('earningsGrowth', None)  # 利益成長率

        return {
            'ticker': ticker,
            'name': name,
            'market': market,
            'market_cap': market_cap,
            'roe': roe * 100 if roe else None,  # パーセント表示
            'roa': roa * 100 if roa else None,
            'pe_ratio': pe_ratio,
            'pb_ratio': pb_ratio,
            'dividend_yield': dividend_yield,
            'debt_to_equity': debt_to_equity,
            'current_ratio': current_ratio,
            'revenue_growth': revenue_growth * 100 if revenue_growth else None,
            'earnings_growth': earnings_growth * 100 if earnings_growth else None,
        }

    except Exception as e:
        print(f"❌ エラー: {ticker} - {str(e)}")
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
            'revenue_growth': None,
            'earnings_growth': None,
        }


# ===========================
# 3. 定量スコアの算出
# ===========================

def calculate_quantitative_score(metrics):
    """
    定量指標からスコア（0-100点）を算出

    評価項目:
    1. 時価総額（20点）: 大型株を優遇
    2. ROE（20点）: 高ROEを優遇
    3. 配当利回り（15点）: 高配当を優遇
    4. PER（15点）: 適正水準（10-20倍）を優遇
    5. PBR（10点）: 低PBRを優遇
    6. 財務健全性（20点）: 低負債、高流動比率を優遇

    合計: 100点満点
    """
    score = 0

    # 1. 時価総額スコア（20点）
    market_cap = metrics['market_cap']
    if market_cap > 10_000_000_000_000:  # 10兆円以上
        score += 20
    elif market_cap > 1_000_000_000_000:  # 1兆円以上
        score += 15
    elif market_cap > 100_000_000_000:  # 1000億円以上
        score += 10
    elif market_cap > 10_000_000_000:  # 100億円以上
        score += 5
    else:
        score += 0

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
        else:
            score += 0

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
        else:
            score += 0

    # 4. PERスコア（15点）: 10-20倍が理想
    pe_ratio = metrics['pe_ratio']
    if pe_ratio is not None:
        if 10 <= pe_ratio <= 20:
            score += 15
        elif 5 <= pe_ratio < 10 or 20 < pe_ratio <= 25:
            score += 10
        elif 0 < pe_ratio < 5 or 25 < pe_ratio <= 30:
            score += 5
        else:
            score += 0

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
        else:
            score += 0

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
        else:
            financial_score += 0

    # 流動比率（10点）
    if current_ratio is not None:
        if current_ratio >= 2.0:
            financial_score += 10
        elif current_ratio >= 1.5:
            financial_score += 7
        elif current_ratio >= 1.0:
            financial_score += 4
        else:
            financial_score += 0

    score += financial_score

    return score


# ===========================
# 4. メイン処理
# ===========================

def main():
    print("=" * 80)
    print("Phase 1: 定量スクリーニング（1000銘柄）")
    print("=" * 80)
    print()

    # 銘柄リストの準備
    print("📋 銘柄リストを準備中...")
    japan_tickers = get_japan_top500_tickers()
    us_tickers = get_us_sp500_tickers()

    print(f"✅ 日本株: {len(japan_tickers)}銘柄")
    print(f"✅ 米国株: {len(us_tickers)}銘柄")
    print(f"✅ 合計: {len(japan_tickers) + len(us_tickers)}銘柄")
    print()

    # データ取得
    all_results = []

    print("📊 定量指標を取得中...")
    print()

    # 日本株の処理
    print("🇯🇵 日本株を評価中...")
    for i, ticker in enumerate(japan_tickers, 1):
        print(f"  [{i}/{len(japan_tickers)}] {ticker}", end='\r')
        metrics = get_stock_metrics(ticker, market='JP')
        score = calculate_quantitative_score(metrics)
        metrics['quantitative_score'] = score
        all_results.append(metrics)
        time.sleep(0.5)  # API制限対策

    print()
    print(f"✅ 日本株 {len(japan_tickers)}銘柄の評価完了")
    print()

    # 米国株の処理
    print("🇺🇸 米国株を評価中...")
    for i, ticker in enumerate(us_tickers, 1):
        print(f"  [{i}/{len(us_tickers)}] {ticker}", end='\r')
        metrics = get_stock_metrics(ticker, market='US')
        score = calculate_quantitative_score(metrics)
        metrics['quantitative_score'] = score
        all_results.append(metrics)
        time.sleep(0.5)  # API制限対策

    print()
    print(f"✅ 米国株 {len(us_tickers)}銘柄の評価完了")
    print()

    # DataFrameに変換
    df = pd.DataFrame(all_results)

    # スコア順にソート
    df = df.sort_values('quantitative_score', ascending=False)

    # CSV出力
    output_file = 'phase1_quantitative_scores_1000stocks.csv'
    df.to_csv(output_file, index=False, encoding='utf-8-sig')

    print("=" * 80)
    print("✅ Phase 1完了")
    print("=" * 80)
    print(f"📄 出力ファイル: {output_file}")
    print(f"📊 評価銘柄数: {len(df)}銘柄")
    print()

    # サマリー統計
    print("📈 定量スコア分布:")
    print(f"  平均: {df['quantitative_score'].mean():.2f}点")
    print(f"  中央値: {df['quantitative_score'].median():.2f}点")
    print(f"  最高: {df['quantitative_score'].max():.0f}点")
    print(f"  最低: {df['quantitative_score'].min():.0f}点")
    print()

    # TOP 10表示
    print("🏆 定量スコア TOP 10:")
    print("-" * 80)
    top10 = df.head(10)
    for i, row in top10.iterrows():
        print(f"{row.name + 1:3d}. {row['ticker']:10s} {row['name']:30s} {row['quantitative_score']:3.0f}点")
    print()

    print("🎯 次のステップ:")
    print("  Phase 2: TOP 200銘柄の詳細評価（3エージェント）")
    print("  - 既存295銘柄と定量スコアTOPを合わせてTOP 200を選定")
    print()


if __name__ == '__main__':
    main()
