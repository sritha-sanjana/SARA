# app/core/test_consensus.py

from app.agents.aura import analyze_case as analyze_aura
from app.agents.nexa import analyze_case as analyze_nexa
from app.agents.lyra import analyze_case as analyze_lyra
from app.agents.ithra import analyze_case as analyze_ithra

from app.core.debate import run_debate
from app.core.consensus import build_consensus


case = """
A 32-year-old woman presents with progressive fatigue,
shortness of breath, and muscle weakness over several months.
Symptoms worsen after physical activity. Laboratory tests show
elevated creatine kinase and mild anemia. There is no known
history of trauma or recent infection.
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

debate_results = run_debate(
    analyses=list(agents.values())
)


# ============================================================
# STEP 3 — DISPLAY DEBATE RESULTS
# ============================================================

print("\n========== DEBATE RESULTS ==========\n")

for result in debate_results:

    print("=" * 60)
    print(f"Agent: {result.target_agent}")
    print("=" * 60)

    print("\nCritique:")
    print(result.critique)

    print("\nAgrees:")
    for item in result.agrees:
        print(f"  + {item}")

    print("\nDisagreements:")
    for item in result.disagreements:
        print(f"  - {item}")

    print("\nNew Insights:")
    for item in result.new_insights:
        print(f"  * {item}")

    print("\nRevised Conclusion:")
    print(result.revised_conclusion)

    print(f"\nConfidence: {result.confidence}")


# ============================================================
# STEP 4 — BUILD CONSENSUS
# ============================================================

print("\n========== BUILDING CONSENSUS ==========\n")

consensus = build_consensus(
    debate_results=debate_results,
    round_number=1,
)


# ============================================================
# STEP 5 — DISPLAY FINAL CONSENSUS
# ============================================================

print("\n========== SARA CONSENSUS RESULT ==========\n")

print(f"Round Number:")
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


print("\n========== SARA CONSENSUS COMPLETE ==========\n")