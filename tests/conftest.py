"""
pytest設定ファイル

テスト用フィクスチャとモックを提供します。
"""

import os
import sys
import pytest

# python/ ディレクトリをパスに追加
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'python'))


@pytest.fixture
def mock_personal_config(monkeypatch):
    """
    personal.pyのモック設定

    personal.pyが存在しない環境でもテストが実行できるよう、
    テスト用のダミーデータを提供します。
    """
    # python.config.personalモジュールをモック
    from python.config import personal_template as personal_mock

    # テスト用のダミー値を設定
    monkeypatch.setattr('python.config.CURRENT_AGE', 35)
    monkeypatch.setattr('python.config.CURRENT_YEAR', 2025)
    monkeypatch.setattr('python.config.RETIREMENT_AGE', 65)
    monkeypatch.setattr('python.config.RETIREMENT_YEAR', 2055)

    return personal_mock
