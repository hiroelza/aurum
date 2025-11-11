#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase 1 (完全版): 1,101銘柄評価 - 成長分野特化
- 既存801銘柄: 再利用
- 追加300銘柄: 成長分野から選定
  - 日本株150銘柄（成長分野）
  - 米国株150銘柄（成長分野）

合計: 1,101銘柄 (日本株655, 米国株446)
実行時間: 約3-4分

アウトプット:
  1. phase1_1100stocks_growth_combined.csv (1,101銘柄の統合評価)
  2. phase2_growth_top300.csv (成長分野TOP 300)
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
# 1. 既存評価データの読み込み
# ===========================

def load_existing_evaluations():
    """
    既存の801銘柄データを読み込み
    """
    print("📂 既存の評価データを読み込み中...")

    try:
        existing_df = pd.read_csv('phase1_800stocks_combined.csv')
        print(f"  ✅ 既存データ: {len(existing_df)}銘柄")

        if 'rank' in existing_df.columns:
            existing_df = existing_df.drop(columns=['rank'])

        return existing_df
    except FileNotFoundError:
        print("  ⚠️ エラー: phase1_800stocks_combined.csv が見つかりません")
        sys.exit(1)


# ===========================
# 2. 成長分野別銘柄リスト
# ===========================

def get_japan_growth_stocks():
    """
    日本株150銘柄 - 成長分野から選定
    """
    return [
        # 半導体・電子部品 (25銘柄)
        '6920.T',  # レーザーテック
        '6857.T',  # アドバンテスト
        '8035.T',  # 東京エレクトロン
        '6723.T',  # ルネサスエレクトロニクス
        '6963.T',  # ローム
        '6752.T',  # パナソニック ホールディングス
        '6762.T',  # TDK
        '6976.T',  # 太陽誘電
        '6988.T',  # 日東電工
        '4063.T',  # 信越化学工業
        '5202.T',  # 日本板硝子
        '6967.T',  # 新光電気工業
        '6754.T',  # アンリツ
        '6770.T',  # アルプスアルパイン
        '6728.T',  # アルバック
        '6965.T',  # 浜松ホトニクス
        '5711.T',  # 三菱マテリアル
        '5713.T',  # 住友金属鉱山
        '6845.T',  # アズビル
        '6849.T',  # 日本光電工業
        '6866.T',  # HIOKI
        '6727.T',  # ワコム
        '6923.T',  # スタンレー電気
        '6941.T',  # 山一電機
        '6803.T',  # ティアック

        # AI・DX・IT (20銘柄)
        '4704.T',  # トレンドマイクロ
        '3659.T',  # ネクソン
        '4324.T',  # 電通グループ
        '4755.T',  # 楽天グループ
        '9613.T',  # NTTデータ
        '4751.T',  # IT/インターネット企業
        '3923.T',  # ラクス
        '4385.T',  # メルカリ
        '4307.T',  # 野村総合研究所
        '9984.T',  # ソフトバンクグループ
        '9434.T',  # ソフトバンク
        '4784.T',  # GMOインターネット
        '3765.T',  # ガンホー・オンライン・エンターテイメント
        '9449.T',  # GMOインターネットグループ
        '2158.T',  # FRONTEO
        '3632.T',  # グリー
        '3667.T',  # enish
        '3664.T',  # モブキャスト
        '3656.T',  # KLab
        '3653.T',  # モルフォ

        # バイオ・医薬品 (20銘柄)
        '4568.T',  # 第一三共
        '4519.T',  # 中外製薬
        '4503.T',  # アステラス製薬
        '4502.T',  # 武田薬品工業
        '4523.T',  # エーザイ
        '4507.T',  # 塩野義製薬
        '4528.T',  # 小野薬品工業
        '4151.T',  # 協和キリン
        '4506.T',  # 住友ファーマ
        '4543.T',  # テルモ
        '4922.T',  # コーセー
        '4911.T',  # 資生堂
        '4927.T',  # ポーラ・オルビスホールディングス
        '4901.T',  # 富士フイルムホールディングス
        '7733.T',  # オリンパス
        '7731.T',  # ニコン
        '7732.T',  # トプコン
        '7741.T',  # HOYA
        '7752.T',  # リコー
        '4578.T',  # 大塚ホールディングス

        # EV・次世代モビリティ (20銘柄)
        '7203.T',  # トヨタ自動車
        '7267.T',  # ホンダ
        '7269.T',  # スズキ
        '7270.T',  # SUBARU
        '7202.T',  # いすゞ自動車
        '7211.T',  # 三菱自動車工業
        '7259.T',  # アイシン
        '7261.T',  # マツダ
        '7276.T',  # 小糸製作所
        '7282.T',  # 豊田合成
        '6902.T',  # デンソー
        '5108.T',  # ブリヂストン
        '5101.T',  # 横浜ゴム
        '5105.T',  # TOYO TIRE
        '6301.T',  # コマツ
        '6305.T',  # 日立建機
        '6326.T',  # クボタ
        '6361.T',  # 荏原製作所
        '6471.T',  # 日本精工
        '6472.T',  # NTN

        # 再生可能エネルギー (15銘柄)
        '5020.T',  # ENEOSホールディングス
        '9531.T',  # 東京ガス
        '9532.T',  # 大阪ガス
        '9502.T',  # 中部電力
        '9503.T',  # 関西電力
        '9504.T',  # 中国電力
        '9506.T',  # 東北電力
        '9508.T',  # 九州電力
        '9509.T',  # 北海道電力
        '1605.T',  # INPEX
        '1662.T',  # 石油資源開発
        '5401.T',  # 日本製鉄
        '5411.T',  # JFEホールディングス
        '5801.T',  # 古河電気工業
        '5802.T',  # 住友電気工業

        # ロボット・FA (15銘柄)
        '6954.T',  # ファナック
        '6273.T',  # SMC
        '6506.T',  # 安川電機
        '6586.T',  # マキタ
        '6302.T',  # 住友重機械工業
        '6103.T',  # オークマ
        '6113.T',  # アマダ
        '6473.T',  # ジェイテクト
        '6508.T',  # 明電舎
        '6641.T',  # 日新電機
        '6645.T',  # オムロン
        '7309.T',  # シマノ
        '6366.T',  # 千代田化工建設
        '7011.T',  # 三菱重工業
        '7012.T',  # 川崎重工業

        # 防衛・宇宙 (15銘柄)
        '7011.T',  # 三菱重工業
        '7012.T',  # 川崎重工業
        '7013.T',  # IHI
        '7003.T',  # 三井E&S
        '7004.T',  # 日立造船
        '6501.T',  # 日立製作所
        '6503.T',  # 三菱電機
        '6702.T',  # 富士通
        '6701.T',  # 日本電気(NEC)
        '6753.T',  # シャープ
        '6724.T',  # セイコーエプソン
        '6807.T',  # 日本航空電子工業
        '6804.T',  # ホシデン
        '6869.T',  # シスメックス
        '6367.T',  # ダイキン工業

        # インバウンド (10銘柄)
        '4661.T',  # オリエンタルランド
        '9735.T',  # セコム
        '3382.T',  # セブン&アイ・ホールディングス
        '8267.T',  # イオン
        '9020.T',  # JR東日本
        '9022.T',  # JR東海
        '9021.T',  # JR西日本
        '9202.T',  # ANAホールディングス
        '9064.T',  # ヤマトホールディングス
        '9101.T',  # 日本郵船
    ][:150]


