# -*- coding: utf-8 -*-
"""
パス設定モジュール

このモジュールはaurumプロジェクトで使用するすべてのパスを一元管理します。

実行方法:
    すべてのスクリプトは aurum/ ディレクトリから実行してください

    例:
        cd aurum
        python python/main/investment_analysis.py

使用方法:
    from python.config.paths import INPUT_CSV_DIR, REPORTS_DIR, WORKING_DIR

最終更新: 2025年11月9日（Phase 1: config分割）
"""

import os

# ベースディレクトリの設定
# このファイルは python/config/paths.py なので、2つ上がaurum/
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# === 新ディレクトリ構造（Phase 12: 2025年11月9日） ===

# sources/ - ソースデータ（手動管理）
SOURCES_DIR = os.path.join(BASE_DIR, 'sources')
SOURCES_PROFILE_DIR = os.path.join(SOURCES_DIR, 'profile')
SOURCES_PROFILE_TEMPLATES_DIR = os.path.join(SOURCES_PROFILE_DIR, 'templates')
SOURCES_PROFILE_HISTORICAL_DIR = os.path.join(SOURCES_PROFILE_DIR, 'historical')
SOURCES_REFERENCE_DIR = os.path.join(SOURCES_DIR, 'reference')
SOURCES_REFERENCE_CSV_DIR = os.path.join(SOURCES_REFERENCE_DIR, 'csv')
SOURCES_REFERENCE_PDF_DIR = os.path.join(SOURCES_REFERENCE_DIR, 'pdf')
SOURCES_REFERENCE_IMAGE_DIR = os.path.join(SOURCES_REFERENCE_DIR, 'image')
SOURCES_REFERENCE_MARKET_DIR = os.path.join(SOURCES_REFERENCE_DIR, 'market')

# outputs/ - 生成データ（自動生成）
OUTPUTS_DIR = os.path.join(BASE_DIR, 'outputs')
OUTPUTS_PYTHON_DIR = os.path.join(OUTPUTS_DIR, 'python')
OUTPUTS_PYTHON_SCREENING_DIR = os.path.join(OUTPUTS_PYTHON_DIR, 'screening')
OUTPUTS_PYTHON_CACHE_DIR = os.path.join(OUTPUTS_PYTHON_DIR, 'cache')
OUTPUTS_PYTHON_TEMP_DIR = os.path.join(OUTPUTS_PYTHON_DIR, 'temp')
OUTPUTS_REPORTS_DIR = os.path.join(OUTPUTS_DIR, 'reports')
OUTPUTS_REPORTS_COMPLETED_DIR = os.path.join(OUTPUTS_REPORTS_DIR, 'completed')
OUTPUTS_REPORTS_WORKING_DIR = os.path.join(OUTPUTS_REPORTS_DIR, 'working')

# document/ - プロジェクト管理
DOCUMENT_DIR = os.path.join(BASE_DIR, 'document')

# === 後方互換性レイヤー（Phase 1以前のパス） ===
# 警告: これらのパスは非推奨です。新しいコードでは上記の新パスを使用してください。

# 旧 data/ 構造
DATA_DIR = SOURCES_DIR  # 非推奨: sources/を使用
DATA_INPUT_DIR = SOURCES_PROFILE_DIR  # 非推奨: sources/profile/を使用
DATA_OUTPUT_DIR = OUTPUTS_PYTHON_DIR  # 非推奨: outputs/python/を使用
DATA_ARCHIVE_DIR = os.path.join(SOURCES_DIR, 'archive')  # 非推奨

# 旧 input 構造
INPUT_CSV_DIR = SOURCES_REFERENCE_CSV_DIR  # 非推奨: sources/reference/csv/を使用

# 旧 output 構造
OUTPUT_CACHE_DIR = OUTPUTS_PYTHON_CACHE_DIR  # 非推奨: outputs/python/cache/を使用
OUTPUT_TEMP_DIR = OUTPUTS_PYTHON_TEMP_DIR  # 非推奨: outputs/python/temp/を使用
OUTPUT_GENERATED_DIR = OUTPUTS_PYTHON_DIR  # 非推奨: outputs/python/を使用

