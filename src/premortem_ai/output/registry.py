"""
output/registry.py

Central registry for PreMortem AI output renderers.

This module is the ONLY place where output formats are mapped to renderers.
"""

from premortem_ai.output.base import OutputFormat
from premortem_ai.output.markdown import MarkdownRenderer
from premortem_ai.output.json_renderer import JSONRenderer


_RENDERERS = {
    OutputFormat.JSON: JSONRenderer(),
    OutputFormat.MARKDOWN: MarkdownRenderer(),
}


def get_renderer(output_format: OutputFormat):
    """
    Resolve the renderer for a given output format.

    Args:
        output_format: OutputFormat enum value

    Returns:
        An output renderer instance

    Raises:
        ValueError if the format is unsupported
    """
    try:
        return _RENDERERS[output_format]
    except KeyError as exc:
        raise ValueError(
            f"Unsupported output format: {output_format}"
        ) from exc
