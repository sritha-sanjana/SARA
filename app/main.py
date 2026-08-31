from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from app.orchestrator import orchestrate
from app.core.schemas import SARAResponse


app = FastAPI(title="SARA API", description="Synchronized Agentic Reasoning & Assistance")


class CaseRequest(BaseModel):
    case_text: str = Field(..., description="Medical case text to analyze", min_length=1)


@app.post("/analyze", response_model=SARAResponse)
def analyze_case(request: CaseRequest) -> SARAResponse:
    """
    Analyze a biomedical case using the complete SARA pipeline.

    Returns:
    - Analyses from all four agents (AURA, NEXA, LYRA, ITHRA)
    - Multi-agent debate results
    - Consensus engine output
    - Final synthesis with clinical reasoning
    """
    try:
        result = orchestrate(request.case_text)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")
