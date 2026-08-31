# app/core/test_final_synthesis.py

from app.agents.aura import analyze_case as analyze_aura
from app.agents.nexa import analyze_case as analyze_nexa
from app.agents.lyra import analyze_case as analyze_lyra
from app.agents.ithra import analyze_case as analyze_ithra

from app.core.debate import run_debate
from app.core.consensus import build_consensus
from app.core.final_synthesis import synthesize_final_result


case = """
A 32-year-old woman presents with progressive fatigue,
shortness of breath, and muscle weakness over several months.
Symptoms worsen after physical activity.

Laboratory testing shows elevated creatine kinase (CK)
and mild anemia.

There is no known history of trauma or recent infection.
"""


# ============================================================
# STEP 1 — RUN ALL FOUR AGENTS
# ============================================================

print("\n========== RUNNING AGENT ANALYSES ==========\n")

agents = {}

print("Running AURA...")
agents["AURA"] = analyze_aura(case)
print("AURA complete.")

print("\nRunning NEXA...")
agents["NEXA"] = analyze_nexa(case)
print("NEXA complete.")

print("\nRunning LYRA...")
agents["LYRA"] = analyze_lyra(case)
print("LYRA complete.")

print("\nRunning ITHRA...")
agents["ITHRA"] = analyze_ithra(case)
print("ITHRA complete.")


# ============================================================
# STEP 2 — RUN MULTI-AGENT DEBATE
# ============================================================

print("\n========== RUNNING DEBATE ==========\n")

debates = run_debate(
    analyses=list(agents.values())
)


# ============================================================
# STEP 3 — BUILD CONSENSUS
# ============================================================

print("\n========== BUILDING CONSENSUS ==========\n")

consensus = build_consensus(
    debate_results=debates,
    round_number=1
)


# ============================================================
# STEP 4 — DISPLAY CONSENSUS
# ============================================================

print("\n========== SARA CONSENSUS RESULT ==========\n")

print("Round Number:")
print(consensus.round_number)

print("\nConsensus Score:")
print(consensus.consensus_score)

print("\nAgreement Score:")
print(consensus.agreement_score)

print("\nConfidence Score:")
print(consensus.confidence_score)

print("\nConsensus Reached:")
print(consensus.consensus_reached)

print("\nDominant Hypothesis:")
print(consensus.dominant_hypothesis)

print("\nUnresolved Disagreements:")

if consensus.unresolved_disagreements:
    for item in consensus.unresolved_disagreements:
        print(f"  - {item}")
else:
    print("  None")


# ============================================================
# STEP 5 — BUILD FINAL SYNTHESIS
# ============================================================

print("\n========== BUILDING FINAL SYNTHESIS ==========\n")

final_result = synthesize_final_result(
    analyses=agents,
    debates=debates,
    consensus=consensus
)


# ============================================================
# STEP 6 — DISPLAY FINAL SARA SYNTHESIS
# ============================================================

print("\n========== SARA FINAL SYNTHESIS ==========\n")

print("\nPrimary Clinical Direction:")
print(final_result["primary_clinical_direction"])

print("\nConfidence:")
print(final_result["confidence"])


print("\nReasoning:")

for item in final_result["reasoning"]:
    print(f"  + {item}")


print("\nSupporting Findings:")

for item in final_result["supporting_findings"]:
    print(f"  + {item}")


print("\nAlternative Hypotheses:")

for hypothesis in final_result["alternative_hypotheses"]:
    print(f"\n  Name: {hypothesis['name']}")
    print(f"  Reason: {hypothesis['reason']}")


print("\nRecommended Investigations:")

for item in final_result["recommended_investigations"]:
    print(f"  - {item}")


print("\nUnresolved Questions:")

for item in final_result["unresolved_questions"]:
    print(f"  - {item}")


print("\nAgent Confidence:")

for agent, confidence in final_result["agent_confidence"].items():
    print(f"  {agent}: {confidence}")


print("\nConsensus Score:")
print(final_result["consensus_score"])

print("\nAgreement Score:")
print(final_result["agreement_score"])

print("\nConsensus Reached:")
print(final_result["consensus_reached"])


print("\nClinical Caution:")
print(final_result["clinical_caution"])


print("\n========== FINAL SYNTHESIS COMPLETE ==========\n")