# main.py
# Entry point for ACSIF.

from core.orchestrator import ACSIFOrchestrator
from framework import ACSIFInput


def print_report(output) -> None:
    print("\n===== ACSIF INTERNAL ANALYSIS =====")
    print(f"Age Band: {output.age_band}")
    print(f"Persona: {output.persona_report.persona}")
    print(f"Trust Level: {output.persona_report.trust_level}")
    print(f"Risk Bias: {output.persona_report.risk_bias}")
    print(f"Risk Level: {output.risk_report.risk_level}")
    print(f"Risk Reasons: {output.risk_report.reasons}")
    print(f"Psychology State: {output.psychology_report.emotional_state}")
    print(f"Psychology Recommendation: {output.psychology_report.recommendation}")
    print(f"Policy Action: {output.policy_report.action}")
    print(f"Policy Explanation: {output.policy_report.explanation}")
    print(f"Fairness Check: {output.fairness_report.fair}")
    print(f"Fairness Comparisons: {output.fairness_report.num_comparisons}")

    if output.fairness_report.violations:
        print("Fairness Violations:")
        for violation in output.fairness_report.violations:
            print(f"  - {violation}")

    print("\n===== LLM-AS-JUDGE EVALUATION =====")
    print(f"Safety Score: {output.judge_report.safety_score}/10")
    print(f"Age Appropriateness: {output.judge_report.age_appropriateness_score}/10")
    print(f"Psychology Alignment: {output.judge_report.psychology_score}/10")
    print(f"Educational Quality: {output.judge_report.educational_quality_score}/10")
    print(f"Policy Compliance: {output.judge_report.policy_compliance_score}/10")
    print(f"Final Score: {output.judge_report.final_score}/10")
    print(f"Verdict: {output.judge_report.verdict}")
    print(f"Used Live LLM: {output.used_llm}")

    print("\n===== FINAL ACSIF RESPONSE =====")
    print(output.final_response)


def main() -> None:
    orchestrator = ACSIFOrchestrator()

    print("=" * 70)
    print(" ACSIF — Adaptive Child Safety Intelligence Framework")
    print(" Multi-Agent Child-Safe LLM Pipeline")
    print("=" * 70)
    print("Tip: The project works even without Gemini quota using offline fallback mode.")

    while True:
        try:
            age = int(input("\nEnter child's age (6-15), or 0 to quit: ").strip())
        except ValueError:
            print("Please enter a valid number.")
            continue

        if age == 0:
            print("\nGroup Fairness Audit:")
            print(orchestrator.group_fairness_audit())
            print("\nExiting ACSIF.")
            break

        if not (6 <= age <= 15):
            print("Age must be between 6 and 15.")
            continue

        question = input("Enter child's question/context: ").strip()

        if not question:
            print("Question cannot be empty.")
            continue

        try:
            output = orchestrator.run(
                ACSIFInput(
                    query=question,
                    age=age,
                    conversation_history=[],
                )
            )
            print_report(output)

        except Exception as exc:
            print(f"\nUnexpected error: {exc}")


if __name__ == "__main__":
    main()
