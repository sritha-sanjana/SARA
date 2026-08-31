from app.agents.lyra import analyze_case

case = """
A 32-year-old woman presents with progressive fatigue, shortness of breath, and muscle weakness over several months. Symptoms worsen after physical activity. Laboratory tests show elevated creatine kinase and mild anemia. There is no known history of trauma or recent infection.
"""

result = analyze_case(case)

print("\n========== LYRA ANALYSIS RESULT ==========\n")

print("Agent:")
print(result.agent)

print("\nKey Findings:")
for item in result.key_findings:
    print("-", item)

print("\nPatterns:")
for item in result.patterns:
    print("-", item)

print("\nHypotheses:")
for hypothesis in result.hypotheses:
    print("\nName:")
    print(hypothesis.name)

    print("Likelihood:")
    print(hypothesis.likelihood)

    print("Supporting Evidence:")
    for item in hypothesis.supporting_evidence:
        print("  +", item)

    print("Contradicting Evidence:")
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

print("\nConfidence:")
print(result.confidence)