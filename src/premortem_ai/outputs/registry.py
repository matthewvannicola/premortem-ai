"""
output/registry.py

Central registry for PreMortem AI output renderers.

This module is the ONLY place where output formats are mapped to renderers.
"""

from typing import Literal

from premortem_ai.output.markdown import MarkdownRenderer
from premortem_ai.output.json_renderer import JSONRenderer

OutputFormat = Literal["json", "markdown"]

_RENDERERS = {
    "json": JSONRenderer(),
    "markdown": MarkdownRenderer(),
}


def get_renderer(format: OutputFormat):
    """
    Resolve the renderer for a given output format.
    """
    try:
        return _RENDERERS[format]
    except KeyError as exc:
        raise ValueError(f"Unsupported output format: {format}") from exc
