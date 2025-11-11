# -*- coding: utf-8 -*-
"""
統計定数モジュール

リスク評価、緊急資金、その他の統計的な定数を定義します。

最終更新: 2025年11月9日（Phase 1: config分割）
"""

# ===== リスク評価 =====

HIGH_RISK_THRESHOLD = 30  # 高リスクとみなす割合（%）
MODERATE_RISK_THRESHOLD = 15  # 中リスクとみなす割合（%）

# ===== 緊急資金 =====

EMERGENCY_FUND_MONTHS = 6  # 推奨する緊急資金（月数）
MINIMUM_CASH_RESERVE_MONTHS = 3  # 最低限の現金準備（月数）

# ===== インフレーション =====

DEFAULT_INFLATION_RATE = 2.0  # デフォルトのインフレ率（年率、%）
HIGH_INFLATION_RATE = 3.0  # 高インフレシナリオ（年率、%）

# ===== 手数料 =====

TYPICAL_FUND_FEE = 0.2  # 一般的なインデックスファンドの信託報酬（%）
HIGH_FEE_THRESHOLD = 1.0  # 高手数料とみなす閾値（%）

# ===== 税金 =====

CAPITAL_GAINS_TAX_RATE = 20.315  # 譲渡益課税率（%）（所得税15% + 住民税5% + 復興特別所得税0.315%）

# ===== NISA制度 =====

NISA_ANNUAL_LIMIT = 360  # 万円（年間投資上限）
NISA_LIFETIME_LIMIT = 1800  # 万円（生涯投資上限）
NISA_GROWTH_LIMIT = 1200  # 万円（成長投資枠上限）

# ===== iDeCo制度 =====

IDECO_MONTHLY_LIMIT_EMPLOYEE = 2.3  # 万円（企業年金ありの会社員）
IDECO_MONTHLY_LIMIT_NO_PENSION = 6.8  # 万円（企業年金なしの会社員）
IDECO_WITHDRAWAL_AGE = 60  # 受給開始年齢

# ===== デバッグ用情報表示 =====

if __name__ == '__main__':
    print("="*60)
    print("統計定数 (python.config.constants)")
    print("="*60)
    print("\n【リスク評価】")
    print(f"  高リスク閾値: {HIGH_RISK_THRESHOLD}%")
    print(f"  中リスク閾値: {MODERATE_RISK_THRESHOLD}%")

    print("\n【緊急資金】")
    print(f"  推奨緊急資金: {EMERGENCY_FUND_MONTHS}ヶ月分")
    print(f"  最低現金準備: {MINIMUM_CASH_RESERVE_MONTHS}ヶ月分")

    print("\n【インフレーション】")
    print(f"  デフォルトインフレ率: {DEFAULT_INFLATION_RATE}%")
    print(f"  高インフレシナリオ: {HIGH_INFLATION_RATE}%")

    print("\n【手数料】")
    print(f"  一般的なファンド信託報酬: {TYPICAL_FUND_FEE}%")
    print(f"  高手数料閾値: {HIGH_FEE_THRESHOLD}%")

    print("\n【税金】")
    print(f"  譲渡益課税率: {CAPITAL_GAINS_TAX_RATE}%")

    print("\n【NISA制度】")
    print(f"  年間投資上限: {NISA_ANNUAL_LIMIT}万円")
    print(f"  生涯投資上限: {NISA_LIFETIME_LIMIT}万円")
    print(f"  成長投資枠上限: {NISA_GROWTH_LIMIT}万円")

    print("\n【iDeCo制度】")
    print(f"  月額上限（企業年金あり）: {IDECO_MONTHLY_LIMIT_EMPLOYEE}万円")
    print(f"  月額上限（企業年金なし）: {IDECO_MONTHLY_LIMIT_NO_PENSION}万円")
    print(f"  受給開始年齢: {IDECO_WITHDRAWAL_AGE}歳")
    print("="*60)
