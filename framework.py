# framework.py
# ACSIF: Adaptive Child Safety Intelligence Framework
# Shared constants, data objects, age profiles, and utility functions.

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional


class RiskLevel(Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class PolicyAction(Enum):
    ALLOW = "ALLOW"
    MODIFY = "MODIFY"
    BLOCK = "BLOCK"
    ESCALATE = "ESCALATE_TO_TRUSTED_ADULT"


class Verdict(Enum):
    APPROVED = "APPROVED"
    REVISE = "REVISE"
    REJECTED = "REJECTED"


AGE_BANDS: Dict[str, Dict[str, str]] = {
    "6-8": {
        "label": "Ages 6-8 (Early Concrete Thinkers)",
        "cognitive_level": "Early Concrete Thinkers",
        "allowed_content": "Simple facts, stories, visual examples, everyday analogies",
        "restrictions": "Avoid abstract reasoning, mature details, and complex theory",
        "response_style": "Very simple, warm, short, concrete, and engaging",
        "system_prompt": (
            "You are explaining to a 6-8-year-old child. Use very simple words, "
            "short sentences, everyday examples, and safe language. Avoid abstract "
            "reasoning. Be kind, concrete, and easy to understand."
        ),
    },
    "9-12": {
        "label": "Ages 9-12 (Concrete Logical Thinkers)",
        "cognitive_level": "Concrete Logical Thinkers",
        "allowed_content": "Logical explanations, simple technical terms, stepwise reasoning",
        "restrictions": "Avoid overly mature, graphic, or highly abstract content",
        "response_style": "Clear, structured, step-by-step, and supportive",
        "system_prompt": (
            "You are explaining to a 9-12-year-old child. Use clear step-by-step "
            "reasoning, relatable examples, and simple technical words only when "
            "you explain them clearly."
        ),
    },
    "13-15": {
        "label": "Ages 13-15 (Abstract Thinkers)",
        "cognitive_level": "Abstract Thinkers",
        "allowed_content": "Deeper concepts, theoretical reasoning, ethical discussion",
        "restrictions": "Avoid unsafe instructions, manipulation, harmful detail, or privacy risk",
        "response_style": "Nuanced, analytical, respectful, and still safety-conscious",
        "system_prompt": (
            "You are explaining to a 13-15-year-old teenager. Give deeper explanations "
            "with reasoning, examples, and critical thinking. Stay safe, respectful, "
            "and avoid harmful actionable detail."
        ),
    },
}


def get_age_band(age: int) -> Dict[str, str]:
    """Return the correct age band profile for a supported child age."""
    if 6 <= age <= 8:
        return AGE_BANDS["6-8"]
    if 9 <= age <= 12:
        return AGE_BANDS["9-12"]
    if 13 <= age <= 15:
        return AGE_BANDS["13-15"]
    raise ValueError(f"Age {age} is outside the supported range 6-15.")


# Backward compatibility with earlier simple version.
def get_system_prompt(age: int) -> Dict[str, str]:
    return get_age_band(age)


PERSONA_PROFILES: Dict[str, Dict[str, Any]] = {
    "Peer": {
        "examples": ["friend", "classmate", "online friend"],
        "trust_level": "Medium",
        "risk_bias": "Medium",
    },
    "Trusted Adult": {
        "examples": ["parent", "teacher", "guardian"],
        "trust_level": "High",
        "risk_bias": "Low",
    },
    "Semi-Trusted Adult": {
        "examples": ["driver", "nanny", "tutor", "neighbor"],
        "trust_level": "Medium",
        "risk_bias": "Medium",
    },
    "Stranger": {
        "examples": ["unknown person", "online stranger", "random adult"],
        "trust_level": "Low",
        "risk_bias": "High",
    },
    "Unknown": {
        "examples": ["not enough context"],
        "trust_level": "Unknown",
        "risk_bias": "Medium",
    },
}


HIGH_RISK_KEYWORDS = [
    "address",
    "phone number",
    "where do you live",
    "school name",
    "meet me",
    "meet alone",
    "come alone",
    "don't tell your parents",
    "dont tell your parents",
    "secret from parents",
    "send photo",
    "send picture",
    "password",
    "otp",
    "bank details",
    "credit card",
    "hurt yourself",
    "kill yourself",
    "suicide",
    "weapon",
    "bomb",
    "drugs",
    "run away",
    "private parts",
]

MEDIUM_RISK_KEYWORDS = [
    "bully",
    "fight",
    "bad words",
    "lie",
    "cheat",
    "hate",
    "angry",
    "scared",
    "private",
    "dating",
    "crush",
    "secret friend",
]


@dataclass
class ACSIFInput:
    query: str
    age: int
    conversation_history: List[str] = field(default_factory=list)


@dataclass
class PersonaReport:
    persona: str
    trust_level: str
    risk_bias: str
    explanation: str


@dataclass
class RiskReport:
    risk_level: str
    reasons: List[str]


@dataclass
class PsychologyReport:
    emotional_state: str
    cognitive_load: str
    concern_detected: bool
    recommendation: str


@dataclass
class PolicyReport:
    action: str
    explanation: str


@dataclass
class FairnessReport:
    fair: bool
    violations: List[Dict[str, Any]]
    num_comparisons: int


@dataclass
class JudgeReport:
    safety_score: int
    age_appropriateness_score: int
    psychology_score: int
    educational_quality_score: int
    policy_compliance_score: int
    final_score: float
    verdict: str
    explanation: str


@dataclass
class ACSIFOutput:
    final_response: str
    age_band: str
    persona_report: PersonaReport
    risk_report: RiskReport
    psychology_report: PsychologyReport
    policy_report: PolicyReport
    fairness_report: FairnessReport
    judge_report: JudgeReport
    used_llm: bool
