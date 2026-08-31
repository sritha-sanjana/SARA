export interface Hypothesis {
  name: string;
  supporting_evidence: string[];
  contradicting_evidence: string[];
  likelihood: string;
}

export interface AgentAnalysis {
  agent: string;
  key_findings: string[];
  patterns: string[];
  hypotheses: Hypothesis[];
  missing_information: string[];
  anomalies: string[];
  analytical_summary: string;
  confidence: number;
}

export interface AgentCritique {
  critique: string;
  target_agent: string;
  agrees: string[];
  disagreements: string[];
  supporting_evidence: string[];
  new_insights: string[];
  revised_conclusion: string;
  confidence: number;
}

export interface ConsensusResult {
  round_number: number;
  consensus_score: number;
  confidence_score: number;
  agreement_score: number;
  consensus_reached: boolean;
  dominant_hypothesis: string | null;
  unresolved_disagreements: string[];
}

export interface AlternativeHypothesis {
  name: string;
  reason: string;
}

export interface FinalSynthesis {
  primary_clinical_direction: string;
  confidence: number;
  reasoning: string[];
  supporting_findings: string[];
  alternative_hypotheses: AlternativeHypothesis[];
  recommended_investigations: string[];
  unresolved_questions: string[];
  agent_confidence: Record<string, number>;
  consensus_score: number;
  agreement_score: number;
  consensus_reached: boolean;
  clinical_caution: string;
}

export interface SARAResponse {
  case_text: string;
  analyses: Record<string, AgentAnalysis>;
  debate: AgentCritique[];
  consensus: ConsensusResult;
  final_synthesis: FinalSynthesis;
}

export interface CaseRequest {
  case_text: string;
}
