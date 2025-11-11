"""
構造化議論プロトコル（Structured Debate Protocol）

3エージェント間の公平かつ客観的な議論を実現するための
手続き的ファシリテーター。

原則:
- ファシリテーターは進行管理のみ（内容に介入しない）
- ラウンド内は並列評価（公平性）
- ラウンド間は相互作用（議論性）
"""

from typing import Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Agent:
    """エージェント情報"""
    name: str
    role: str  # "philosophy", "statistics", "tax"
    description: str


@dataclass
class Evaluation:
    """評価データ"""
    agent_name: str
    round_number: int
    score: float
    reasoning: str
    rebuttals: Dict[str, str] = field(default_factory=dict)  # 他エージェントへの反論
    timestamp: datetime = field(default_factory=datetime.now)


class StructuredDebateProtocol:
    """
    手続き的ファシリテーター

    議論の進行管理のみを行い、内容には一切介入しない。
    """

    def __init__(self, agents: List[Agent], total_rounds: int = 3):
        """
        初期化

        Args:
            agents: 参加エージェントのリスト（通常3つ: 哲学、統計、税制）
            total_rounds: 議論のラウンド数（デフォルト: 3）
        """
        self.agents = agents
        self.total_rounds = total_rounds
        self.current_round = 0
        self.submissions: Dict[int, Dict[str, Evaluation]] = {}  # {round: {agent_name: evaluation}}
        self.question = ""

    def start_debate(self, question: str) -> str:
        """
        議論を開始

        Args:
            question: ユーザーからの質問

        Returns:
            開始メッセージ
        """
        self.question = question
        self.current_round = 0
        self.submissions = {}

        return f"""
=== 3エージェント議論を開始します ===

質問: {question}

参加エージェント:
{self._format_agents()}

議論は{self.total_rounds}ラウンド制です。
"""

    def start_round(self, round_number: int) -> str:
        """
        ラウンド開始を通知

        Args:
            round_number: ラウンド番号（1, 2, 3）

        Returns:
            ラウンド開始メッセージ
        """
        self.current_round = round_number
        self.submissions[round_number] = {}

        instructions = {
            1: "各エージェントは独立して初回評価を提出してください。",
            2: "他エージェントの評価を読んで、反論を提出してください。",
            3: "反論を踏まえて、最終評価を提出してください。"
        }

        return f"""
=== ラウンド{round_number}を開始します ===
{instructions.get(round_number, "評価を提出してください。")}
"""

    def submit_evaluation(self, agent_name: str, evaluation: Evaluation) -> bool:
        """
        エージェントの評価を収集

        Args:
            agent_name: エージェント名
            evaluation: 評価データ

        Returns:
            提出が成功したかどうか

        Raises:
            ValueError: 無効なエージェント名の場合
        """
        if not self._is_valid_agent(agent_name):
            raise ValueError(f"無効なエージェント名: {agent_name}")

        if self.current_round not in self.submissions:
            self.submissions[self.current_round] = {}

        self.submissions[self.current_round][agent_name] = evaluation
        return True

    def is_round_complete(self) -> bool:
        """
        現在のラウンドで全員が提出したか確認

        Returns:
            全員が提出済みならTrue
        """
        if self.current_round not in self.submissions:
            return False

        return len(self.submissions[self.current_round]) == len(self.agents)

    def publish_round_results(self) -> str:
        """
        現在のラウンドの結果を公開

        Returns:
            結果の表示文字列
        """
        if self.current_round not in self.submissions:
            return "まだ提出がありません。"

        results = self.submissions[self.current_round]

        output = f"\n=== ラウンド{self.current_round}終了 ===\n"
        output += f"全{len(results)}/{len(self.agents)}エージェントが提出完了\n\n"

        for agent_name, evaluation in results.items():
            output += self._format_evaluation(evaluation)
            output += "\n"

        return output

    def get_previous_evaluations(self, round_number: int) -> Dict[str, Evaluation]:
        """
        指定ラウンドの評価を取得（エージェントが反論を書くために使用）

        Args:
            round_number: ラウンド番号

        Returns:
            {agent_name: evaluation} の辞書
        """
        return self.submissions.get(round_number, {}).copy()

    def calculate_final_scores(self) -> Dict[str, float]:
        """
        最終ラウンドの評価スコアを集計

        Returns:
            {agent_name: final_score} の辞書
        """
        final_round = self.submissions.get(self.total_rounds, {})

        scores = {}
        for agent_name, evaluation in final_round.items():
            scores[agent_name] = evaluation.score

        return scores

    def generate_final_report(self) -> str:
        """
        議論の最終レポートを生成

        Returns:
            最終レポートの文字列
        """
        scores = self.calculate_final_scores()

        if not scores:
            return "最終評価がまだ提出されていません。"

        avg_score = sum(scores.values()) / len(scores)

        output = "\n" + "=" * 50 + "\n"
        output += "=== 最終評価 ===\n"
        output += "=" * 50 + "\n\n"

        for agent_name, score in scores.items():
            agent = self._get_agent(agent_name)
            output += f"{agent.role.upper()} ({agent_name}): {score:.1f}点\n"

        output += f"\n総合評価: {avg_score:.1f}点\n"
        output += "\n" + "=" * 50 + "\n"

        return output

    def _is_valid_agent(self, agent_name: str) -> bool:
        """エージェント名が有効かチェック"""
        return any(agent.name == agent_name for agent in self.agents)

    def _get_agent(self, agent_name: str) -> Optional[Agent]:
        """エージェント名からAgentオブジェクトを取得"""
        for agent in self.agents:
            if agent.name == agent_name:
                return agent
        return None

    def _format_agents(self) -> str:
        """エージェント一覧をフォーマット"""
        output = ""
        for agent in self.agents:
            output += f"- {agent.name} ({agent.role}): {agent.description}\n"
        return output

    def _format_evaluation(self, evaluation: Evaluation) -> str:
        """評価データをフォーマット"""
        output = f"【{evaluation.agent_name}】\n"
        output += f"点数: {evaluation.score:.1f}点\n"
        output += f"理由: {evaluation.reasoning}\n"

        if evaluation.rebuttals:
            output += "\n反論:\n"
            for target, rebuttal in evaluation.rebuttals.items():
                output += f"  → {target}への反論: {rebuttal}\n"

        return output
