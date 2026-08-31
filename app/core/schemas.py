# Data Schemas and Models
from typing import Dict, List
from pydantic import BaseModel, Field

class Hypothesis(BaseModel):
    name: str
    supporting_evidence: List[str] = Field(default_factory=list)
    contradicting_evidence: List[str] = Field(default_factory=list)
    likelihood: str

class AgentAnalysis(BaseModel):
    agent: str
    key_findings: List[str] = Field(default_factory=list)
    patterns: List[str] = Field(default_factory=list)
    hypotheses: List[Hypothesis] = Field(default_factory=list)
    missing_information: List[str] = Field(default_factory=list)
    anomalies: List[str] = Field(default_factory=list)
    analytical_summary: str
    confidence: float = Field(default=0,ge=0, le=100)

class AgentCritique(BaseModel):
    critique: str
    target_agent: str
    agrees: List[str] = Field(default_factory=list)
    disagreements: List[str] = Field(default_factory=list)
    supporting_evidence: List[str] = Field(default_factory=list)
    new_insights: List[str] = Field(default_factory=list)
    revised_conclusion: str
    confidence: float = Field(ge=0, le=100)

class ConsensusResult(BaseModel):
    round_number: int
    consensus_score: float = Field(ge=0, le=100)
    confidence_score: float = Field(ge=0, le=100)
    agreement_score: float = Field(ge=0, le=100)
    consensus_reached: bool
    dominant_hypothesis: str | None = None
    unresolved_disagreements: List[str] = Field(default_factory=list)

class AlternativeHypothesis(BaseModel):
    name: str
    reason: str

class FinalSynthesis(BaseModel):
    primary_clinical_direction: str
    confidence: float = Field(ge=0, le=100)
    reasoning: List[str]
    supporting_findings: List[str]
    alternative_hypotheses: List[AlternativeHypothesis]
    recommended_investigations: List[str]
    unresolved_questions: List[str]
    agent_confidence: Dict[str, float]
    consensus_score: float = Field(ge=0, le=100)
    agreement_score: float = Field(ge=0, le=100)
    consensus_reached: bool
    clinical_caution: str

class SARAResponse(BaseModel):
    case_text: str
    analyses: Dict[str, AgentAnalysis]
    debate: List[AgentCritique]
    consensus: ConsensusResult
    final_synthesis: FinalSynthesis