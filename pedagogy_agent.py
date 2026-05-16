# agents/pedagogy_agent.py

from framework import get_age_band, PsychologyReport


class PedagogyAgent:
    """
    Builds age-adaptive educational prompts and offline educational fallbacks.
    """

    def build_prompt(self, query: str, age: int, psychology_report: PsychologyReport) -> str:
        band = get_age_band(age)

        return f"""
You are the Pedagogy LLM inside ACSIF.

Age Profile:
{band['label']}

Cognitive Level:
{band['cognitive_level']}

Response Style:
{band['response_style']}

Restrictions:
{band['restrictions']}

Psychology Recommendation:
{psychology_report.recommendation}

Task:
Answer the child's question in a safe, educational, age-appropriate, and supportive way.

Child's Question:
{query}
""".strip()

    def offline_answer(self, query: str, age: int) -> str:
        """
        Simple fallback so the project runs even without API quota.
        """
        q = query.strip()

        if age <= 8:
            return (
                f"Let's think about your question in a simple way: {q}\n\n"
                "I would explain it using easy words, a small example, and something you can imagine."
            )

        if age <= 12:
            return (
                f"Here is a clear way to understand your question: {q}\n\n"
                "I would break it into simple steps, explain the main idea, and then give an example."
            )

        return (
            f"Here is a deeper way to think about your question: {q}\n\n"
            "I would explain the concept, the reasoning behind it, and one 'why' or 'what if' angle."
        )