def get_us_growth_stocks():
    """
    米国株150銘柄 - 成長分野から選定
    """
    return [
        # AI・生成AI (30銘柄)
        'NVDA',   # NVIDIA
        'MSFT',   # Microsoft
        'GOOGL',  # Alphabet
        'META',   # Meta
        'AMZN',   # Amazon
        'AAPL',   # Apple
        'TSLA',   # Tesla
        'AMD',    # AMD
        'INTC',   # Intel
        'AVGO',   # Broadcom
        'QCOM',   # Qualcomm
        'TXN',    # Texas Instruments
        'AMAT',   # Applied Materials
        'LRCX',   # Lam Research
        'KLAC',   # KLA
        'NXPI',   # NXP Semiconductors
        'MCHP',   # Microchip Technology
        'ADI',    # Analog Devices
        'SNPS',   # Synopsys
        'CDNS',   # Cadence Design
        'PLTR',   # Palantir
        'SNOW',   # Snowflake
        'AI',     # C3.ai
        'PATH',   # UiPath
        'MDB',    # MongoDB
        'DDOG',   # Datadog
        'NET',    # Cloudflare
        'CRWD',   # CrowdStrike
        'ZS',     # Zscaler
        'OKTA',   # Okta

        # クラウド・SaaS (25銘柄)
        'CRM',    # Salesforce
        'ORCL',   # Oracle
        'ADBE',   # Adobe
        'NOW',    # ServiceNow
        'WDAY',   # Workday
        'TEAM',   # Atlassian
        'SHOP',   # Shopify
        'SQ',     # Block (Square)
        'PYPL',   # PayPal
        'ZM',     # Zoom
        'DOCU',   # DocuSign
        'TWLO',   # Twilio
        'SPLK',   # Splunk
        'PANW',   # Palo Alto Networks
        'FTNT',   # Fortinet
        'VEEV',   # Veeva Systems
        'TTD',    # Trade Desk
        'PINS',   # Pinterest
        'SNAP',   # Snap
        'UBER',   # Uber
        'LYFT',   # Lyft
        'DASH',   # DoorDash
        'ABNB',   # Airbnb
        'RBLX',   # Roblox
        'U',      # Unity Software

        # バイオテック (25銘柄)
        'MRNA',   # Moderna
        'BNTX',   # BioNTech
        'REGN',   # Regeneron
        'VRTX',   # Vertex Pharmaceuticals
        'GILD',   # Gilead Sciences
        'AMGN',   # Amgen
        'BIIB',   # Biogen
        'ILMN',   # Illumina
        'CRSP',   # CRISPR Therapeutics
        'EDIT',   # Editas Medicine
        'NTLA',   # Intellia Therapeutics
        'BEAM',   # Beam Therapeutics
        'BLUE',   # bluebird bio
        'SRPT',   # Sarepta Therapeutics
        'BMRN',   # BioMarin
        'ALNY',   # Alnylam Pharmaceuticals
        'INCY',   # Incyte
        'EXEL',   # Exelixis
        'JAZZ',   # Jazz Pharmaceuticals
        'VTRS',   # Viatris
        'TECH',   # Bio-Techne
        'IONS',   # Ionis Pharmaceuticals
        'RARE',   # Ultragenyx
        'FOLD',   # Amicus Therapeutics
        'BBIO',   # BridgeBio Pharma

        # EV・自動運転 (20銘柄)
        'TSLA',   # Tesla
        'RIVN',   # Rivian
        'LCID',   # Lucid Motors
        'F',      # Ford
        'GM',     # General Motors
        'NIO',    # NIO
        'XPEV',   # XPeng
        'LI',     # Li Auto
        'CHPT',   # ChargePoint
        'BLNK',   # Blink Charging
        'EVG O',   # Evgo
        'QS',     # QuantumScape
        'STEM',   # Stem
        'ENPH',   # Enphase Energy
        'SEDG',   # SolarEdge
        'RUN',    # Sunrun
        'NOVA',   # Sunnova Energy
        'PLUG',   # Plug Power
        'FCEL',   # FuelCell Energy
        'BE',     # Bloom Energy

        # フィンテック・暗号資産 (15銘柄)
        'COIN',   # Coinbase
        'SQ',     # Block
        'PYPL',   # PayPal
        'V',      # Visa
        'MA',     # Mastercard
        'AXP',    # American Express
        'SOFI',   # SoFi Technologies
        'AFRM',   # Affirm
        'UPST',   # Upstart
        'LC',     # LendingClub
        'NU',     # Nu Holdings
        'HOOD',   # Robinhood
        'MARA',   # Marathon Digital
        'RIOT',   # Riot Platforms
        'MSTR',   # MicroStrategy

        # 宇宙開発 (15銘柄)
        'BA',     # Boeing
        'LMT',    # Lockheed Martin
        'NOC',    # Northrop Grumman
        'RTX',    # Raytheon Technologies
        'GD',     # General Dynamics
        'TXT',    # Textron
        'HII',    # Huntington Ingalls
        'AJRD',   # Aerojet Rocketdyne (買収済み)
        'SPCE',   # Virgin Galactic
        'RKLB',   # Rocket Lab
        'ASTS',   # AST SpaceMobile
        'SATS',   # EchoStar
        'GSAT',   # Globalstar
        'IRDM',   # Iridium Communications
        'VSAT',   # Viasat

        # 再生可能エネルギー (10銘柄)
        'NEE',    # NextEra Energy
        'ENPH',   # Enphase Energy
        'SEDG',   # SolarEdge
        'FSLR',   # First Solar
        'RUN',    # Sunrun
        'NOVA',   # Sunnova Energy
        'PLUG',   # Plug Power
        'FCEL',   # FuelCell Energy
        'BE',     # Bloom Energy
        'VWDRY',  # Vestas Wind Systems

        # 量子コンピューティング (5銘柄)
        'IBM',    # IBM
        'GOOGL',  # Alphabet
        'IONQ',   # IonQ
        'RGTI',   # Rigetti Computing
        'QUBT',   # Quantum Computing

        # その他新興分野 (5銘柄)
        'RBLX',   # Roblox (メタバース)
        'U',      # Unity (AR/VR)
        'MTTR',   # Matterport (3D)
        'VUZI',   # Vuzix (AR)
        'KOPN',   # Kopin (AR/VR)
    ][:150]


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
    print("Phase 1 (完全版): 1,101銘柄評価 - 成長分野特化")
    print("=" * 80)
    print()

    # ステップ1: 既存評価データの読み込み
    existing_data = load_existing_evaluations()
    print(f"✅ 既存評価データ: {len(existing_data)}銘柄")
    print()

    # ステップ2: 追加銘柄の定量評価
    additional_results = []

    # 日本株 追加150銘柄
    print("📊 日本株の追加評価（成長分野150銘柄）...")
    japan_growth = get_japan_growth_stocks()
    for i, ticker in enumerate(japan_growth, 1):
        print(f"  [{i}/{len(japan_growth)}] {ticker}", end='\r')
        metrics = get_stock_metrics(ticker, market='JP')
        score = calculate_quantitative_score(metrics)
        metrics['final_score'] = score
        metrics['evaluation_type'] = 'growth_quantitative'
        metrics['hayato'] = None
        metrics['researcher'] = None
        metrics['japanese'] = None
        metrics['sector'] = 'JP Growth'
        additional_results.append(metrics)
        time.sleep(0.5)

    print()
    print(f"✅ 日本株成長分野評価完了: {len(japan_growth)}銘柄")
    print()

    # 米国株 追加150銘柄
    print("📊 米国株の追加評価（成長分野150銘柄）...")
    us_growth = get_us_growth_stocks()
    for i, ticker in enumerate(us_growth, 1):
        print(f"  [{i}/{len(us_growth)}] {ticker}", end='\r')
        metrics = get_stock_metrics(ticker, market='US')
        score = calculate_quantitative_score(metrics)
        metrics['final_score'] = score
        metrics['evaluation_type'] = 'growth_quantitative'
        metrics['hayato'] = None
        metrics['researcher'] = None
        metrics['japanese'] = None
        metrics['sector'] = 'US Growth'
        additional_results.append(metrics)
        time.sleep(0.5)

    print()
    print(f"✅ 米国株成長分野評価完了: {len(us_growth)}銘柄")
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
    output_file = 'phase1_1100stocks_growth_combined.csv'
    all_data.to_csv(output_file, index=False, encoding='utf-8-sig')

    print("=" * 80)
    print("✅ Phase 1完了 - 1,101銘柄評価（成長分野特化）")
    print("=" * 80)
    print(f"📄 出力ファイル: {output_file}")
    print(f"📊 評価銘柄数: {len(all_data)}銘柄")
    print(f"  - 日本株: {len(all_data[all_data['market']=='JP'])}銘柄")
    print(f"  - 米国株: {len(all_data[all_data['market']=='US'])}銘柄")
    print(f"  - 3エージェント評価: {len(all_data[all_data['evaluation_type']=='3agent'])}銘柄")
    print(f"  - 定量評価: {len(all_data[all_data['evaluation_type']=='quantitative'])}銘柄")
    print(f"  - 成長分野定量評価: {len(all_data[all_data['evaluation_type']=='growth_quantitative'])}銘柄")
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

    # TOP 30表示
    print("🏆 総合スコア TOP 30:")
    print("-" * 80)
    for _, row in all_data.head(30).iterrows():
        eval_type = "3agent" if row['evaluation_type'] == '3agent' else "quant"
        if row['evaluation_type'] == 'growth_quantitative':
            eval_type = "growth"
        print(f"{row['rank']:3d}. [{row['market']}] {row['ticker']:10s} {str(row['name'])[:30]:30s} {row['final_score']:5.1f}点 [{eval_type}]")
    print()

    # 成長分野TOP 300抽出
    growth_top300 = all_data.head(300)
    growth_file = 'phase2_growth_top300.csv'
    growth_top300.to_csv(growth_file, index=False, encoding='utf-8-sig')
    print(f"🎯 成長分野TOP 300: {growth_file}")
    print()

    # TOP 300の内訳
    top300_jp = len(growth_top300[growth_top300['market'] == 'JP'])
    top300_us = len(growth_top300[growth_top300['market'] == 'US'])

    print("📊 TOP 300の内訳:")
    print(f"  - 日本株: {top300_jp}銘柄")
    print(f"  - 米国株: {top300_us}銘柄")
    print()

    print("✨ 完了!")
    print("  1,101銘柄の評価が完了しました。")
    print("  成長分野に特化したTOP 300銘柄がphase2_growth_top300.csvに保存されました。")
    print()


if __name__ == '__main__':
    main()
