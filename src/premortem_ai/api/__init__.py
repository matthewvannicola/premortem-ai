"""
API package initializer for the PreMortem AI system.

This package provides:
    - Public API-facing modules (REST handlers, routers, controllers)
    - Integration points for HTTP frameworks (FastAPI, Flask, etc.)
    - A stable import boundary for SDK consumers

Example usage:

    from premortem_ai.api import router
    app.include_router(router)

or:

    from premortem_ai.api import AnalysisAPI

This file intentionally re-exports only the public API surface so internal
structure can evolve without breaking external consumers.
"""

# If you eventually add a FastAPI router:
# from .router import router

# If you add an API wrapper around the service layer:
# from .analysis_api import AnalysisAPI

# Expose exports here when those modules exist.
__all__ = [
    # "router",
    # "AnalysisAPI",
]
