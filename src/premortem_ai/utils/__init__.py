"""
Utility package for PreMortem AI.

This module centralizes lightweight, reusable helpers that support the
pipeline, service layer, and API infrastructure. These utilities are intentionally
framework-agnostic and safe to import anywhere in the codebase.

Public Exports:
    - logger       : Shared application logger
    - Timer        : Execution time measurement helper
    - read_text_file, write_text_file : Safe UTF-8 file operations

Downstream modules should import from here for a stable, governed utility API:

    from premortem_ai.utils import logger, Timer
"""

from .logger import logger
from .timer import Timer
from .file_io import read_text_file, write_text_file

__all__ = [
    "logger",
    "Timer",
    "read_text_file",
    "write_text_file",
]
