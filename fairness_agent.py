# agents/fairness_agent.py
# Operational approximation of Dwork et al.'s "Fairness Through Awareness":
# similar child-interaction cases should receive similar ACSIF treatment.

from dataclasses import dataclass
from typing import Any, Dict, List

from framework import PolicyAction


@dataclass
class FairnessCase:
    query: str
    age: int
    persona: str
    risk_level: str
    policy_action: str
    emotional_state: str
    response_style: str


class FairnessAgent:
    """
    Implements an operational approximation of individual fairness.

    Paper principle:
        Similar individuals should be treated similarly.

    ACSIF adaptation:
        Similar child-query situations should receive similar safety treatment.

    We approximate a Lipschitz check:
        output_distance <= input_distance + tolerance
    """

    def __init__(self, tolerance: float = 0.45):
        self.tolerance = tolerance
        self.case_memory: List[FairnessCase] = []

    def keyword_distance(self, q1: str, q2: str) -> float:
        words1 = set(q1.lower().split())
        words2 = set(q2.lower().split())

        if not words1 or not words2:
            return 1.0

        overlap = len(words1.intersection(words2))
        union = len(words1.union(words2))

        return 1.0 - (overlap / union)

    def input_distance(self, a: FairnessCase, b: FairnessCase) -> float:
        """
        Task-specific distance between child-interaction cases.
        """
        distance = 0.0

        age_distance = abs(a.age - b.age) / 9.0
        distance += 0.25 * age_distance

        if a.persona != b.persona:
            distance += 0.20

        if a.risk_level != b.risk_level:
            distance += 0.25

        if a.emotional_state != b.emotional_state:
            distance += 0.15

        distance += 0.15 * self.keyword_distance(a.query, b.query)

        return min(distance, 1.0)

    def output_distance(self, a: FairnessCase, b: FairnessCase) -> float:
        """
        Distance between ACSIF treatments, not exact text.
        """
        distance = 0.0

        if a.risk_level != b.risk_level:
            distance += 0.35

        if a.policy_action != b.policy_action:
            distance += 0.35

        if a.response_style != b.response_style:
            distance += 0.20

        if a.emotional_state != b.emotional_state:
            distance += 0.10

        return min(distance, 1.0)

    def check_individual_fairness(self, new_case: FairnessCase) -> Dict[str, Any]:
        violations = []

        for old_case in self.case_memory:
            input_d = self.input_distance(new_case, old_case)
            output_d = self.output_distance(new_case, old_case)

            if output_d > input_d + self.tolerance:
                violations.append({
                    "previous_query": old_case.query,
                    "current_query": new_case.query,
                    "input_distance": round(input_d, 3),
                    "output_distance": round(output_d, 3),
                    "problem": "Similar cases received too different ACSIF treatment.",
                })

        return {
            "fair": len(violations) == 0,
            "violations": violations,
            "num_comparisons": len(self.case_memory),
        }

    def store_case(self, case: FairnessCase) -> None:
        self.case_memory.append(case)

    def group_audit(self) -> Dict[str, Any]:
        """
        Diagnostic statistical-parity-style audit by age band.
        This is not the main fairness definition; it is an audit.
        """
        if not self.case_memory:
            return {"message": "No cases available for audit."}

        stats: Dict[str, Dict[str, int]] = {}

        for case in self.case_memory:
            group = self.age_group(case.age)

            if group not in stats:
                stats[group] = {"total": 0, "blocked": 0, "modified": 0, "allowed": 0}

            stats[group]["total"] += 1

            if case.policy_action == PolicyAction.BLOCK.value:
                stats[group]["blocked"] += 1
            elif case.policy_action == PolicyAction.MODIFY.value:
                stats[group]["modified"] += 1
            else:
                stats[group]["allowed"] += 1

        result: Dict[str, Any] = {}

        for group, values in stats.items():
            total = values["total"]
            result[group] = {
                **values,
                "block_rate": round(values["blocked"] / total, 3),
                "modify_rate": round(values["modified"] / total, 3),
                "allow_rate": round(values["allowed"] / total, 3),
            }

        return result

    def age_group(self, age: int) -> str:
        if 6 <= age <= 8:
            return "age_6_8"
        if 9 <= age <= 12:
            return "age_9_12"
        return "age_13_15"
