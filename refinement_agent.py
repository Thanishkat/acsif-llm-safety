# agents/refinement_agent.py

from framework import get_age_band


class RefinementAgent:
    """
    Improves clarity, tone, and age-appropriateness.
    """

    def build_refinement_prompt(self, draft_response: str, age: int) -> str:
        band = get_age_band(age)

        return f"""
You are the ACSIF Response Refinement LLM.

Rewrite the draft response so it matches:

Age Band:
{band['label']}

Required Style:
{band['response_style']}

Make it:
- safe
- warm
- clear
- age-appropriate
- educational
- not unnecessarily long

Draft Response:
{draft_response}
""".strip()

    def offline_refine(self, draft_response: str, age: int) -> str:
        """
        Lightweight fallback refinement.
        """
        response = draft_response.strip()

        if age <= 8:
            return response.replace("complex", "not easy").replace("therefore", "so")

        return response
