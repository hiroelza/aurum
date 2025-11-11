"""
テスト: python/config/paths.py

パス設定が正しく構成されているかをテストします。
"""

import os
import sys

# python/ ディレクトリをパスに追加
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'python'))

from config import paths


def test_base_dir_exists():
    """BASE_DIRが存在することを確認"""
    assert os.path.exists(paths.BASE_DIR), f"BASE_DIR does not exist: {paths.BASE_DIR}"


def test_base_dir_is_aurum():
    """BASE_DIRがaurumディレクトリを指していることを確認"""
    assert paths.BASE_DIR.endswith('aurum'), f"BASE_DIR should end with 'aurum': {paths.BASE_DIR}"


def test_data_dir_path():
    """DATA_DIRのパスが正しいことを確認（sources/へのエイリアス）"""
    expected = os.path.join(paths.BASE_DIR, 'sources')
    assert paths.DATA_DIR == expected, f"DATA_DIR mismatch: {paths.DATA_DIR} != {expected}"


def test_input_csv_dir_path():
    """INPUT_CSV_DIRのパスが正しいことを確認（sources/reference/csv/）"""
    expected = os.path.join(paths.BASE_DIR, 'sources', 'reference', 'csv')
    assert paths.INPUT_CSV_DIR == expected, f"INPUT_CSV_DIR mismatch: {paths.INPUT_CSV_DIR} != {expected}"


def test_output_generated_dir_path():
    """OUTPUT_GENERATED_DIRのパスが正しいことを確認（outputs/python/）"""
    expected = os.path.join(paths.BASE_DIR, 'outputs', 'python')
    assert paths.OUTPUT_GENERATED_DIR == expected, f"OUTPUT_GENERATED_DIR mismatch"


def test_reports_dir_path():
    """REPORTS_DIRのパスが正しいことを確認（outputs/reports/）"""
    expected = os.path.join(paths.BASE_DIR, 'outputs', 'reports')
    assert paths.REPORTS_DIR == expected, f"REPORTS_DIR mismatch: {paths.REPORTS_DIR} != {expected}"


def test_working_dir_path():
    """WORKING_DIRのパスが正しいことを確認（outputs/reports/working/）"""
    expected = os.path.join(paths.BASE_DIR, 'outputs', 'reports', 'working')
    assert paths.WORKING_DIR == expected, f"WORKING_DIR mismatch: {paths.WORKING_DIR} != {expected}"


def test_backward_compatibility_csv_dir():
    """後方互換性: CSV_DIR == INPUT_CSV_DIRを確認"""
    assert paths.CSV_DIR == paths.INPUT_CSV_DIR, "CSV_DIR should equal INPUT_CSV_DIR"


def test_backward_compatibility_result_dir():
    """後方互換性: RESULT_DIR == REPORTS_COMPLETED_DIRを確認"""
    expected = os.path.join(paths.BASE_DIR, 'outputs', 'reports', 'completed')
    assert paths.RESULT_DIR == expected, f"RESULT_DIR mismatch"


def test_backward_compatibility_image_dir():
    """後方互換性: IMAGE_DIR == OUTPUT_GENERATED_DIRを確認"""
    assert paths.IMAGE_DIR == paths.OUTPUT_GENERATED_DIR, "IMAGE_DIR should equal OUTPUT_GENERATED_DIR"


def test_all_critical_dirs_exist():
    """重要なディレクトリが存在することを確認"""
    critical_dirs = [
        paths.BASE_DIR,
        paths.DATA_DIR,  # sources/
        # INPUT_CSV_DIR, REPORTS_DIRはpaths.pyで自動作成されるためスキップ
    ]

    for dir_path in critical_dirs:
        assert os.path.exists(dir_path), f"Critical directory does not exist: {dir_path}"
