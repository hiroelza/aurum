# -*- coding: utf-8 -*-
"""
シミュレーション設定モジュール

投資シミュレーション、モンテカルロシミュレーションで使用する
パラメータを定義します。

最終更新: 2025年11月9日（Phase 1: config分割）
"""

# ===== モンテカルロシミュレーション =====

MONTE_CARLO_ITERATIONS = 10000  # シミュレーション回数

# ===== 期待リターン（年率、%） =====

EXPECTED_RETURN_STOCK = 7.0  # 株式の期待リターン
EXPECTED_RETURN_BOND = 3.0  # 債券の期待リターン
EXPECTED_RETURN_BALANCED = 5.0  # バランス型の期待リターン

# ===== ボラティリティ（年率、%） =====

VOLATILITY_STOCK = 18.0  # 株式のボラティリティ（標準偏差）
VOLATILITY_BOND = 5.0  # 債券のボラティリティ（標準偏差）
VOLATILITY_BALANCED = 10.0  # バランス型のボラティリティ（標準偏差）

# ===== アセットアロケーション =====

# デフォルトのアセットアロケーション（%）
DEFAULT_STOCK_RATIO = 80  # 株式比率
DEFAULT_BOND_RATIO = 20  # 債券比率

# ===== シミュレーション期間 =====

DEFAULT_SIMULATION_YEARS = 20  # デフォルトシミュレーション期間（年）

# ===== デバッグ用情報表示 =====

if __name__ == '__main__':
    print("="*60)
    print("シミュレーション設定 (python.config.simulation)")
    print("="*60)
    print("\n【モンテカルロシミュレーション】")
    print(f"  シミュレーション回数: {MONTE_CARLO_ITERATIONS:,}回")

    print("\n【期待リターン（年率）】")
    print(f"  株式: {EXPECTED_RETURN_STOCK}%")
    print(f"  債券: {EXPECTED_RETURN_BOND}%")
    print(f"  バランス: {EXPECTED_RETURN_BALANCED}%")

    print("\n【ボラティリティ（年率）】")
    print(f"  株式: {VOLATILITY_STOCK}%")
    print(f"  債券: {VOLATILITY_BOND}%")
    print(f"  バランス: {VOLATILITY_BALANCED}%")

    print("\n【デフォルトアセットアロケーション】")
    print(f"  株式: {DEFAULT_STOCK_RATIO}%")
    print(f"  債券: {DEFAULT_BOND_RATIO}%")

    print("\n【シミュレーション期間】")
    print(f"  デフォルト期間: {DEFAULT_SIMULATION_YEARS}年")
    print("="*60)
