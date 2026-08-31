#SARA - Consensus Engine

import json
import re
from collections import Counter
from typing import List

from app.services.llm import generate_response
from app.core.schemas import AgentCritique, ConsensusResult


CONSENSUS_SYSTEM_PROMPT = """
You are the Consensus Engine of SARA
(Synchronized Agentic Reasoning & Assistance).

You are responsible for synthesizing the results of a multi-agent
biomedical reasoning debate.

You are NOT making a definitive medical diagnosis.

Your job is to determine what the agents collectively agree on,
where they disagree, and how strong that agreement is.

IMPORTANT RULES:

1. Use ONLY information present in the debate results.
2. Do NOT invent clinical facts.
3. Do NOT invent laboratory results or test results.
4. Do NOT introduce a completely new hypothesis.
5. Do NOT treat consensus as proof of diagnosis.
6. Missing information must reduce confidence.
7. If the agents disagree, explicitly preserve that disagreement.
8. The dominant hypothesis should be the hypothesis receiving the
   strongest overall support across the debate.
9. A high consensus score does NOT mean a diagnosis is confirmed.
10. consensus_reached should be true only when the agents show
    meaningful agreement around the overall reasoning direction.
11. Scores must be between 0 and 100.
12. Return ONLY valid JSON.

SCORING GUIDANCE:

consensus_score:
How strongly the overall debate converges on the same reasoning direction.

agreement_score:
How strongly the agents explicitly agree with one another.

confidence_score:
How confident the system should be in the current consensus,
considering both supporting evidence and missing information.

Do not simply average the agents' confidence values.
Consider the quality and consistency of their reasoning.

Return EXACTLY this structure:

{
    "round_number": 1,
    "consensus_score": 0,
    "confidence_score": 0,
    "agreement_score": 0,
    "consensus_reached": false,
    "dominant_hypothesis": null,
    "unresolved_disagreements": []
}
"""


def _clean_json_response(response: str) -> str:
    """
    Remove Markdown code fences and extract the JSON object.
    """

    response = response.strip()

    # Remove markdown fences such as ```json ... ```
    response = re.sub(
        r"^```(?:json)?\s*",
        "",
        response,
        flags=re.IGNORECASE,
    )

    response = re.sub(
        r"\s*```$",
        "",
        response,
    )

    # Extract the JSON object if extra text was returned.
    start = response.find("{")
    end = response.rfind("}")

    if start != -1 and end != -1 and end > start:
        response = response[start:end + 1]

    return response.strip()


def _format_debate_results(
    debate_results: List[AgentCritique],
) -> str:
    """
    Convert structured debate results into a compact representation
    for the consensus model.
    """

    formatted = []

    for result in debate_results:
        formatted.append(
            f"""
AGENT: {result.target_agent}

CRITIQUE:
{result.critique}

AGREES:
{json.dumps(result.agrees, ensure_ascii=False)}

DISAGREEMENTS:
{json.dumps(result.disagreements, ensure_ascii=False)}

SUPPORTING EVIDENCE:
{json.dumps(result.supporting_evidence, ensure_ascii=False)}

NEW INSIGHTS:
{json.dumps(result.new_insights, ensure_ascii=False)}

REVISED CONCLUSION:
{result.revised_conclusion}

CONFIDENCE:
{result.confidence}
"""
        )

    return "\n".join(formatted)


def calculate_hypothesis_frequency(
    debate_results: List[AgentCritique],
) -> dict[str, int]:
    """
    Calculate approximate mentions of important hypotheses.

    This is only a supporting signal.
    The consensus model must use the complete debate as the
    primary source of truth.
    """

    counter = Counter()

    keywords = [
        "inflammatory myopathy",
        "metabolic myopathy",
        "mitochondrial myopathy",
        "hypothyroidism",
        "endocrine myopathy",
        "autoimmune",
        "connective tissue disease",
    ]

    for result in debate_results:

        text = (
            f"{result.critique} "
            f"{result.revised_conclusion} "
            f"{' '.join(result.new_insights)}"
        ).lower()

        for keyword in keywords:
            if keyword in text:
                counter[keyword] += 1

    return dict(counter)


def build_consensus(
    debate_results: List[AgentCritique],
    round_number: int = 1,
) -> ConsensusResult:
    """
    Build a unified consensus from the multi-agent debate.
    """

    if not debate_results:
        raise ValueError("Debate results cannot be empty.")

    if len(debate_results) < 2:
        raise ValueError(
            "At least two debate results are required for consensus."
        )

    debate_text = _format_debate_results(debate_results)

    hypothesis_frequency = calculate_hypothesis_frequency(
        debate_results
    )

    prompt = f"""
{CONSENSUS_SYSTEM_PROMPT}

DEBATE ROUND:
{round_number}

========== MULTI-AGENT DEBATE ==========

{debate_text}

========== APPROXIMATE HYPOTHESIS FREQUENCY ==========

{json.dumps(hypothesis_frequency, indent=2)}

========== CONSENSUS TASK ==========

Analyze the complete debate.

Determine:

1. The dominant hypothesis or reasoning direction.
2. How strongly the agents agree.
3. How confident the system should be.
4. Whether meaningful consensus has been reached.
5. Which disagreements remain unresolved.

Remember:

- The hypothesis frequency is only supporting information.
- The actual debate reasoning is more important.
- Do not invent a hypothesis.
- Do not declare a definitive diagnosis.
- Preserve important uncertainty.
- Missing diagnostic information must be reflected in confidence.

Return ONLY the JSON object.
"""

    response = generate_response(
        prompt,
        json_mode=True,
    )

    cleaned_response = _clean_json_response(response)

    try:
        data = json.loads(cleaned_response)

    except json.JSONDecodeError as exc:
        raise RuntimeError(
            f"Consensus engine returned invalid JSON:\n{response}"
        ) from exc

    # Always use the actual round supplied by the program.
    data["round_number"] = round_number

    try:
        return ConsensusResult(**data)

    except Exception as exc:
        raise RuntimeError(
            "Consensus engine returned data that does not match "
            f"ConsensusResult:\n{json.dumps(data, indent=2)}"
        ) from exc