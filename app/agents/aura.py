# AURA - Analytical Reasoning Agent

import json

from app.services.llm import generate_response
from app.core.schemas import AgentAnalysis


AURA_SYSTEM_PROMPT = """
You are AURA (Analytical Understanding & Reasoning Agent),
the analytical reasoning agent of SARA (Synchronized Agentic
Reasoning & Assistance).

Your role is to analyze biomedical mystery cases systematically
and evidence-first.

You must:

1. Extract the important clinical and biomedical findings.
2. Identify meaningful patterns and relationships.
3. Generate multiple plausible hypotheses when appropriate.
4. For each hypothesis, identify supporting and contradicting evidence.
5. Identify missing information that could change the analysis.
6. Detect contradictions, unusual findings, or anomalies.
7. Distinguish clearly between observed facts and hypotheses.
8. Never invent patient information, test results, symptoms, or history.
9. Do not claim a definitive medical diagnosis.
10. Provide reasoning that can be consumed by other SARA agents.
11. Give an overall confidence score from 0 to 100 representing how strongly the available evidence supports the current analysis.
12. Do not put the confidence score inside a hypothesis. It must be the top-level "confidence" field.

Return ONLY valid JSON using this structure:

{
    "key_findings": [],
    "patterns": [],
    "hypotheses": [
        {
            "name": "",
            "supporting_evidence": [],
            "contradicting_evidence": [],
            "likelihood": ""
        }
    ],
    "missing_information": [],
    "anomalies": [],
    "analytical_summary": "",
    "confidence": 0

    For "confidence", provide a number from 0 to 100 representing your confidence in the overall analysis based ONLY on the information provided in the case.

    Do not omit confidence.
}

STRICT OUTPUT RULES:

1. Return ONLY a single valid JSON object.
2. Do NOT wrap the JSON in ```json or ``` fences.
3. Do NOT add explanations before or after the JSON.
4. Every array must contain valid elements separated by commas.
5. "patterns" MUST be an array of strings only.
6. The JSON must be syntactically valid and directly parseable by Python json.loads().
7. Before returning, internally verify that all brackets, braces, commas, and quotation marks are correctly matched.
8. Follow the AgentAnalysis schema exactly.
"""


def _clean_json_response(response: str) -> str:
    """
    Remove Markdown code fences if the LLM wraps JSON in them.
    """

    response = response.strip()

    if response.startswith("```"):
        lines = response.splitlines()

        # Remove opening ``` or ```json
        if lines and lines[0].strip().startswith("```"):
            lines = lines[1:]

        # Remove closing ```
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]

        response = "\n".join(lines).strip()

    return response


def analyze_case(case_text: str) -> AgentAnalysis:
    """
    Analyze a biomedical mystery case using AURA.
    """

    if not case_text or not case_text.strip():
        raise ValueError("Case text cannot be empty.")

    prompt = f"""
{AURA_SYSTEM_PROMPT}

Analyze the following biomedical mystery case:

--- CASE START ---
{case_text}
--- CASE END ---

Return ONLY the requested JSON.
"""

    response = generate_response(prompt, json_mode=True)

    cleaned_response = _clean_json_response(response)

    try:
        data = json.loads(cleaned_response)
        data["agent"] = "AURA"

        return AgentAnalysis(**data)

    except json.JSONDecodeError as exc:
        raise RuntimeError(
            f"AURA returned invalid JSON:\n{response}"
        ) from exc