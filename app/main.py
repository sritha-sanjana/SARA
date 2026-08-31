from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from app.orchestrator import orchestrate
from app.core.schemas import SARAResponse


app = FastAPI(title="SARA API", description="Synchronized Agentic Reasoning & Assistance")

# Add CORS middleware to allow requests from deployed frontend domains
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",      # Local Vite dev server
        "http://127.0.0.1:5173",      # Local development
        "https://sara-9u4x.onrender.com",  # Backend (for health checks)
        "https://sara-biomedical.vercel.app",
        # Add frontend deployment domains here when known
        # e.g., "https://sara-frontend.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
