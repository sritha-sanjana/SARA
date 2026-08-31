# app/core/final_synthesis.py

import json
import re
from typing import Dict, List

from app.core.schemas import (
    AgentAnalysis,
    AgentCritique,
    ConsensusResult,
)
from app.services.llm import generate_response


def _clean_json_response(response: str) -> str:
    """
    Remove Markdown code fences and extract the JSON object
    from the model response.
    """

    response = response.strip()

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

    start = response.find("{")
    end = response.rfind("}")

    if start != -1 and end != -1 and end > start:
        response = response[start:end + 1]

    return response.strip()


def _serialize_analyses(
    analyses: Dict[str, AgentAnalysis]
) -> dict:
    """
    Convert AgentAnalysis Pydantic models into normal dictionaries
    so they can be serialized into JSON.
    """

    return {
        agent_name: analysis.model_dump()
        for agent_name, analysis in analyses.items()
    }


def _serialize_debates(
    debates: List[AgentCritique]
) -> list:
    """
    Convert AgentCritique Pydantic models into normal dictionaries.
    """

    return [
        debate.model_dump()
        for debate in debates
    ]


def _serialize_consensus(
    consensus: ConsensusResult
) -> dict:
    """
    Convert ConsensusResult Pydantic model into a normal dictionary.
    """

    return consensus.model_dump()


def synthesize_final_result(
    analyses: Dict[str, AgentAnalysis],
    debates: List[AgentCritique],
    consensus: ConsensusResult,
) -> dict:
    """
    Build the final SARA clinical reasoning synthesis.

    Inputs:
        analyses:
            Individual analyses produced by AURA, NEXA, LYRA and ITHRA.

        debates:
            Critiques produced during the multi-agent debate.

        consensus:
            Consensus produced by the consensus engine.

    Returns:
        Structured final synthesis as a dictionary.
    """

    # ---------------------------------------------------------
    # VALIDATION
    # ---------------------------------------------------------

    if not analyses:
        raise ValueError("Agent analyses cannot be empty.")

    if not debates:
        raise ValueError("Debate results cannot be empty.")

    if consensus is None:
        raise ValueError("Consensus result cannot be empty.")

    # ---------------------------------------------------------
    # SERIALIZATION
    # ---------------------------------------------------------

    # Pydantic objects cannot be passed directly to json.dumps().
    # Convert them into normal Python dictionaries/lists first.

    serialized_analyses = _serialize_analyses(analyses)

    serialized_debates = _serialize_debates(debates)

    serialized_consensus = _serialize_consensus(consensus)

    # ---------------------------------------------------------
    # FINAL SYNTHESIS PROMPT
    # ---------------------------------------------------------

    prompt = f"""
You are SARA's Final Synthesis Engine.

Your task is to combine:

1. Individual analyses from AURA, NEXA, LYRA and ITHRA.
2. The multi-agent debate results.
3. The final consensus.

Produce one structured clinical reasoning summary.

IMPORTANT SAFETY RULES:

- Do NOT invent patient information.
- Do NOT claim a definitive diagnosis.
- Do NOT present a hypothesis as confirmed.
- Clearly distinguish the leading clinical direction from alternatives.
- Preserve uncertainty and unresolved disagreements.
- Base conclusions only on the information provided.
- Do NOT introduce hypotheses that were not discussed by the agents.
- Recommended investigations must come from the missing information
  or workup discussed by the agents.
- This is an AI-assisted clinical reasoning system,
  NOT a medical diagnosis tool.

================ AGENT ANALYSES ================

{json.dumps(serialized_analyses, indent=2)}

================ DEBATE RESULTS ================

{json.dumps(serialized_debates, indent=2)}

================ CONSENSUS ================

{json.dumps(serialized_consensus, indent=2)}

=================================================

Return ONLY valid JSON.

Use EXACTLY this structure:

{{
    "primary_clinical_direction": "",
    "confidence": 0,
    "reasoning": [
        "",
        "",
        ""
    ],
    "supporting_findings": [
        "",
        ""
    ],
    "alternative_hypotheses": [
        {{
            "name": "",
            "reason": ""
        }}
    ],
    "recommended_investigations": [
        "",
        ""
    ],
    "unresolved_questions": [
        "",
        ""
    ],
    "agent_confidence": {{
        "AURA": 0,
        "NEXA": 0,
        "LYRA": 0,
        "ITHRA": 0
    }},
    "consensus_score": 0,
    "agreement_score": 0,
    "consensus_reached": false,
    "clinical_caution": ""
}}

RULES:

- confidence must be a number from 0 to 100.
- consensus_score must be a number from 0 to 100.
- agreement_score must be a number from 0 to 100.
- consensus_reached must be true or false.

- reasoning must explain WHY the primary clinical direction
  was selected.

- supporting_findings must contain findings directly supported
  by the case.

- alternative_hypotheses must contain plausible alternatives
  identified by the agents or debate.

- recommended_investigations must come from missing information
  or diagnostic workup discussed by the agents.

- unresolved_questions must preserve important uncertainty
  identified during the debate.

- agent_confidence must contain the confidence values for
  AURA, NEXA, LYRA and ITHRA based on their analyses/debate.

- consensus_score, agreement_score and consensus_reached should
  reflect the supplied consensus result.

- clinical_caution MUST explicitly state that this is an
  AI-assisted clinical reasoning output and NOT a definitive
  diagnosis.

Return ONLY JSON.
"""

    # ---------------------------------------------------------
    # CALL LLM
    # ---------------------------------------------------------

    response = generate_response(
        prompt,
        json_mode=True,
    )

    # ---------------------------------------------------------
    # CLEAN RESPONSE
    # ---------------------------------------------------------

    cleaned_response = _clean_json_response(response)

    # ---------------------------------------------------------
    # PARSE JSON
    # ---------------------------------------------------------

    try:
        return json.loads(cleaned_response)

    except json.JSONDecodeError as exc:
        raise RuntimeError(
            f"Final synthesis returned invalid JSON:\n{response}"
        ) from exc