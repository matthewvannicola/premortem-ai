"""
fastapi_app.py

Primary FastAPI application for exposing the PreMortem AI analysis pipeline
as an HTTP service. This module defines:

    - POST /analyze     : Runs a full PreMortem AI analysis
    - Health checks     : Lightweight readiness/liveness endpoints

The API intentionally surfaces only the stable input/output contracts defined
in:
    - PipelineRequest
    - PipelineResponse

All business logic is delegated to AnalysisService and the underlying
PipelineOrchestrator.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from premortem_ai.analysis_service import AnalysisService
from premortem_ai.models import PipelineRequest, PipelineResponse


# ---------------------------------------------------------------------------
# FastAPI Application Setup
# ---------------------------------------------------------------------------

app = FastAPI(
    title="PreMortem AI – Analysis API",
    version="1.0.0",
    description="Run automated project risk analysis using PreMortem AI.",
)

# Optional: allow cross-origin access (useful for dashboards or JS clients)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],    # tighten in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the service layer
service = AnalysisService()


# ---------------------------------------------------------------------------
# Health Endpoints
# ---------------------------------------------------------------------------

@app.get("/health", tags=["system"])
def health_check():
    return {"status": "ok"}


@app.get("/ready", tags=["system"])
def readiness_check():
    return {"ready": True}


# ---------------------------------------------------------------------------
# Main Analysis Endpoint
# ---------------------------------------------------------------------------

@app.post(
    "/analyze",
    response_model=PipelineResponse,
    tags=["analysis"],
    summary="Run a full PreMortem AI analysis",
)
def analyze(request: PipelineRequest):
    """
    Execute a complete PreMortem AI pipeline run.

    Validates the request using canonical models, invokes AnalysisService,
    and returns a fully validated PipelineResponse.
    """
    try:
        response = service.run_analysis(request.model_dump())
        return response
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


# ---------------------------------------------------------------------------
# Root Endpoint
# ---------------------------------------------------------------------------

@app.get("/", tags=["system"])
def root():
    return {
        "message": "PreMortem AI Analysis API",
        "endpoints": {
            "POST /analyze": "Submit project description for full risk analysis",
            "GET /health": "Basic system health",
            "GET /ready": "Readiness probe",
        },
    }
