"""
file_io.py

Utility helpers for safe and predictable file operations within PreMortem AI.

This module centralizes:
    - UTF-8 safe reading
    - Basic write utilities (future)
    - Error-wrapped file access for clearer debugging
    - A thin abstraction layer for future remote file backends (S3, GCS, etc.)

By keeping file operations here, pipeline modules remain pure and testable.
"""

from pathlib import Path


def read_text_file(path: str | Path) -> str:
    """
    Read a UTF-8 text file safely.

    Args:
        path (str | Path): Path to the file.

    Returns:
        str: File contents as a UTF-8 decoded string.

    Raises:
        FileNotFoundError: If the file does not exist.
        RuntimeError: For any other unexpected read failure.
    """
    try:
        file_path = Path(path)
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        return file_path.read_text(encoding="utf-8")

    except FileNotFoundError:
        raise
    except Exception as exc:
        raise RuntimeError(f"Failed to read file '{path}': {exc}") from exc


def write_text_file(path: str | Path, content: str) -> None:
    """
    Write UTF-8 text to a file, creating parent directories if necessary.

    Args:
        path (str | Path): Destination path.
        content (str): Text content to write.

    Raises:
        RuntimeError: For unexpected write failures.
    """
    try:
        file_path = Path(path)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content, encoding="utf-8")
    except Exception as exc:
        raise RuntimeError(f"Failed to write file '{path}': {exc}") from exc
