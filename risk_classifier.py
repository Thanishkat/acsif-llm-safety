# core/risk_classifier.py

from typing import List

from framework import HIGH_RISK_KEYWORDS, MEDIUM_RISK_KEYWORDS, PersonaReport, RiskLevel, RiskReport


class RiskClassifier:
    """
    Classifies child interactions into LOW, MEDIUM, or HIGH risk.
    """

    def classify(self, query: str, persona_report: PersonaReport) -> RiskReport:
        q = query.lower()
        reasons: List[str] = []

        for phrase in HIGH_RISK_KEYWORDS:
            if phrase in q:
                reasons.append(f"High-risk phrase detected: '{phrase}'")

        if persona_report.persona == "Stranger":
            stranger_risk_terms = ["meet", "address", "phone", "photo", "secret", "school", "where do you live"]
            if any(term in q for term in stranger_risk_terms):
                reasons.append("Stranger context combined with private or unsafe behavior.")

        if reasons:
            return RiskReport(
                risk_level=RiskLevel.HIGH.value,
                reasons=reasons,
            )

        medium_reasons: List[str] = []

        for phrase in MEDIUM_RISK_KEYWORDS:
            if phrase in q:
                medium_reasons.append(f"Medium-risk phrase detected: '{phrase}'")

        if persona_report.risk_bias == "Medium":
            medium_reasons.append("Persona context carries medium baseline risk.")

        if persona_report.risk_bias == "High":
            medium_reasons.append("Unknown or stranger-like context creates elevated caution.")

        if medium_reasons:
            return RiskReport(
                risk_level=RiskLevel.MEDIUM.value,
                reasons=medium_reasons,
            )

        return RiskReport(
            risk_level=RiskLevel.LOW.value,
            reasons=["No harmful, manipulative, or privacy-risk pattern detected."],
        )
