"""
非推奨: このファイルは後方互換性のために残されています。
新しいコードでは python.controllers.investment_analysis を使用してください。
"""
import warnings
import sys
import os

warnings.warn(
    "python.main.investment_analysis is deprecated. Use python.controllers.investment_analysis instead.",
    DeprecationWarning,
    stacklevel=2
)

# 新しいファイルのパスを取得
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
new_file_path = os.path.join(os.path.dirname(__file__), '..', 'controllers', 'investment_analysis.py')

# このファイルが直接実行された場合のみ、新しいファイルの内容を実行
if __name__ == "__main__":
    with open(new_file_path, 'r', encoding='utf-8') as f:
        code = f.read()
    exec(code)
