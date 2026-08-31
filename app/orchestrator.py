# SARA Orchestrator#
#
# Coordinates the Four SARA reasoning agents:
# AURA, NEXA, LYRA, and ITHRA.

from typing import Dict

from app.agents.aura import analyze_case as analyze_aura
from app.agents.nexa import analyze_case as analyze_nexa
from app.agents.lyra import analyze_case as analyze_lyra
from app.agents.ithra import analyze_case as analyze_ithra

from app.core.schemas import AgentAnalysis
from app.core.debate import run_debate
from app.core.consensus import build_consensus
from app.core.final_synthesis import synthesize_final_result

def run_agents(case_text: str) -> Dict[str, AgentAnalysis]:
    """
    Run all four SARA agents on the same biomedical case.

    Returns:
        A dictionary containing the analysis from each agent.
    """

    if not case_text or not case_text.strip():
        raise ValueError("Case text cannot be empty.")
    
    results = {}

    print("\n========== SARA AGENT ANALYSIS ==========\n")

    print("Running AURA...")
    results["AURA"] = analyze_aura(case_text)
    print("AURA analysis complete.\n")

    print("Running NEXA...")
    results["NEXA"] = analyze_nexa(case_text)
    print("NEXA analysis complete.\n")

    print("Running LYRA...")
    results["LYRA"] = analyze_lyra(case_text)
    print("LYRA analysis complete.\n")

    print("Running ITHRA...")
    results["ITHRA"] = analyze_ithra(case_text)
    print("ITHRA analysis complete.\n")

    return results

def orchestrate(case_text: str) -> dict:
    """
    Main orchestration entry point.

    Complete pipeline:

    Case
      ↓
    AURA, NEXA, LYRA, ITHRA (parallel agents)
      ↓
    Multi-agent Debate
      ↓
    Consensus Engine
      ↓
    Final Synthesis
      ↓
    Structured result
    """

    # Stage 1: Run all four agents
    analyses = run_agents(case_text)

    # Stage 2: Run multi-agent debate
    debates = run_debate(analyses=list(analyses.values()))

    # Stage 3: Build consensus
    consensus = build_consensus(debate_results=debates, round_number=1)

    # Stage 4: Synthesize final result
    final_result = synthesize_final_result(
        analyses=analyses,
        debates=debates,
        consensus=consensus
    )

    return {
        "case_text": case_text,
        "analyses": {name: analysis.model_dump() for name, analysis in analyses.items()},
        "debate": [critique.model_dump() for critique in debates],
        "consensus": consensus.model_dump(),
        "final_synthesis": final_result
    }