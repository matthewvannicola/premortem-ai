"""
output/json_renderer.py

Canonical JSON renderer for PreMortem AI.

This renderer produces the authoritative machine-readable output
for all pipeline executions.

All other formats (Markdown, DOCX, PDF) must be derivable from this
JSON representation.
"""

from __future__ import annotations

import json
from typing import Any, Dict

from premortem_ai.models.pipeline_response import PipelineResponse
from premortem_ai.output.base import BaseRenderer, OutputFormat


class JSONRenderer(BaseRenderer):
    """
    Renders a PipelineResponse into canonical JSON.

    This renderer:
    - Performs no formatting or interpretation
    - Preserves full structural fidelity
    - Produces deterministic, diffable output
    """

    format = OutputFormat.JSON

    def render(self, response: PipelineResponse) -> Dict[str, Any]:
        """
        Render the PipelineResponse into a JSON-serializable dict.

        Args:
            response: Fully validated PipelineResponse

        Returns:
            Dictionary suitable for JSON serialization
        """
        return response.model_dump(mode="json")

    def metadata(self) -> Dict[str, Any]:
        """
        Metadata describing the JSON output format.
        """
        return {
            "file_extension": ".json",
            "mime_type": "application/json",
            "default_filename": "premortem_report.json",
        }

