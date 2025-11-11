# -*- coding: utf-8 -*-
"""
⚠️ 非推奨: このファイルは後方互換性のために残されています。

新しいセットアップでは python/config/personal.template.py を使用してください。

セットアップ手順:
1. python/config/personal.template.py を python/config/personal.py にコピー
2. [...]部分を実際の値に置き換え

最終更新: 2025年11月9日（Phase 1: config分割、後方互換性レイヤー）
"""
import warnings
warnings.warn(
    "python/personal_config.template.py is deprecated. Use python/config/personal.template.py instead.",
    DeprecationWarning,
    stacklevel=2
)

# 後方互換性のため、新しいテンプレートの内容をインポート
from python.config.personal import *

# ===== 基本情報 =====

# 年齢（現在）
CURRENT_AGE = [YOUR_AGE]  # 例: 35
CURRENT_YEAR = 2025
RETIREMENT_AGE = [RETIREMENT_AGE]  # 例: 60, 65
RETIREMENT_YEAR = CURRENT_YEAR + (RETIREMENT_AGE - CURRENT_AGE)

# 家族構成
WIFE_AGE = [SPOUSE_AGE]  # 配偶者の年齢、例: 33（いない場合は None）
ELDEST_CHILD_AGE = [CHILD1_AGE]  # 第1子の年齢、例: 5（いない場合は None）
YOUNGEST_CHILD_AGE = [CHILD2_AGE]  # 第2子の年齢、例: 3（いない場合は None）

# ===== 資産状況（万円） =====

# 投資資産
CURRENT_NISA = [NISA_ASSETS]  # NISA資産、例: 500
CURRENT_NISA_PRINCIPAL = [NISA_PRINCIPAL]  # NISA元本、例: 450
CURRENT_NISA_GAIN = CURRENT_NISA - CURRENT_NISA_PRINCIPAL  # NISA含み益（自動計算）

CURRENT_IDECO = [IDECO_ASSETS]  # iDeCo資産、例: 100
CURRENT_IDECO_PRINCIPAL = [IDECO_PRINCIPAL]  # iDeCo元本、例: 90
CURRENT_IDECO_GAIN = CURRENT_IDECO - CURRENT_IDECO_PRINCIPAL  # iDeCo含み益（自動計算）

CURRENT_COMPANY_STOCK = [COMPANY_STOCK_ASSETS]  # 自社株、例: 0（ない場合は 0）
CURRENT_COMPANY_STOCK_COST = [COMPANY_STOCK_COST]  # 自社株簿価、例: 0（ない場合は 0）
CURRENT_COMPANY_STOCK_GAIN = CURRENT_COMPANY_STOCK - CURRENT_COMPANY_STOCK_COST  # 自社株含み益（自動計算）

# 現金・預金
CURRENT_CASH = [CASH_ASSETS]  # 現金・普通預金、例: 200

# 総資産（自動計算）
TOTAL_ASSETS = CURRENT_NISA + CURRENT_IDECO + CURRENT_COMPANY_STOCK + CURRENT_CASH

# ===== 収入（万円/年） =====

ANNUAL_INCOME_AFTER_TAX = [ANNUAL_INCOME_NET]  # 手取り年収、例: 450
MONTHLY_INCOME = ANNUAL_INCOME_AFTER_TAX / 12  # 月収（手取り、自動計算）

# ===== 支出（万円/年） =====

ANNUAL_RENT = [ANNUAL_RENT]  # 年間家賃、例: 120（月10万円の場合）
MONTHLY_RENT = ANNUAL_RENT / 12  # 月間家賃（自動計算）

# ===== 月次投資額（万円/月） =====

# 現在（2025年）
CURRENT_MONTHLY_NISA = [MONTHLY_NISA]  # 新NISA積立、例: 5.0
CURRENT_MONTHLY_IDECO = [MONTHLY_IDECO]  # iDeCo積立、例: 2.0
CURRENT_TOTAL_MONTHLY_INVESTMENT = CURRENT_MONTHLY_NISA + CURRENT_MONTHLY_IDECO

