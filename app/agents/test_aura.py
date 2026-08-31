from app.agents.aura import analyze_case

case = """
A 32-year-old woman presents with progressive fatigue, shortness of breath, and muscle weakness over several months. Symptoms worsen after physical activity. Laboratory tests show elevated creatine kinase and mild anemia. There is no known history of trauma or recent infection.
"""

result = analyze_case(case)

print("\n========== AURA ANALYSIS RESULT ==========\n")

print("Agent:", result.agent)

print("\nKey Findings:")
for item in result.key_findings:
    print("-", item)

print("\nPatterns:")
for item in result.patterns:
    print("-", item)

print("\nHypotheses:")
for hypothesis in result.hypotheses:
    print("\n", hypothesis.name)
    print("Likelihood:", hypothesis.likelihood)

    print("Supporting:")
    for item in hypothesis.supporting_evidence:
        print("  +", item)

    print("Contradicting:")
    for item in hypothesis.contradicting_evidence:
        print("  -", item)

print("\nMissing Information:")
for item in result.missing_information:
    print("-", item)

print("\nAnomalies:")
for item in result.anomalies:
    print("-", item)

print("\nAnalytical Summary:")
print(result.analytical_summary)

print("\nConfidence:", result.confidence)