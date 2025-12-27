"""
premortem_ai.output

Rendering layer for PreMortem AI reports.

This package is responsible for transforming a fully validated
PipelineResponse into presentation formats such as:
- JSON (canonical record)
- Markdown (Enterprise-grade report)
- PDF / DOCX (derived formats)

Renderers must:
- Accept PipelineResponse only
- Perform NO reasoning or data mutation
"""

from premortem_ai.output.base import BaseRenderer, OutputFormat
from premortem_ai.output.json_renderer import JSONRenderer
from premortem_ai.output.markdown import MarkdownRenderer

__all__ = [
    "BaseRenderer",
    "OutputFormat",
    "JSONRenderer",
    "MarkdownRenderer",
]

