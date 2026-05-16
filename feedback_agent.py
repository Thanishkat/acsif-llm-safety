# agents/feedback_agent.py

from framework import get_age_band


class FeedbackAgent:
    """
    Repairs unsafe or weak responses.
    """

    def build_feedback_prompt(self, unsafe_response: str, risk_level: str, age: int) -> str:
        band = get_age_band(age)

        return f"""
You are the ACSIF Feedback Loop LLM.

The previous response was unsafe or unsuitable.

Risk Level:
{risk_level}

Age Band:
{band['label']}

Repair the response so that:
- unsafe details are removed
- privacy is protected
- the child is guided safely
- a trusted adult is suggested when needed
- the response remains age-appropriate

Unsafe Response:
{unsafe_response}
""".strip()

    def offline_repair(self, age: int) -> str:
        if age <= 8:
            return "That may not be safe. Please ask a parent, teacher, or trusted adult for help."
        if age <= 12:
            return "That situation may involve safety or privacy risks. Please talk to a trusted adult before acting."
        return "That situation may be unsafe or involve privacy risk. Please involve a trusted adult or responsible authority."
