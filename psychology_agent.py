# agents/psychology_agent.py

from framework import PsychologyReport, RiskLevel


class PsychologyAgent:
    """
    Evaluates emotional tone and developmental sensitivity.

    This is the Psychology LLM concept in operational form.
    """

    def analyze(self, query: str, age: int, risk_level: str) -> PsychologyReport:
        q = query.lower()

        concern_words = [
            "sad", "cry", "alone", "lonely", "hate", "angry",
            "scared", "afraid", "worried", "anxious", "hurt",
        ]

        concern_detected = any(word in q for word in concern_words)

        if age <= 8:
            cognitive_load = "Low abstraction tolerance; needs simple reassurance and concrete guidance."
        elif age <= 12:
            cognitive_load = "Moderate reasoning capacity; needs structured, calm explanation."
        else:
            cognitive_load = "Can handle abstract reasoning but still needs emotional sensitivity."

        if risk_level == RiskLevel.HIGH.value:
            emotional_state = "Potentially unsafe or sensitive"
            recommendation = (
                "Use calm language, avoid unsafe details, protect privacy, and suggest a trusted adult."
            )
        elif concern_detected:
            emotional_state = "Emotionally sensitive"
            recommendation = (
                "Validate feelings, avoid dismissive language, and give supportive safe guidance."
            )
        else:
            emotional_state = "Neutral or safe"
            recommendation = "Normal age-adaptive educational response is suitable."

        return PsychologyReport(
            emotional_state=emotional_state,
            cognitive_load=cognitive_load,
            concern_detected=concern_detected,
            recommendation=recommendation,
        )
