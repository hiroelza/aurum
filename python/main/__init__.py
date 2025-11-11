"""
非推奨: このディレクトリは後方互換性のために残されています。
新しいコードでは python.controllers を使用してください。
"""
import warnings

warnings.warn(
    "python.main is deprecated. Use python.controllers instead.",
    DeprecationWarning,
    stacklevel=2
)
