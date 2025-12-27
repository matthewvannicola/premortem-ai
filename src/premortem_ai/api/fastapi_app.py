"""
fastapi_app.py

FastAPI application exposing the PreMortem AI system.
Acts strictly as the HTTP boundary.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, PlainTextResponse

import traceback

from premortem_ai.models.pipeline_request import PipelineRequest
from premortem_ai.models.pipeline_response import PipelineResponse
from premortem_ai.pipelines.run_pipeline import run_pipeline
from premortem_ai.output.base import OutputFormat
from premortem_ai.output.registry import get_renderer

from premortem_ai.exceptions import (
    ValidationError,
    CrossReferenceError,
    ModelInvocationError,
    ConfigurationError,
    PipelineExecutionError,
)

from premortem_ai.core.logger import info, error

# Intake router
from premortem_ai.api.routes.intake import router as intake_router


# ---------------------------------------------------------
# APP INITIALIZATION
# ---------------------------------------------------------

app = FastAPI(
    title="PreMortem AI",
    description="Automated project risk analysis & pre-mortem engine.",
    version="1.0.0",
)


# ---------------------------------------------------------
# CORS CONFIG (UI COMPATIBILITY)
# ---------------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # OK for local + MVP
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------
# ROUTER REGISTRATION
# ---------------------------------------------------------

app.include_router(intake_router)


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

@app.post("/pipeline/run", tags=["analysis"])
def run_pipeline_endpoint(request: PipelineRequest):
    """
    Execute the full PreMortem AI pipeline and render output
    in the requested format.
    """

    info("Received pipeline request")

    try:
        # 1. Execute pipeline
        context = run_pipeline(request)

        # 2. Build canonical response
        response = PipelineResponse.from_context(context)

        # 3. Select renderer
        renderer = get_renderer(request.output_format)

        # 4. Render output
        rendered = renderer.render(response)

        # 5. Return appropriate media type
        if request.output_format == OutputFormat.MARKDOWN:
            return PlainTextResponse(
                content=rendered,
                media_type="text/markdown",
            )

        # Default: JSON
        return JSONResponse(content=rendered)

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
        traceback.print_exc()
        error(f"Unhandled exception: {exc}")
        raise HTTPException(status_code=500, detail=str(exc))
