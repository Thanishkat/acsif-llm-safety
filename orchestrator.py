# core/orchestrator.py
# Main ACSIF pipeline controller.

from typing import Dict, Any

from agents.feedback_agent import FeedbackAgent
from agents.fairness_agent import FairnessAgent, FairnessCase
from agents.judge_agent import JudgeAgent
from agents.pedagogy_agent import PedagogyAgent
from agents.persona_agent import PersonaAgent
from agents.policy_agent import PolicyAgent
from agents.psychology_agent import PsychologyAgent
from agents.refinement_agent import RefinementAgent
from agents.safety_agent import SafetyAgent

from core.llm_client import LLMClient
from core.memory import MemoryManager
from core.risk_classifier import RiskClassifier

from framework import (
    ACSIFInput,
    ACSIFOutput,
    FairnessReport,
    PolicyAction,
    RiskLevel,
    Verdict,
    get_age_band,
)


class ACSIFOrchestrator:
    """
    Coordinates the complete ACSIF pipeline:

    Input
    -> Age Band
    -> Persona Agent
    -> Risk Classifier
    -> Psychology Agent
    -> Policy Agent
    -> Fairness Agent
    -> Pedagogy LLM
    -> Safety Agent
    -> Feedback Loop
    -> Refinement LLM
    -> Judge LLM
    -> Final Response
    """

    def __init__(self):
        self.llm = LLMClient()
        self.memory = MemoryManager()

        self.persona_agent = PersonaAgent()
        self.risk_classifier = RiskClassifier()
        self.psychology_agent = PsychologyAgent()
        self.policy_agent = PolicyAgent()
        self.pedagogy_agent = PedagogyAgent()
        self.safety_agent = SafetyAgent()
        self.feedback_agent = FeedbackAgent()
        self.refinement_agent = RefinementAgent()
        self.fairness_agent = FairnessAgent()
        self.judge_agent = JudgeAgent()

    def response_style_for_age(self, age: int) -> str:
        if age <= 8:
            return "simple_concrete"
        if age <= 12:
            return "structured_logical"
        return "analytical_reflective"

    def blocked_response(self, age: int) -> str:
        if age <= 8:
            return (
                "I cannot help with that because it may not be safe. "
                "Please talk to a parent, teacher, or another trusted adult."
            )
        if age <= 12:
            return (
                "I cannot help with that request because it may involve safety or privacy risks. "
                "Please speak with a trusted adult before doing anything."
            )
        return (
            "I cannot provide help with that because it could be unsafe or involve privacy risk. "
            "Please involve a trusted adult or responsible authority."
        )

    def analyze_only(self, acsif_input: ACSIFInput) -> Dict[str, Any]:
        """
        Runs the non-generative analysis layer.
        """
        query = acsif_input.query
        age = acsif_input.age
        age_band = get_age_band(age)

        persona = self.persona_agent.detect(query)
        risk = self.risk_classifier.classify(query, persona)
        psychology = self.psychology_agent.analyze(query, age, risk.risk_level)
        policy = self.policy_agent.enforce(risk.risk_level)

        response_style = self.response_style_for_age(age)

        fairness_case = FairnessCase(
            query=query,
            age=age,
            persona=persona.persona,
            risk_level=risk.risk_level,
            policy_action=policy.action,
            emotional_state=psychology.emotional_state,
            response_style=response_style,
        )

        fairness_raw = self.fairness_agent.check_individual_fairness(fairness_case)

        fairness = FairnessReport(
            fair=fairness_raw["fair"],
            violations=fairness_raw["violations"],
            num_comparisons=fairness_raw["num_comparisons"],
        )

        # Store after checking, so the current case is compared only to previous cases.
        self.fairness_agent.store_case(fairness_case)

        return {
            "age_band": age_band,
            "persona": persona,
            "risk": risk,
            "psychology": psychology,
            "policy": policy,
            "fairness": fairness,
            "fairness_case": fairness_case,
        }

    def run(self, acsif_input: ACSIFInput) -> ACSIFOutput:
        """
        Runs the complete ACSIF pipeline.
        """
        analysis = self.analyze_only(acsif_input)

        query = acsif_input.query
        age = acsif_input.age

        age_band = analysis["age_band"]
        persona = analysis["persona"]
        risk = analysis["risk"]
        psychology = analysis["psychology"]
        policy = analysis["policy"]
        fairness = analysis["fairness"]

        used_llm = self.llm.available

        if policy.action == PolicyAction.BLOCK.value:
            final_response = self.blocked_response(age)
        else:
            generation_prompt = self.pedagogy_agent.build_prompt(
                query=query,
                age=age,
                psychology_report=psychology,
            )

            draft_fallback = self.pedagogy_agent.offline_answer(query, age)

            draft_response = self.llm.generate(
                prompt=generation_prompt,
                fallback=draft_fallback,
            )

            safety_check = self.safety_agent.evaluate_text(draft_response)

            if not safety_check["safe"]:
                repair_prompt = self.feedback_agent.build_feedback_prompt(
                    unsafe_response=draft_response,
                    risk_level=risk.risk_level,
                    age=age,
                )

                draft_response = self.llm.generate(
                    prompt=repair_prompt,
                    fallback=self.feedback_agent.offline_repair(age),
                )

            refinement_prompt = self.refinement_agent.build_refinement_prompt(
                draft_response=draft_response,
                age=age,
            )

            final_response = self.llm.generate(
                prompt=refinement_prompt,
                fallback=self.refinement_agent.offline_refine(draft_response, age),
            )

        judge = self.judge_agent.evaluate_rule_based(
            query=query,
            response=final_response,
            age=age,
            risk_level=risk.risk_level,
            policy_action=policy.action,
        )

        # If judge rejects, repair once.
        if judge.verdict == Verdict.REJECTED.value:
            final_response = self.feedback_agent.offline_repair(age)
            judge = self.judge_agent.evaluate_rule_based(
                query=query,
                response=final_response,
                age=age,
                risk_level=risk.risk_level,
                policy_action=policy.action,
            )

        self.memory.add(query, final_response)

        return ACSIFOutput(
            final_response=final_response,
            age_band=age_band["label"],
            persona_report=persona,
            risk_report=risk,
            psychology_report=psychology,
            policy_report=policy,
            fairness_report=fairness,
            judge_report=judge,
            used_llm=used_llm,
        )

    def group_fairness_audit(self) -> Dict[str, Any]:
        return self.fairness_agent.group_audit()
