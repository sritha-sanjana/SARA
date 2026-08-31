# app/core/debate.py

import json
import re
from typing import List, Dict

from app.core.schemas import AgentAnalysis, AgentCritique
from app.services.llm import generate_response


def _clean_json_response(response: str) -> str:
    """
    Remove markdown code fences and extract the JSON object.
    """

    response = response.strip()

    # Remove ```json ... ``` or ``` ... ```
    response = re.sub(
        r"^```(?:json)?\s*",
        "",
        response,
        flags=re.IGNORECASE
    )

    response = re.sub(
        r"\s*```$",
        "",
        response
    )

    # Find the first JSON object
    start = response.find("{")
    end = response.rfind("}")

    if start != -1 and end != -1 and end > start:
        response = response[start:end + 1]

    return response.strip()


def _build_debate_prompt(
    target_agent: AgentAnalysis,
    other_agents: List[AgentAnalysis]
) -> str:
    """
    Build the prompt for one agent to critique the other agents.
    """

    other_analyses = []

    for agent in other_agents:
        other_analyses.append(
            {
                "agent": agent.agent,
                "key_findings": agent.key_findings,
                "patterns": agent.patterns,
                "hypotheses": [
                    hypothesis.model_dump()
                    for hypothesis in agent.hypotheses
                ],
                "missing_information": agent.missing_information,
                "anomalies": agent.anomalies,
                "analytical_summary": agent.analytical_summary,
                "confidence": agent.confidence,
            }
        )

    target_data = {
        "agent": target_agent.agent,
        "key_findings": target_agent.key_findings,
        "patterns": target_agent.patterns,
        "hypotheses": [
            hypothesis.model_dump()
            for hypothesis in target_agent.hypotheses
        ],
        "missing_information": target_agent.missing_information,
        "anomalies": target_agent.anomalies,
        "analytical_summary": target_agent.analytical_summary,
        "confidence": target_agent.confidence,
    }

    return f"""
You are {target_agent.agent}, participating in SARA's multi-agent
medical reasoning debate.

You have already performed your independent analysis of the case.

Your analysis:
{json.dumps(target_data, indent=2)}

The other SARA agents produced these analyses:

{json.dumps(other_analyses, indent=2)}

Your task is to critically compare the other agents' reasoning with
your own analysis.

IMPORTANT:
- Do not simply agree with everyone.
- Identify genuine agreements and disagreements.
- Check whether hypotheses are actually supported by the available evidence.
- Identify important evidence that another agent may have overlooked.
- Identify reasoning that may be too strong or insufficiently supported.
- Do not invent patient information.
- Do not provide a definitive medical diagnosis.
- This is an internal reasoning debate for the SARA system.

Return ONLY valid JSON.

Use EXACTLY this structure:

{{
    "critique": "Overall critique of the other agents' reasoning.",
    "target_agent": "{target_agent.agent}",
    "agrees": [
        "Specific point the agent agrees with"
    ],
    "disagreements": [
        "Specific point where the agent disagrees"
    ],
    "supporting_evidence": [
        "Evidence from the case supporting the reasoning"
    ],
    "new_insights": [
        "New reasoning or connection identified during the debate"
    ],
    "revised_conclusion": "How the agent's conclusion changes or remains the same after considering the other agents.",
    "confidence": 0
}}

The confidence value must be a number from 0 to 100.

Again: return ONLY JSON.
"""


def _parse_critique(response: str, target_agent: str) -> AgentCritique:
    """
    Parse Gemini's response into an AgentCritique object.
    """

    cleaned_response = _clean_json_response(response)

    try:
        data = json.loads(cleaned_response)
    except json.JSONDecodeError as exc:
        raise RuntimeError(
            f"{target_agent} returned invalid debate JSON:\n{response}"
        ) from exc

    # Make sure the target agent is always correct.
    data["target_agent"] = target_agent

    try:
        return AgentCritique(**data)
    except Exception as exc:
        raise RuntimeError(
            f"{target_agent} debate response failed schema validation:\n"
            f"{json.dumps(data, indent=2)}"
        ) from exc


def run_debate(analyses: List[AgentAnalysis]) -> List[AgentCritique]:
    """
    Run the SARA multi-agent debate.

    Each agent receives the analyses of the other agents and produces
    one critique.

    This results in:
        AURA  -> critique
        NEXA  -> critique
        LYRA  -> critique
        ITHRA -> critique

    Returns:
        List[AgentCritique]
    """

    if not analyses:
        raise ValueError("No agent analyses were provided for debate.")

    if len(analyses) < 2:
        raise ValueError(
            "At least two agent analyses are required for debate."
        )

    critiques: List[AgentCritique] = []

    print("\n========== SARA MULTI-AGENT DEBATE ==========\n")

    for target_agent in analyses:

        print(f"Running debate for {target_agent.agent}...")

        other_agents = [
            agent
            for agent in analyses
            if agent.agent != target_agent.agent
        ]

        prompt = _build_debate_prompt(
            target_agent=target_agent,
            other_agents=other_agents
        )

        response = generate_response(prompt)

        critique = _parse_critique(
            response=response,
            target_agent=target_agent.agent
        )

        critiques.append(critique)

        print(f"{target_agent.agent} debate complete.")

    return critiques


def debate_agents(analyses: List[AgentAnalysis]) -> List[AgentCritique]:
    """
    Alias for run_debate().

    This gives the orchestrator a more descriptive function name.
    """

    return run_debate(analyses)