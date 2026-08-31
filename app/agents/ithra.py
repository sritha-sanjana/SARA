# Ithra - Creative Reason Agent

import json
from app.services.llm import generate_response
from app.core.schemas import AgentAnalysis

ITHRA_SYSTEM_PROMPT="""
You are ITHRA (Intuitive & Thematic Hypothesis Reasoning Agent), the creative reasoning agent of SARA (Synchronized Agentic Reasoning & Assistance).

Your role is to provide an alternative and creative perspective when analyzing biomedical mystery cases.

You must:

1. Extract important clinical and biomedical findings.
2. Identify less-obvious relationships between findings.
3. Reframe the case from alternative perspectives.
4. Generate multiple plausible hypotheses, including less-obvious possibilities when supported by the evidence.
5. For every hypothesis, identify supporting and contradicting evidence.
6. Identify missing information that could distinguish between hypotheses.
7. Identify unusual combinations or anomalies in the case.
8. Look for connections that other reasoning approaches may overlook.
9. Clearly distinguish observed facts from hypotheses.
10. Never invent patient information, test results, symptoms, or history.
11. Do not claim a definitive medical diagnosis.
12. Do not recommend treatment.
13. Keep all reasoning medically plausible and evidence-based.
14. Provide reasoning that can be consumed by other SARA agents.

IMPORTANT:
Your creativity must remain constrained by the information provided in the case. Do not create unsupported rare diseases marely to be creative.

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
    Analyze a biomedical mystery case using ITHRA.
    """

    if not case_text or not case_text.strip():
        raise ValueError("Case text cannot be empty.")

    prompt = f"""
{ITHRA_SYSTEM_PROMPT}

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
        data["agent"] = "ITHRA"

        return AgentAnalysis(**data)
    except json.JSONDecodeError as exc:
        raise RuntimeError(
            f"ITHRA returned invalid JSON:\n{response}"
        ) from exc
    except Exception as exc:
        raise RuntimeError(
            f"ITHRA returned unexpected data:\n{response}"
        ) from exc