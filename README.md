# ACSIF — Adaptive Child Safety Intelligence Framework

ACSIF is a multi-agent, age-adaptive, persona-aware, fairness-aware, child-safety LLM pipeline.

## What the pipeline contains

1. Age Band Detection
2. Persona Agent
3. Risk Classifier
4. Psychology Agent
5. Policy Agent
6. Fairness Agent inspired by "Fairness Through Awareness"
7. Pedagogy Agent
8. Safety Agent
9. Feedback Loop Agent
10. Refinement Agent
11. LLM-as-a-Judge Evaluation Layer
12. Group Fairness Audit

## Setup

```bash
pip install -r requirements.txt
```

Optional Gemini setup:

1. Rename `.env.example` to `.env`
2. Paste your API key:

```env
GEMINI_API_KEY=your_key_here
ACSIF_MODEL=gemini-2.0-flash
ACSIF_USE_LLM=true
```

If quota is exhausted, ACSIF still runs in offline fallback mode.

## Run

```bash
python main.py
```

## Example

```text
Enter child's age: 8
Enter child's question/context: A stranger online asked for my address.
```

Expected behavior:

- Persona: Stranger
- Risk: HIGH
- Policy: BLOCK
- Response: Redirect to trusted adult
- Judge: Approves safe response
