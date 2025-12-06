"""
FastAPI application exposing the PreMortem AI pipeline.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from premortem_ai.models.pipeline_request import PipelineRequest
from premortem_ai.models.pipeline_response import PipelineResponse
from premortem_ai.pipelines.run_pipeline import run_pipeline
from premortem_ai.exceptions import (
    ValidationError,
    CrossReferenceError,
    ModelInvocationError,
    ConfigurationError,
    PipelineExecutionError,
)
from premortem_ai.core.logger import info, error


app = FastAPI(
    title="PreMortem AI",
    description="Automated project risk analysis & pre-mortem engine.",
    version="1.0.0",
)


# ---------------------------------------------------------
# CORS CONFIG
# ---------------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update later for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------
# HEALTH ENDPOINTS
# ---------------------------------------------------------

@app.get("/health", tags=["system"])
def health_check():
    return {"status": "ok"}


@app.get("/", tags=["system"])
def root():
    return {
        "service": "PreMortem AI",
        "version": "1.0.0",
        "status": "running",
    }


# ---------------------------------------------------------
# PIPELINE EXECUTION ENDPOINT
# ---------------------------------------------------------

@app.post("/pipeline/run", response_model=PipelineResponse, tags=["analysis"])
def run_pipeline_endpoint(request: PipelineRequest):
    """
    Execute the full PreMortem AI pipeline.
    """

    info("Received pipeline request")

    try:
        # The pipeline returns a PipelineContext
        context = run_pipeline(request)

        # Convert context → PipelineResponse (FINAL FIX)
        response = PipelineResponse.from_context(context)

        return response

    except ValidationError as exc:
        error(f"Validation error: {exc}")
        raise HTTPException(status_code=400, detail=str(exc))

    except CrossReferenceError as exc:
        error(f"Cross-reference error: {exc}")
        raise HTTPException(status_code=422, detail=str(exc))

    except ModelInvocationError as exc:
        error(f"LLM model invocation error: {exc}")
        raise HTTPException(status_code=500, detail=str(exc))

    except ConfigurationError as exc:
        error(f"Configuration error: {exc}")
        raise HTTPException(status_code=500, detail=str(exc))

    except PipelineExecutionError as exc:
        error(f"Pipeline execution failed: {exc}")
        raise HTTPException(status_code=500, detail=str(exc))

    except Exception as exc:
        error(f"Unhandled exception: {exc}")
        raise HTTPException(status_code=500, detail="Internal server error")
