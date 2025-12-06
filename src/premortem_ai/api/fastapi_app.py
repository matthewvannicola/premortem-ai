"""
fastapi_app.py

FastAPI application exposing the PreMortem AI pipeline.
Uses the new functional pipeline entrypoint:
    run_pipeline(PipelineRequest)

This layer is intentionally thin — all logic lives in domains + pipeline.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from premortem_ai.models import PipelineRequest, PipelineResponse
from premortem_ai.pipelines import run_pipeline
from premortem_ai.exceptions import (
    ValidationError,
    CrossReferenceError,
    ModelInvocationError,
    ConfigurationError,
)
from premortem_ai.core.logger import error, info


# ---------------------------------------------------------------------------
# FastAPI Setup
# ---------------------------------------------------------------------------

app = FastAPI(
    title="PreMortem AI – Pipeline API",
    version="2.0.0",
    description="Automated project risk analysis powered by the PreMortem AI pipeline.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# Health Endpoints
# ---------------------------------------------------------------------------

@app.get("/health", tags=["system"])
def health():
    return {"status": "ok"}


@app.get("/ready", tags=["system"])
def ready():
    return {"ready": True}


# ---------------------------------------------------------------------------
# Pipeline Execution Endpoint
# ---------------------------------------------------------------------------

@app.post(
    "/pipeline/run",
    response_model=PipelineResponse,
    tags=["analysis"],
    summary="Run the full PreMortem AI pipeline",
)
def pipeline_run(request: PipelineRequest):
    """
    Execute the complete risk analysis pipeline.
    """
    try:
        info("API: Received pipeline request.")
        response = run_pipeline(request)
        return response

    # ---------------- Core validation issues -----------------
    except ValidationError as exc:
        error(f"Validation error: {exc}")
        raise HTTPException(status_code=422, detail=str(exc))

    # ---------------- Cross-reference / schema mismatch -------
    except CrossReferenceError as exc:
        error(f"Cross-reference error: {exc}")
        raise HTTPException(status_code=400, detail=str(exc))

    # ---------------- Model or LLM failure --------------------
    except ModelInvocationError as exc:
        error(f"Model invocation error: {exc}")
        raise HTTPException(status_code=500, detail=str(exc))

    # ---------------- Configuration issues --------------------
    except ConfigurationError as exc:
        error(f"Configuration error: {exc}")
        raise HTTPException(status_code=500, detail=str(exc))

    # ---------------- Unexpected fallback ---------------------
    except Exception as exc:
        error(f"Unhandled API error: {exc}")
        raise HTTPException(status_code=500, detail=f"Unexpected error: {exc}")


# ---------------------------------------------------------------------------
# Root Endpoint
# ---------------------------------------------------------------------------

@app.get("/", tags=["system"])
def root():
    return {
        "message": "PreMortem AI Pipeline API",
        "endpoints": {
            "POST /pipeline/run": "Execute a full PreMortem AI analysis",
            "GET /health": "Basic health check",
            "GET /ready": "Readiness probe",
        },
    }
