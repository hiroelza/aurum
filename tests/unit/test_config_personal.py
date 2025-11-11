"""
テスト: python/config/personal.py

個人設定が正しく構成されているかをテストします。

注意: personal.pyが存在しない場合、これらのテストはスキップされます。
"""

import os
import sys
import pytest

# python/ ディレクトリをパスに追加
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'python'))

# personal.pyの存在確認
PERSONAL_PY_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'python', 'config', 'personal.py')
PERSONAL_PY_EXISTS = os.path.exists(PERSONAL_PY_PATH)

# personal.pyが存在しない場合はモジュール全体をスキップ
if not PERSONAL_PY_EXISTS:
    pytest.skip("personal.py not found. Please copy from personal.template.py", allow_module_level=True)

from config import personal


def test_current_age_is_positive():
    """CURRENT_AGEが正の整数であることを確認"""
    assert personal.CURRENT_AGE > 0, "CURRENT_AGE should be positive"
    assert isinstance(personal.CURRENT_AGE, int), "CURRENT_AGE should be an integer"


def test_retirement_age_is_greater_than_current():
    """RETIREMENT_AGEがCURRENT_AGEより大きいことを確認"""
    assert personal.RETIREMENT_AGE > personal.CURRENT_AGE, \
        f"RETIREMENT_AGE ({personal.RETIREMENT_AGE}) should be greater than CURRENT_AGE ({personal.CURRENT_AGE})"


def test_total_assets_equals_sum():
    """TOTAL_ASSETSが各資産の合計と一致することを確認"""
    calculated_total = (
        personal.CURRENT_NISA +
        personal.CURRENT_IDECO +
        personal.CURRENT_COMPANY_STOCK +
        personal.CURRENT_CASH
    )
    assert abs(personal.TOTAL_ASSETS - calculated_total) < 0.01, \
        f"TOTAL_ASSETS ({personal.TOTAL_ASSETS}) should equal sum of assets ({calculated_total})"


def test_all_assets_are_non_negative():
    """すべての資産額が非負であることを確認"""
    assets = [
        ('CURRENT_NISA', personal.CURRENT_NISA),
        ('CURRENT_IDECO', personal.CURRENT_IDECO),
        ('CURRENT_COMPANY_STOCK', personal.CURRENT_COMPANY_STOCK),
        ('CURRENT_CASH', personal.CURRENT_CASH),
    ]

    for name, value in assets:
        assert value >= 0, f"{name} should be non-negative: {value}"


def test_annual_income_is_positive():
    """年収が正の値であることを確認"""
    assert personal.ANNUAL_INCOME_AFTER_TAX > 0, "ANNUAL_INCOME_AFTER_TAX should be positive"


def test_monthly_income_calculation():
    """月収が年収の1/12であることを確認"""
    expected_monthly = personal.ANNUAL_INCOME_AFTER_TAX / 12
    assert abs(personal.MONTHLY_INCOME - expected_monthly) < 0.01, \
        f"MONTHLY_INCOME should be ANNUAL_INCOME_AFTER_TAX / 12"


def test_nisa_lifetime_limit_is_positive():
    """NISA生涯投資枠が正の値であることを確認"""
    assert personal.NISA_LIFETIME_LIMIT > 0, "NISA_LIFETIME_LIMIT should be positive"


def test_current_monthly_ideco_is_positive():
    """iDeCo月額投資額が正の値であることを確認"""
    assert personal.CURRENT_MONTHLY_IDECO > 0, "CURRENT_MONTHLY_IDECO should be positive"


def test_education_cost_per_child_is_positive():
    """子供一人あたりの教育費が正の値であることを確認"""
    assert personal.EDUCATION_COST_PER_CHILD > 0, "EDUCATION_COST_PER_CHILD should be positive"


def test_retirement_year_calculation():
    """RETIREMENT_YEARの計算が正しいことを確認"""
    expected_retirement_year = personal.CURRENT_YEAR + (personal.RETIREMENT_AGE - personal.CURRENT_AGE)
    assert personal.RETIREMENT_YEAR == expected_retirement_year, \
        f"RETIREMENT_YEAR calculation mismatch: {personal.RETIREMENT_YEAR} != {expected_retirement_year}"
