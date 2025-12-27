"""
Public API surface for the PreMortem AI web layer.
Currently exposes only the FastAPI app instance.
"""

from .fastapi_app import app

__all__ = ["app"]
