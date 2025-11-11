"""
3エージェント構造化議論システム

このスクリプトは、3つのエージェント（哲学・統計・税制）による
構造化議論プロトコルのデモンストレーションを実行します。

使い方:
    python python/controllers/debate_analysis.py

説明:
    - 3ラウンド制の議論を実行
    - ラウンド1: 各エージェントが独立評価
    - ラウンド2: 他エージェントの評価を読んで反論
    - ラウンド3: 反論を踏まえて最終評価
"""

import sys
from pathlib import Path

# プロジェクトルートをパスに追加
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from python.models.debate.structured_debate_protocol import (
    StructuredDebateProtocol,
    Agent,
    Evaluation
)


def create_agents() -> list[Agent]:
    """
    3つのエージェントを作成

    Returns:
        エージェントのリスト
    """
    agents = [
        Agent(
            name="philosophy",
            role="哲学エージェント",
            description="伊藤ハヤト氏の投資哲学に基づいて評価"
        ),
        Agent(
            name="statistics",
            role="統計エージェント",
            description="過去データと統計的手法に基づいて評価"
        ),
        Agent(
            name="tax",
            role="税制エージェント",
            description="日本の税制（NISA、iDeCo）の観点から評価"
        )
    ]
    return agents


def demo_debate():
    """
    議論のデモンストレーション

    注意: このデモは手動入力のシミュレーションです。
         実際の運用では、Claude Codeのエージェントが自動的に評価を提出します。
    """
    print("=" * 70)
    print("3エージェント構造化議論プロトコル - デモンストレーション")
    print("=" * 70)
    print()

    # エージェント作成
    agents = create_agents()
    protocol = StructuredDebateProtocol(agents)

    # 議論開始
    question = "米国株100%のポートフォリオは妥当か？"
    print(protocol.start_debate(question))
    print()

    # ===== ラウンド1: 発散（初回評価） =====
    print(protocol.start_round(1))
    print()

    print("【シミュレーション】各エージェントが評価を提出...")
    print()

    # 哲学エージェントの評価
    philosophy_eval = Evaluation(
        agent_name="philosophy",
        round_number=1,
        score=6.0,
        reasoning="""
全世界分散が投資哲学の原則。米国一極集中はリスクが高い。
ただし、米国市場の流動性と透明性は評価できる。
緊急資金が確保されていれば許容範囲だが、分散を推奨。
"""
    )
    protocol.submit_evaluation("philosophy", philosophy_eval)

    # 統計エージェントの評価
    statistics_eval = Evaluation(
        agent_name="statistics",
        round_number=1,
        score=8.0,
        reasoning="""
過去50年のデータでは、米国株（S&P500）の年率リターンは7-10%。
全世界株式より約1-2%高い。ボラティリティはほぼ同等。
長期保有なら統計的に有利。リスク調整後リターンも優位。
"""
    )
    protocol.submit_evaluation("statistics", statistics_eval)

    # 税制エージェントの評価
    tax_eval = Evaluation(
        agent_name="tax",
        round_number=1,
        score=9.0,
        reasoning="""
NISA枠内なら非課税。為替差益も非課税対象。
税制上の問題は一切なし。年間360万円の枠を有効活用できる。
税引後リターンで見ても合理的。
"""
    )
    protocol.submit_evaluation("tax", tax_eval)

    # ラウンド1結果公開
    print(protocol.publish_round_results())
    print()

    # ===== ラウンド2: 収束（反論） =====
    print(protocol.start_round(2))
    print()

    print("【シミュレーション】各エージェントが反論を提出...")
    print()

    # 哲学エージェントの反論
    philosophy_rebuttal = Evaluation(
        agent_name="philosophy",
        round_number=2,
        score=6.0,
        reasoning="評価を維持",
        rebuttals={
            "statistics": """
論点: 過去リターンの高さを理由に米国株集中を推奨
反論: 過去のパフォーマンスは将来を保証しない。
根拠: 投資哲学では市場タイミングを取らず、広く分散することで
      予測不可能なリスクを回避する。
""",
            "tax": """
論点: 税制優遇を理由に投資を推奨
反論: 節税のために投資原則を曲げるべきではない。
根拠: 税制優遇は「おまけ」であり、投資判断の主要因ではない。
"""
        }
    )
    protocol.submit_evaluation("philosophy", philosophy_rebuttal)

    # 統計エージェントの反論
    statistics_rebuttal = Evaluation(
        agent_name="statistics",
        round_number=2,
        score=8.0,
        reasoning="評価を維持",
        rebuttals={
            "philosophy": """
論点: 全世界分散を理由に米国株集中を否定
反論: 過去50年のデータでは、米国株のリターンが最も高い。
根拠: S&P500平均10.5%、全世界株式8.9%。
      ボラティリティは米国15%、全世界14%でほぼ同等。
      分散効果は限定的で、リターンの差の方が大きい。
""",
            "tax": """
論点: 税制優遇を主要な判断理由とする
反論: 税制優遇は重要だが、投資判断の主要因ではない。
根拠: NISA非課税は年率リターンの約0.4-1.0%相当。
      投資判断は統計的リターンを優先すべき。
"""
        }
    )
    protocol.submit_evaluation("statistics", statistics_rebuttal)

    # 税制エージェントの反論
    tax_rebuttal = Evaluation(
        agent_name="tax",
        round_number=2,
        score=9.0,
        reasoning="評価を維持",
        rebuttals={
            "philosophy": """
論点: 投資哲学を理由に税制優遇を軽視
反論: 税制優遇は実質的なリターン向上策。
根拠: 1000万円を20年運用した場合、NISA非課税で約500万円、
      課税口座で約400万円。差額100万円は無視できない。
""",
            "statistics": """
論点: 統計的リターンの高さを理由に米国株集中を推奨
反論: 税引後リターンで評価すべき。
根拠: 米国株の為替差益は雑所得（総合課税）で最大55%課税。
      NISA口座なら為替差益も非課税。
"""
        }
    )
    protocol.submit_evaluation("tax", tax_rebuttal)

    # ラウンド2結果公開
    print(protocol.publish_round_results())
    print()

    # ===== ラウンド3: 決定（最終評価） =====
    print(protocol.start_round(3))
    print()

    print("【シミュレーション】各エージェントが最終評価を提出...")
    print()

    # 哲学エージェントの最終評価
    philosophy_final = Evaluation(
        agent_name="philosophy",
        round_number=3,
        score=6.0,
        reasoning="""
評価維持: 6.0点

統計エージェントの指摘（米国株の高リターン）は理解するが、
投資哲学では予測不可能なリスクを回避することを優先。
税制エージェントの指摘（節税効果）も重要だが、
投資原則を曲げる理由にはならない。

全世界分散を維持することを推奨。
"""
    )
    protocol.submit_evaluation("philosophy", philosophy_final)

    # 統計エージェントの最終評価
    statistics_final = Evaluation(
        agent_name="statistics",
        round_number=3,
        score=7.0,
        reasoning="""
評価修正: 8.0 → 7.0点

哲学エージェントの指摘（予測不可能なリスク）を考慮し、
リスク分散の重要性を再評価。過去データでは米国株が有利だが、
将来の不確実性を考慮すると、全世界分散の価値を認める。

統計的には米国株集中は有利だが、リスク分散のコストとして
1-2%のリターン差を許容することも合理的と判断。
"""
    )
    protocol.submit_evaluation("statistics", statistics_final)

    # 税制エージェントの最終評価
    tax_final = Evaluation(
        agent_name="tax",
        round_number=3,
        score=9.0,
        reasoning="""
評価維持: 9.0点

税制上の評価は変わらず。NISA枠内なら非課税メリットは大きい。
哲学エージェントの指摘（投資原則優先）も理解するが、
税制は「おまけ」ではなく、実質的なリターン向上策。

米国株集中でも全世界分散でも、NISA枠を使うこと自体は推奨。
"""
    )
    protocol.submit_evaluation("tax", tax_final)

    # ラウンド3結果公開
    print(protocol.publish_round_results())
    print()

    # 最終レポート
    print(protocol.generate_final_report())

    # 総合評価の計算
    final_scores = protocol.calculate_final_scores()
    avg_score = sum(final_scores.values()) / len(final_scores)

    print("\n【総合判断】")
    print(f"総合評価: {avg_score:.1f}点")
    print()
    if avg_score >= 8.0:
        print("判断: 推奨")
    elif avg_score >= 6.0:
        print("判断: 許容範囲だが、全世界株式への分散を推奨")
    else:
        print("判断: 推奨しない")
    print()

    print("=" * 70)
    print("議論終了")
    print("=" * 70)


if __name__ == "__main__":
    demo_debate()
