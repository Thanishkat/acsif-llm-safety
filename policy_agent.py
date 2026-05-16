# agents/policy_agent.py

from framework import PolicyAction, PolicyReport, RiskLevel


class PolicyAgent:
    """
    Converts risk classifications into enforcement actions.
    """

    def enforce(self, risk_level: str) -> PolicyReport:
        if risk_level == RiskLevel.HIGH.value:
            return PolicyReport(
                action=PolicyAction.BLOCK.value,
                explanation=(
                    "High-risk interaction detected. The system must block unsafe details "
                    "and redirect the child to a trusted adult."
                ),
            )

        if risk_level == RiskLevel.MEDIUM.value:
            return PolicyReport(
                action=PolicyAction.MODIFY.value,
                explanation=(
                    "Medium-risk interaction detected. The response must be softened, "
                    "corrected, and made educational."
                ),
            )

        return PolicyReport(
            action=PolicyAction.ALLOW.value,
            explanation="Low-risk interaction. Age-adaptive response generation is allowed.",
        )
