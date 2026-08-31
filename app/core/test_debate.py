# app/test_debate.py

from app.agents.aura import analyze_case as analyze_aura
from app.agents.nexa import analyze_case as analyze_nexa
from app.agents.lyra import analyze_case as analyze_lyra
from app.agents.ithra import analyze_case as analyze_ithra

from app.core.debate import run_debate


# Same type of case we've been using to test the agents.
case = """
A 32-year-old woman presents with progressive fatigue, shortness of breath, and muscle weakness over several months. Her symptoms worsen after physical activity.

Laboratory investigations show elevated creatine kinase (CK)
and mild anemia.

There is no known history of trauma and no recent infection.
"""


print("\n========== RUNNING AGENT ANALYSES ==========\n")


print("Running AURA...")
aura_result = analyze_aura(case)
print("AURA complete.\n")


print("Running NEXA...")
nexa_result = analyze_nexa(case)
print("NEXA complete.\n")


print("Running LYRA...")
lyra_result = analyze_lyra(case)
print("LYRA complete.\n")


print("Running ITHRA...")
ithra_result = analyze_ithra(case)
print("ITHRA complete.\n")


# Put all four independent analyses together.
analyses = [
    aura_result,
    nexa_result,
    lyra_result,
    ithra_result
]


# Start the debate.
critiques = run_debate(analyses)


print("\n========== DEBATE RESULTS ==========\n")


for critique in critiques:

    print("=" * 60)
    print(f"Agent: {critique.target_agent}")
    print("=" * 60)

    print("\nCritique:")
    print(critique.critique)

    print("\nAgrees:")
    for item in critique.agrees:
        print(f"  + {item}")

    print("\nDisagreements:")
    for item in critique.disagreements:
        print(f"  - {item}")

    print("\nSupporting Evidence:")
    for item in critique.supporting_evidence:
        print(f"  + {item}")

    print("\nNew Insights:")
    for item in critique.new_insights:
        print(f"  * {item}")

    print("\nRevised Conclusion:")
    print(critique.revised_conclusion)

    print("\nConfidence:")
    print(critique.confidence)

    print()