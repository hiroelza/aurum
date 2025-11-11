# -*- coding: utf-8 -*-
"""
⚠️ 非推奨: このファイルは後方互換性のために残されています。

新しいコードでは python.config を使用してください。

旧: from config import INPUT_CSV_DIR
新: from python.config import INPUT_CSV_DIR

または:
    from python.config.paths import INPUT_CSV_DIR
    from python.config.personal import CURRENT_AGE
    from python.config.simulation import MONTE_CARLO_ITERATIONS
    from python.config.constants import HIGH_RISK_THRESHOLD

最終更新: 2025年11月9日（Phase 1: config分割、後方互換性レイヤー）
"""
import warnings
warnings.warn(
    "python/config.py is deprecated. Use 'from python.config import *' instead.",
    DeprecationWarning,
    stacklevel=2
)

from python.config import *
