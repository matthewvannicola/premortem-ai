"""
output/base.py

Defines the canonical rendering contract for PreMortem AI reports.

All output formats (Markdown, JSON, DOCX, PDF) MUST implement this interface.

Renderers:
- Accept a fully constructed PipelineResponse
- Apply a fixed, governed presentation structure
- Perform NO reasoning and NO data mutation
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Dict

from premortem_ai.models.pipeline_response import PipelineResponse


class OutputFormat(str, Enum):
    """
    Supported output formats.

    Used by:
    - API request validation
    - Renderer routing
    - UI format selection
    """

    JSON = "json"
    MARKDOWN = "markdown"
    DOCX = "docx"
    PDF = "pdf"


class BaseRenderer(ABC):
    """
    Abstract base class for all PreMortem output renderers.

    Renderers are PURE presentation layers.
    They must not:
    - modify data
    - infer new meaning
    - re-score risks
    """

    format: OutputFormat

    @abstractmethod
    def render(self, response: PipelineResponse) -> Any:
        """
        Render a PipelineResponse into a presentation artifact.

        Args:
            response: Fully validated PipelineResponse

        Returns:
            Rendered artifact (e.g., str, bytes, dict)
        """
        raise NotImplementedError

    def metadata(self) -> Dict[str, Any]:
        """
        Optional renderer metadata.

        Examples:
            - file_extension
            - mime_type
            - default_filename
        """
        return {}

