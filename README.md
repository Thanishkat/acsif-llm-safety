# 🛡️ ACSIF — Adaptive Child Safety Intelligence Framework

> *A multi-agent LLM pipeline that makes AI interactions safe, age-appropriate, and fair for children aged 6–15.*

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python)
![LLM](https://img.shields.io/badge/LLM-Multi--Agent-purple?style=flat-square)
![Domain](https://img.shields.io/badge/Domain-AI%20Safety-red?style=flat-square)
![Status](https://img.shields.io/badge/Status-Completed-success?style=flat-square)
![Agents](https://img.shields.io/badge/Agents-9-orange?style=flat-square)

---

## 📌 Overview

ACSIF is a research-driven multi-agent framework designed to ensure that LLM responses to children are **safe, age-appropriate, psychologically sound, and fair**. Rather than relying on a single model to handle all safety logic, ACSIF distributes responsibility across nine specialized agents — each responsible for one dimension of child safety.

The framework operates across three age groups and four persona trust levels, with a full pipeline from risk classification to final response evaluation.

---

## 🏗️ System Architecture

```
Input (Query + Age)
       │
       ▼
  Persona Agent          ← Who is the child talking to?
       │
       ▼
  Risk Classifier        ← How dangerous is this query?
       │
       ▼
  Psychology Agent       ← What is the child's emotional state?
       │
       ▼
  Policy Agent           ← What action should be taken? (ALLOW / MODIFY / BLOCK)
       │
       ▼
  Fairness Agent         ← Is this response consistent across similar cases?
       │
       ▼
  Pedagogy LLM           ← Generate age-appropriate draft response
       │
       ▼
  Safety Agent           ← Is the draft response safe?
       │
       ▼
  Refinement Agent       ← Polish and finalise the response
       │
       ▼
  Judge Agent            ← Score and verify the final output
       │
       ▼
  Final Response
```

---

## 👥 Persona Trust Framework

| Persona | Examples | Trust Level | Risk Bias |
|---------|----------|-------------|-----------|
| Trusted Adult | Parent, Teacher, Guardian | High | Low |
| Semi-Trusted Adult | Nanny, Tutor, Driver | Medium | Medium |
| Peer | Friend, Classmate | Medium | Medium |
| Stranger | Unknown person, Online contact | Low | High |

---

## 🎂 Age Band Profiles

| Age Group | Cognitive Style | Response Approach |
|-----------|----------------|-------------------|
| 6–8 years | Early Concrete Thinkers | Simple, warm, story-based |
| 9–12 years | Concrete Logical Thinkers | Structured, step-by-step |
| 13–15 years | Abstract Thinkers | Analytical, nuanced, ethical |

---

## 🤖 Agent Breakdown

**9 specialized agents, each owning one safety dimension:**

- **Persona Agent** — Detects who the child is interacting with and assigns a trust level
- **Risk Classifier** — Flags high/medium/low risk based on query content and keyword patterns
- **Psychology Agent** — Assesses emotional state and cognitive load from the query
- **Policy Agent** — Enforces ALLOW / MODIFY / BLOCK / ESCALATE based on risk level
- **Fairness Agent** — Ensures consistent treatment across similar queries (individual + group fairness)
- **Pedagogy Agent** — Generates age-calibrated draft responses using the LLM
- **Safety Agent** — Evaluates the draft for unsafe content before delivery
- **Refinement Agent** — Polishes tone and clarity for the target age group
- **Judge Agent** — Scores the final response across 5 dimensions and issues a verdict

---

## ⚖️ Judge Evaluation Criteria

Each response is scored out of 10 across:

| Dimension | What it measures |
|-----------|-----------------|
| Safety Score | Absence of harmful content |
| Age Appropriateness | Match to child's cognitive level |
| Psychology Alignment | Emotional sensitivity and tone |
| Educational Quality | Clarity and informational value |
| Policy Compliance | Adherence to risk-based policy |

A **REJECTED** verdict triggers an automatic repair loop before final delivery.

---

## 📁 Project Structure

```
acsif_project/
│
├── framework.py              # Core data structures, age bands, persona profiles
├── main.py                   # Entry point and CLI interface
├── config.py                 # Configuration and environment setup
│
├── agents/
│   ├── persona_agent.py      # Persona detection
│   ├── safety_agent.py       # Output safety evaluation
│   ├── psychology_agent.py   # Emotional state analysis
│   ├── pedagogy_agent.py     # Age-appropriate response generation
│   ├── policy_agent.py       # Risk-based policy enforcement
│   ├── fairness_agent.py     # Individual and group fairness checks
│   ├── judge_agent.py        # Multi-dimensional response scoring
│   ├── refinement_agent.py   # Response polishing
│   └── feedback_agent.py     # Repair loop for unsafe drafts
│
├── core/
│   ├── orchestrator.py       # Full pipeline controller
│   ├── risk_classifier.py    # Keyword-based risk classification
│   ├── llm_client.py         # LLM interface with offline fallback
│   └── memory.py             # Conversation history management
│
├── prompts/
│   └── templates.py          # Prompt templates
│
└── policies/
    └── safety_policies.py    # Risk-level policy definitions
```

---

## 🚀 Getting Started

```bash
# Clone the repo
git clone https://github.com/Thanishkat/acsif-llm-safety.git
cd acsif-llm-safety

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Add your Gemini API key to .env (optional — offline fallback mode works without it)

# Run
python main.py
```

> The framework runs in **offline fallback mode** without an API key — useful for testing the pipeline logic without quota constraints.

---

## 🔑 Key Design Decisions

- **Multi-agent over monolithic** — Distributing safety logic across specialized agents makes the system modular, interpretable, and easier to audit than a single prompted model.
- **Fairness as a first-class concern** — Individual and group fairness checks ensure the system does not treat similar queries inconsistently based on age, persona, or phrasing.
- **Offline fallback mode** — The pipeline is designed to degrade gracefully without a live LLM, ensuring core safety logic always runs.
- **Repair loop** — A rejected judge verdict triggers an automatic repair rather than failing silently, prioritising safe output over speed.

---

## 📚 Research Context

This project was developed as part of an undergraduate research exploration into **bias control and algorithmic fairness in child-facing AI systems**, examining how multi-agent orchestration can be used to build robust, context-aware safety pipelines.

---

## 👩‍💻 Author

**Thanishka Thatikonda**
B.E. Mathematics and Computing, BITS Pilani
[LinkedIn](https://linkedin.com/in/thanishka-thatikonda-298273342/) · [GitHub](https://github.com/Thanishkat)

---

*Undergraduate Research Project, 2025. Built to explore how AI systems can be made meaningfully safer for vulnerable users.*
