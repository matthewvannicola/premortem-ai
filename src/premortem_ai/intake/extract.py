"""
extract.py

Deterministic document text extraction for the PreMortem intake layer.

Responsibilities:
- Accept supported file types
- Extract raw text only
- Perform NO interpretation or normalization
- Return plain text with minimal metadata

This module must remain upstream of all reasoning logic.
"""

from typing import List, Dict
from pathlib import Path
import json

from premortem_ai.exceptions import PremortemException

# Optional dependencies (imported lazily)
# - pdfplumber for PDFs
# - python-docx for DOCX


class DocumentExtractionError(PremortemException):
    """Raised when document extraction fails."""


SUPPORTED_EXTENSIONS = {"pdf", "docx", "md", "txt", "json"}


def extract_documents(file_paths: List[Path]) -> List[Dict[str, str]]:
    """
    Extract raw text from supported document types.

    Args:
        file_paths: List of file paths to extract

    Returns:
        List of dicts with keys:
            - filename
            - file_type
            - text

    Raises:
        DocumentExtractionError if any file cannot be processed
    """
    extracted: List[Dict[str, str]] = []

    for path in file_paths:
        if not path.exists():
            raise DocumentExtractionError(f"File does not exist: {path}")

        ext = path.suffix.lower().lstrip(".")

        if ext not in SUPPORTED_EXTENSIONS:
            raise DocumentExtractionError(
                f"Unsupported file type: .{ext} ({path.name})"
            )

        try:
            if ext == "pdf":
                text = _extract_pdf(path)
            elif ext == "docx":
                text = _extract_docx(path)
            elif ext in {"md", "txt"}:
                text = _extract_text(path)
            elif ext == "json":
                text = _extract_json(path)
            else:
                # This should never happen due to SUPPORTED_EXTENSIONS check
                raise DocumentExtractionError(f"Unhandled file type: .{ext}")

            extracted.append(
                {
                    "filename": path.name,
                    "file_type": ext,
                    "text": text,
                }
            )

        except Exception as exc:
            raise DocumentExtractionError(
                f"Failed to extract {path.name}: {exc}"
            ) from exc

    return extracted


def _extract_pdf(path: Path) -> str:
    import pdfplumber

    text_chunks = []

    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text_chunks.append(page_text)

    return "\n".join(text_chunks)


def _extract_docx(path: Path) -> str:
    from docx import Document

    doc = Document(path)
    paragraphs = [p.text for p in doc.paragraphs if p.text]

    return "\n".join(paragraphs)


def _extract_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def _extract_json(path: Path) -> str:
    """
    Load JSON and return a pretty-printed string representation.

    This does NOT validate or interpret the JSON structure.
    """
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    return json.dumps(data, indent=2, sort_keys=True)
