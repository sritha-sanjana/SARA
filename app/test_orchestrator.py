from app.orchestrator import orchestrate

case = """
A 32-year-old woman presents with progressive fatigue, shortness of breath, and muscle weakness over several months. Symptoms worsen after physical activity.

Laboratory investigations show elevated creatine kinase (CK) and mild anemia.

There is no known history of trauma or recent infection.
"""

result = orchestrate(case)

print("\n========== ORCHESTRATOR ANALYSIS RESULT ==========\n")

print("Case Text:")
print(result["case_text"][:100] + "...\n")

print("Agents Analyzed:", ", ".join(result["analyses"].keys()))
print("Debate Rounds:", len(result["debate"]))
print("Consensus Score:", result["consensus"]["consensus_score"])
print("Final Synthesis Confidence:", result["final_synthesis"]["confidence"])

print("\nPrimary Clinical Direction:")
print(result["final_synthesis"]["primary_clinical_direction"])

print("\nFinal Synthesis Reasoning:")
for reason in result["final_synthesis"]["reasoning"]:
    print(f"  - {reason}")