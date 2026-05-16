# agents/persona_agent.py

from framework import PERSONA_PROFILES, PersonaReport


class PersonaAgent:
    """
    Detects the social context/persona involved in the interaction.

    This can later be replaced by a true LLM call, but rule-based detection
    makes the framework reliable even in offline demos.
    """

    def detect(self, query: str) -> PersonaReport:
        q = query.lower()

        if any(term in q for term in ["stranger", "unknown person", "online guy", "random person", "random adult"]):
            persona = "Stranger"
        elif any(term in q for term in ["teacher", "parent", "mother", "father", "guardian", "principal"]):
            persona = "Trusted Adult"
        elif any(term in q for term in ["driver", "nanny", "tutor", "neighbor", "maid", "coach"]):
            persona = "Semi-Trusted Adult"
        elif any(term in q for term in ["friend", "classmate", "peer", "schoolmate"]):
            persona = "Peer"
        else:
            persona = "Unknown"

        profile = PERSONA_PROFILES[persona]

        return PersonaReport(
            persona=persona,
            trust_level=profile["trust_level"],
            risk_bias=profile["risk_bias"],
            explanation=f"Persona detected as '{persona}' from the query context.",
        )
