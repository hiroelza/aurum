#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
1000銘柄リストの生成
- 日本株500銘柄: 東証プライム市場の時価総額TOP 500
- 米国株500銘柄: S&P 500の全銘柄
"""

import pandas as pd
import yfinance as yf
import time

# ===========================
# 日本株500銘柄リスト
# ===========================

def generate_japan_500_tickers():
    """
    日本株500銘柄のティッカーリストを生成
    東証プライム市場の時価総額TOP 500を想定
    """

    # 日経225 + TOPIX 500の主要銘柄を手動リスト化
    # ※実際の運用では、証券取引所APIや金融データプロバイダーから取得

    japan_stocks = [
        # 超大型株 (時価総額 5兆円以上)
        '7203.T',   # トヨタ自動車
        '6758.T',   # ソニーグループ
        '9984.T',   # ソフトバンクグループ
        '6861.T',   # キーエンス
        '8306.T',   # 三菱UFJフィナンシャル・グループ
        '9433.T',   # KDDI
        '4063.T',   # 信越化学工業
        '6098.T',   # リクルートホールディングス
        '8035.T',   # 東京エレクトロン
        '9432.T',   # 日本電信電話
        '6501.T',   # 日立製作所
        '8058.T',   # 三菱商事
        '7974.T',   # 任天堂
        '8031.T',   # 三井物産
        '4502.T',   # 武田薬品工業

        # 大型株 (時価総額 1兆円以上)
        '6902.T',   # デンソー
        '4503.T',   # アステラス製薬
        '6954.T',   # ファナック
        '6367.T',   # ダイキン工業
        '4519.T',   # 中外製薬
        '6273.T',   # SMC
        '9735.T',   # セコム
        '6857.T',   # アドバンテスト
        '8001.T',   # 伊藤忠商事
        '8316.T',   # 三井住友フィナンシャルグループ
        '6971.T',   # 京セラ
        '4543.T',   # テルモ
        '6762.T',   # TDK
        '4661.T',   # オリエンタルランド
        '6976.T',   # 太陽誘電
        '6301.T',   # コマツ
        '2413.T',   # エムスリー
        '6645.T',   # オムロン
        '8053.T',   # 住友商事
        '6506.T',   # 安川電機
        '6326.T',   # クボタ
        '5108.T',   # ブリヂストン
        '7267.T',   # ホンダ
        '9434.T',   # ソフトバンク
        '6702.T',   # 富士通
        '6479.T',   # ミネベアミツミ
        '6503.T',   # 三菱電機
        '4452.T',   # 花王
        '6841.T',   # 横河電機
        '4704.T',   # トレンドマイクロ
        '7751.T',   # キヤノン
        '8411.T',   # みずほフィナンシャルグループ
        '8309.T',   # 三井住友トラスト・ホールディングス
        '8766.T',   # 東京海上ホールディングス
        '8604.T',   # 野村ホールディングス
        '7011.T',   # 三菱重工業
        '5401.T',   # 日本製鉄
        '6752.T',   # パナソニック ホールディングス
        '6981.T',   # 村田製作所
        '3382.T',   # セブン&アイ・ホールディングス
        '9101.T',   # 日本郵船
        '9107.T',   # 川崎汽船
        '9104.T',   # 商船三井
        '9020.T',   # JR東日本
        '9022.T',   # JR東海
        '5020.T',   # ENEOSホールディングス
        '3659.T',   # ネクソン
        '4911.T',   # 資生堂
        '4901.T',   # 富士フイルムホールディングス
        '7733.T',   # オリンパス
        '6920.T',   # レーザーテック
        '4324.T',   # 電通グループ
        '4188.T',   # 三菱ケミカルグループ
        '3086.T',   # J.フロント リテイリング
        '8252.T',   # 丸井グループ
        '6178.T',   # 日本郵政
        '4568.T',   # 第一三共

        # 中型株 (時価総額 1000億円以上)
        '6594.T',   # 日本電産
        '4324.T',   # 電通グループ
        '4523.T',   # エーザイ
        '4507.T',   # 塩野義製薬
        '8795.T',   # T&Dホールディングス
        '8725.T',   # MS&ADインシュアランスグループホールディングス
        '8750.T',   # 第一生命ホールディングス
        '8801.T',   # 三井不動産
        '8802.T',   # 三菱地所
        '3405.T',   # クラレ
        '4042.T',   # 東ソー
        '4183.T',   # 三井化学
        '4005.T',   # 住友化学
        '5202.T',   # 日本板硝子
        '5214.T',   # 日本電気硝子
        '5333.T',   # 日本碍子
        '5711.T',   # 三菱マテリアル
        '5713.T',   # 住友金属鉱山
        '5801.T',   # 古河電気工業
        '5802.T',   # 住友電気工業
        '7201.T',   # 日産自動車
        '7202.T',   # いすゞ自動車
        '7269.T',   # スズキ
        '7270.T',   # SUBARU
        '7272.T',   # ヤマハ発動機
        '9005.T',   # 東急
        '9007.T',   # 小田急電鉄
        '9008.T',   # 京王電鉄
        '9009.T',   # 京成電鉄
        '9001.T',   # 東武鉄道
        '9064.T',   # ヤマトホールディングス
        '9062.T',   # 日本通運
        '9613.T',   # NTTデータ
        '4755.T',   # 楽天グループ
        '9602.T',   # 東宝
        '2802.T',   # 味の素
        '2801.T',   # キッコーマン
        '2502.T',   # アサヒグループホールディングス
        '2503.T',   # キリンホールディングス
        '2914.T',   # JT
        '3401.T',   # 帝人
        '3402.T',   # 東レ

        # 以下、500銘柄まで拡張（一部省略）
        # 実際の運用では、証券取引所のAPIから時価総額順に取得
    ]

    # 重複削除
    japan_stocks = list(set(japan_stocks))

    # 500銘柄に満たない場合、追加
    if len(japan_stocks) < 500:
        # TOPIX 500の残りの銘柄を追加
        # ※ここでは簡略化のため、実際の銘柄リストは外部データソースから取得
        print(f"⚠️ 日本株が{len(japan_stocks)}銘柄のみです。")
        print(f"   残り{500 - len(japan_stocks)}銘柄は外部データソースから取得してください。")

    return japan_stocks[:500]


# ===========================
# 米国株500銘柄リスト (S&P 500)
# ===========================

def generate_us_sp500_tickers():
    """
    S&P 500の全銘柄リストを生成
    """

    # S&P 500の主要銘柄（実際は500銘柄）
    sp500_stocks = [
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

        # Mid Cap
        'APD',    # Air Products and Chemicals
        'ICE',    # Intercontinental Exchange
        'SLB',    # Schlumberger
        'WM',     # Waste Management
        'CME',    # CME Group
        'PH',     # Parker-Hannifin
        'FISV',   # Fiserv
        'ITW',    # Illinois Tool Works
        'AON',    # Aon
        'MCO',    # Moody's
        'EMR',    # Emerson Electric
        'APH',    # Amphenol
        'TGT',    # Target
        'ROP',    # Roper Technologies
        'PYPL',   # PayPal
        'ATVI',   # Activision Blizzard
        'AMAT',   # Applied Materials
        'ADI',    # Analog Devices
        'LRCX',   # Lam Research
        'KLAC',   # KLA Corporation
        'NXPI',   # NXP Semiconductors
        'MCHP',   # Microchip Technology
        'SNPS',   # Synopsys
        'CDNS',   # Cadence Design Systems
        'ADSK',   # Autodesk
        'PAYX',   # Paychex
        'ROST',   # Ross Stores
        'FAST',   # Fastenal
        'VRSK',   # Verisk Analytics
        'CTAS',   # Cintas
        'ORLY',   # O'Reilly Automotive
        'AZO',    # AutoZone
        'MSCI',   # MSCI
        'CMG',    # Chipotle Mexican Grill
        'EA',     # Electronic Arts
        'IDXX',   # IDEXX Laboratories
        'MKTX',   # MarketAxess Holdings
        'ANSS',   # ANSYS
        'FTNT',   # Fortinet
        'CTSH',   # Cognizant Technology Solutions
        'PAYX',   # Paychex
        'PCAR',   # PACCAR
        'KMB',    # Kimberly-Clark
        'GIS',    # General Mills
        'HSY',    # Hershey
        'SYY',    # Sysco
        'MKC',    # McCormick & Company
        'K',      # Kellogg
        'HRL',    # Hormel Foods
        'CLX',    # Clorox
        'TSN',    # Tyson Foods
        'CAH',    # Cardinal Health
        'MCK',    # McKesson
        'CNC',    # Centene
        'HUM',    # Humana
        'BIIB',   # Biogen
        'IQV',    # IQVIA Holdings
        'A',      # Agilent Technologies
        'MTD',    # Mettler-Toledo
        'PKI',    # PerkinElmer
        'WAT',    # Waters Corporation

        # 以下、500銘柄まで拡張
        # 実際のS&P 500は全500銘柄をカバー
    ]

    # 重複削除
    sp500_stocks = list(set(sp500_stocks))

    if len(sp500_stocks) < 500:
        print(f"⚠️ 米国株が{len(sp500_stocks)}銘柄のみです。")
        print(f"   残り{500 - len(sp500_stocks)}銘柄はS&P 500公式リストから取得してください。")

    return sp500_stocks[:500]


# ===========================
# CSVファイルの生成
# ===========================

def main():
    print("=" * 80)
    print("1000銘柄リストの生成")
    print("=" * 80)
    print()

    # 日本株500銘柄
    japan_tickers = generate_japan_500_tickers()
    print(f"✅ 日本株: {len(japan_tickers)}銘柄")

    # 米国株500銘柄
    us_tickers = generate_us_sp500_tickers()
    print(f"✅ 米国株: {len(us_tickers)}銘柄")

    print(f"✅ 合計: {len(japan_tickers) + len(us_tickers)}銘柄")
    print()

    # DataFrameに変換
    japan_df = pd.DataFrame({
        'ticker': japan_tickers,
        'market': 'JP'
    })

    us_df = pd.DataFrame({
        'ticker': us_tickers,
        'market': 'US'
    })

    # 結合
    all_stocks = pd.concat([japan_df, us_df], ignore_index=True)

    # CSV出力
    output_file = 'stocks_1000_master_list.csv'
    all_stocks.to_csv(output_file, index=False, encoding='utf-8-sig')

    print(f"📄 出力ファイル: {output_file}")
    print()
    print("🎯 次のステップ:")
    print("  1. このリストをもとにphase1_quantitative_screening.pyを実行")
    print("  2. 定量評価スコアを算出")
    print()


if __name__ == '__main__':
    main()