# 旧 reports 構造
REPORTS_DIR = OUTPUTS_REPORTS_DIR  # 非推奨: outputs/reports/を使用
REPORTS_COMPLETED_DIR = OUTPUTS_REPORTS_COMPLETED_DIR  # 非推奨
REPORTS_WORKING_DIR = OUTPUTS_REPORTS_WORKING_DIR  # 非推奨

# 旧ドキュメントディレクトリ（Phase 12以前はDOCUMENT_DIRが存在していたが、Phase 12でdocument/に統一）

# 後方互換性レイヤー（非推奨）
IMAGE_DIR = OUTPUT_GENERATED_DIR  # 廃止予定
OUTPUT_CSV_DIR = OUTPUT_GENERATED_DIR  # 廃止予定
CSV_DIR = INPUT_CSV_DIR  # 非推奨
RESULT_DIR = REPORTS_COMPLETED_DIR  # 非推奨
RESEARCH_DIR = REPORTS_WORKING_DIR  # 非推奨
WORKING_DIR = REPORTS_WORKING_DIR  # 非推奨

# ディレクトリが存在しない場合は作成
_REQUIRED_DIRS = [
    # sources/
    SOURCES_PROFILE_DIR,
    SOURCES_PROFILE_TEMPLATES_DIR,
    SOURCES_PROFILE_HISTORICAL_DIR,
    SOURCES_REFERENCE_CSV_DIR,
    SOURCES_REFERENCE_PDF_DIR,
    SOURCES_REFERENCE_IMAGE_DIR,
    SOURCES_REFERENCE_MARKET_DIR,
    # outputs/
    OUTPUTS_PYTHON_SCREENING_DIR,
    OUTPUTS_PYTHON_CACHE_DIR,
    OUTPUTS_PYTHON_TEMP_DIR,
    OUTPUTS_REPORTS_COMPLETED_DIR,
    OUTPUTS_REPORTS_WORKING_DIR,
    # document/
    DOCUMENT_DIR
]

for directory in _REQUIRED_DIRS:
    os.makedirs(directory, exist_ok=True)

# パス情報の表示（デバッグ用）
if __name__ == '__main__':
    print("=== Aurum Project - Path Configuration ===")
    print(f"BASE_DIR: {BASE_DIR}")
    print(f"\n【データディレクトリ】")
    print(f"DATA_DIR: {DATA_DIR}")
    print(f"DATA_INPUT_DIR: {DATA_INPUT_DIR}")
    print(f"INPUT_CSV_DIR: {INPUT_CSV_DIR}")
    print(f"DATA_OUTPUT_DIR: {DATA_OUTPUT_DIR}")
    print(f"OUTPUT_CACHE_DIR: {OUTPUT_CACHE_DIR}")
    print(f"OUTPUT_TEMP_DIR: {OUTPUT_TEMP_DIR}")
    print(f"OUTPUT_GENERATED_DIR: {OUTPUT_GENERATED_DIR}")
    print(f"DATA_ARCHIVE_DIR: {DATA_ARCHIVE_DIR}")
    print(f"\n【レポートディレクトリ】")
    print(f"REPORTS_DIR: {REPORTS_DIR}")
    print(f"REPORTS_COMPLETED_DIR: {REPORTS_COMPLETED_DIR}")
    print(f"REPORTS_WORKING_DIR: {REPORTS_WORKING_DIR}")
    print(f"\n【後方互換性レイヤー（非推奨）】")
    print(f"IMAGE_DIR: {IMAGE_DIR}")
    print(f"OUTPUT_CSV_DIR: {OUTPUT_CSV_DIR}")
    print(f"CSV_DIR: {CSV_DIR}")
    print(f"\n=== Directory Status ===")
    for name, path in [
        ('BASE_DIR', BASE_DIR),
        ('DATA_INPUT_DIR', DATA_INPUT_DIR),
        ('INPUT_CSV_DIR', INPUT_CSV_DIR),
        ('OUTPUT_GENERATED_DIR', OUTPUT_GENERATED_DIR),
        ('DATA_ARCHIVE_DIR', DATA_ARCHIVE_DIR),
        ('REPORTS_COMPLETED_DIR', REPORTS_COMPLETED_DIR),
        ('REPORTS_WORKING_DIR', REPORTS_WORKING_DIR)
    ]:
        status = "[OK] Exists" if os.path.exists(path) else "[ERROR] Not Found"
        print(f"{name}: {status}")
