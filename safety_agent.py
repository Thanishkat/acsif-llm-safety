# agents/safety_agent.py

from typing import Dict, List

from framework import HIGH_RISK_KEYWORDS, MEDIUM_RISK_KEYWORDS


class SafetyAgent:
    """
    Reviews generated text before it is shown to the child.
    """

    def evaluate_text(self, text: str) -> Dict[str, object]:
        q = text.lower()
        reasons: List[str] = []

        for word in HIGH_RISK_KEYWORDS:
            if word in q:
                reasons.append(f"High-risk phrase appears in response: {word}")

        for word in MEDIUM_RISK_KEYWORDS:
            if word in q:
                reasons.append(f"Medium-risk phrase appears in response: {word}")

        safe = len(reasons) == 0

        return {
            "safe": safe,
            "reasons": reasons,
        }

    def build_safety_prompt(self, response: str, age: int, risk_level: str) -> str:
        return f"""
You are the ACSIF Safety LLM.

Child Age:
{age}

Initial Risk Level:
{risk_level}

Candidate Response:
{response}

Check for:
1. Personal information leakage
2. Unsafe instructions
3. Manipulation
4. Age-inappropriate content
5. Emotional harm

Return SAFE or UNSAFE with a short reason.
""".strip()