# 将来の計画（オプション）
MONTHLY_IDECO_2027 = [MONTHLY_IDECO_FUTURE]  # iDeCo増額後、例: 2.5
MONTHLY_INVESTMENT_2027 = CURRENT_MONTHLY_NISA + MONTHLY_IDECO_2027

# 配偶者の投資（該当する場合）
WIFE_MONTHLY_NISA = [SPOUSE_MONTHLY_NISA]  # 妻のNISA積立、例: 0（いない場合は 0）

# NISA生涯投資枠
NISA_LIFETIME_LIMIT = 1800  # 万円（制度上限）
NISA_LIFETIME_REMAINING = [NISA_REMAINING]  # 万円（残り枠）、例: 1300

# ===== ライフプラン目標 =====

# 教育費
EDUCATION_COST = [EDUCATION_TOTAL]  # 万円（全子供分）、例: 0（子供がいない場合は 0）
EDUCATION_COST_PER_CHILD = EDUCATION_COST / 2 if EDUCATION_COST > 0 else 0  # 1人あたり（自動計算）

# 老後資金目標
RETIREMENT_GOAL = [RETIREMENT_TARGET]  # 万円（退職時点の目標資産）、例: 3000

# ===== 統計データ：年金受給額 =====

MONTHLY_PENSION = [MONTHLY_PENSION_ESTIMATE]  # 万円（年金受給額の見込み）、例: 15.0
ANNUAL_PENSION = MONTHLY_PENSION * 12

# 統計データ：老後の月間不足額
MONTHLY_RETIREMENT_SHORTFALL = [MONTHLY_SHORTFALL]  # 万円、例: 5.0

# ===== デバッグ用情報表示 =====

if __name__ == '__main__':
    print("="*60)
    print("個人情報設定ファイル (personal_config.py)")
    print("="*60)
    print("\n【基本情報】")
    print(f"  年齢: {CURRENT_AGE}歳")
    print(f"  配偶者の年齢: {WIFE_AGE}歳")
    print(f"  第1子: {ELDEST_CHILD_AGE}歳")
    print(f"  第2子: {YOUNGEST_CHILD_AGE}歳")
    print(f"  退職年: {RETIREMENT_YEAR}年（{RETIREMENT_AGE}歳）")

    print("\n【資産状況】")
    print(f"  NISA: {CURRENT_NISA:.1f}万円（元本{CURRENT_NISA_PRINCIPAL}万円、含み益+{CURRENT_NISA_GAIN:.1f}万円）")
    print(f"  iDeCo: {CURRENT_IDECO:.1f}万円（元本{CURRENT_IDECO_PRINCIPAL}万円、含み益+{CURRENT_IDECO_GAIN:.1f}万円）")
    print(f"  自社株: {CURRENT_COMPANY_STOCK}万円（簿価{CURRENT_COMPANY_STOCK_COST}万円、含み益+{CURRENT_COMPANY_STOCK_GAIN}万円）")
    print(f"  現金: {CURRENT_CASH}万円")
    print(f"  総資産: {TOTAL_ASSETS:.1f}万円")

    print("\n【収入】")
    print(f"  手取り年収: {ANNUAL_INCOME_AFTER_TAX}万円")
    print(f"  月収（手取り）: {MONTHLY_INCOME:.1f}万円")

    print("\n【支出】")
    print(f"  年間家賃: {ANNUAL_RENT}万円")
    print(f"  月間家賃: {MONTHLY_RENT:.1f}万円")

    print("\n【月次投資額】")
    print(f"  NISA: {CURRENT_MONTHLY_NISA}万円/月")
    print(f"  iDeCo（現在）: {CURRENT_MONTHLY_IDECO}万円/月")
    print(f"  iDeCo（将来）: {MONTHLY_IDECO_2027}万円/月")
    print(f"  配偶者NISA: {WIFE_MONTHLY_NISA}万円/月")

    print("\n【ライフプラン目標】")
    print(f"  教育費目標: {EDUCATION_COST}万円")
    print(f"  老後資金目標: {RETIREMENT_GOAL}万円（{RETIREMENT_AGE}歳時点）")

    print("\n⚠️  [...]を実際の値に置き換えてください。")
    print("="*60)
