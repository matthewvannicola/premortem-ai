"""
file_io.py

Enterprise-safe file input/output utilities for PreMortem AI.

Goals:
    • Deterministic and secure filesystem operations
    • Safe JSON read/write handling
    • Atomic write guarantees (prevents partial files)
    • UTF-8 encoding normalization
    • CanonicalModel support for easy serialization
    • Predictable behavior across OS environments

This module is intentionally minimal yet robust, and suitable for:
    • Pipeline output persistence
    • Logging artifacts
    • CLI usage
    • Testing utilities
    • Local storage for debugging complex runs
"""

import json
import os
import tempfile
from typing import Any, Union

from premortem_ai.models.base_model import CanonicalModel


# ----------------------------------------------------------------------
# Directory utilities
# ----------------------------------------------------------------------
def ensure_dir(path: str) -> None:
    """Create a directory if it doesn't exist (idempotent)."""
    os.makedirs(path, exist_ok=True)


# ----------------------------------------------------------------------
# Text file read/write
# ----------------------------------------------------------------------
def write_text(path: str, content: str) -> None:
    """
    Safely write UTF-8 text content to a file.

    Uses atomic write:
        - write to temporary file
        - replace original file in a single operation
    """
    ensure_dir(os.path.dirname(path) or ".")

    with tempfile.NamedTemporaryFile("w", delete=False, encoding="utf-8") as tmp:
        tmp.write(content)
        tmp_path = tmp.name

    os.replace(tmp_path, path)


def read_text(path: str) -> str:
    """Read UTF-8 text from a file. Raises clear error if missing."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"File does not exist: {path}")

    with open(path, "r", encoding="utf-8") as f:
        return f.read()


# ----------------------------------------------------------------------
# JSON read/write helpers
# ----------------------------------------------------------------------
def write_json(path: str, data: Union[dict, list, CanonicalModel]) -> None:
    """
    Write JSON data safely using atomic write.

    Supports:
        - dict
        - list
        - CanonicalModel (serialized via model_dump)
    """
    if isinstance(data, CanonicalModel):
        data = data.model_dump()

    ensure_dir(os.path.dirname(path) or ".")

    with tempfile.NamedTemporaryFile("w", delete=False, encoding="utf-8") as tmp:
        json.dump(data, tmp, indent=2, ensure_ascii=False)
        tmp_path = tmp.name

    os.replace(tmp_path, path)


def read_json(path: str) -> Any:
    """Read JSON content with UTF-8 decoding."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"JSON file not found: {path}")

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


# ----------------------------------------------------------------------
# CanonicalModel-specific helpers
# ----------------------------------------------------------------------
def save_model(path: str, model: CanonicalModel) -> None:
    """
    Save any CanonicalModel to a file as JSON.
    The output is deterministic and ideal for debugging or caching.
    """
    write_json(path, model.model_dump())


def load_model(path: str, model_cls: type[CanonicalModel]) -> CanonicalModel:
    """
    Load JSON content into a CanonicalModel subclass.
    """
    data = read_json(path)
    return model_cls(**data)
