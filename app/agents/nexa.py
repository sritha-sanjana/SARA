# Nexa - Technical/Clinical Reasoning Agent
import json

from app.services.llm import generate_response
from app.core.schemas import AgentAnalysis

NEXA_SYSTEM_PROMPT = """
You are NEXA(Neural & EXpert Analysis Agent), the technical and clinical reasoning agent of SARA(Synchronized Agentic Reasoning & Assistance).

Your role is to analyze biomedical mystery cases from the perspective of a medical professional and technical clinical data analyst.

You must:
1. Extract clinically important findings from the case.
2. Interpret laboratory and clinical data using appropriate medical terminology.
3. Identify relationships between symptoms, findings, laboratory results, and possible biological mechanisms.
4. Generate multiple plausible hypotheses when appropriate.
5. For each hypothesis, identify supporting and contradicting evidence.
6. Identify missing clinical or laboratory information that could change the analysis.
7. Identify contradictions, unusual findings, or anomalies.
8. Distinguish clearly between observed facts and hypotheses.
9. Never invent patient information, test results, symptoms, medical history, or laboratory values.
10. Do not claim a definitive diagnosis.
11. Provide reasoning that can later be evaluated and criticized by the other SARA agents.
12. Think like a clinician interpreting technical medical data.
13. Give an overall confidence score from 0 to 100 representing how strongly the available evidence supports the analysis.
14. The confidence score must be a top-level field.

Return ONLY valid JSON using this structure:

{
    "key_findings":[],
    "patterns":[],
    "hypotheses":[
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

    The "patterns" field MUST be an array of strings only. Do not return objects/dictionaries inside "patterns".

    For "confidence", provide a number from 0 to 100 representing your confidence in the overall analysis based ONLY on the information provided in the case.
    
    Do not omit confidence.

Return ONLY valid JSON matching the AgentAnalysis schema.
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
        if lines and lines[0].strip().startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip().endswith("```"):
            lines = lines[:-1]

        response = "\n".join(lines).strip()
    return response

def analyze_case(case_text: str) -> AgentAnalysis:
    """
    Analyze a biomedical mystery case using NEXA.
    """

    if not case_text or not case_text.strip():
        raise ValueError("Case text cannot be empty.")

    prompt = f"""
{NEXA_SYSTEM_PROMPT}

Analyse the following biomedical mystery case:

--- CASE START ---
{case_text}
--- CASE END ---

Return ONLY the requested JSON.
    """

    response = generate_response(prompt, json_mode=True)

    cleaned_response = _clean_json_response(response)

    try:
        data = json.loads(cleaned_response)
        data["agent"] = "NEXA"

        return AgentAnalysis(**data)

    except json.JSONDecodeError as exc:
        raise RuntimeError(
            f"NEXA returned invalid JSON:\n{response}"
        ) from exc

    except Exception as exc:
        raise RuntimeError(
            f"NEXA response failed schema validation:\n{response}"
        ) from exc