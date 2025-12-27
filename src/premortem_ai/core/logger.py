"""
logger.py

Enterprise-grade structured logging utility for PreMortem AI.

Goals:
    • Provide consistent logging across all services and modules
    • JSON-safe logs for ingestion by observability systems
    • Optional trace_id injection (from Metadata)
    • Fully compatible with local development, serverless, and containers
    • Minimal dependencies, high portability

This logger intentionally avoids heavy frameworks and sticks to the
Python logging module wrapped with structured helpers.
"""

import json
import logging
import sys
from typing import Any, Dict, Optional


# ----------------------------------------------------------------------
# Logger Configuration
# ----------------------------------------------------------------------

def _configure_root_logger() -> logging.Logger:
    """
    Configure the root logger if not already configured.
    Ensures idempotency and prevents duplicated handlers.
    """
    logger = logging.getLogger("premortem")
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(StructuredLogFormatter())
        logger.addHandler(handler)

    return logger


class StructuredLogFormatter(logging.Formatter):
    """
    Format logs as JSON objects for clean ingestion by:
        - cloud logging systems
        - ELK / OpenSearch
        - Datadog / Honeycomb
        - container logs
        - serverless logs

    Example output:
        {"level": "INFO", "message": "...", "trace_id": "1234", ...}
    """

    def format(self, record: logging.LogRecord) -> str:
        log = {
            "level": record.levelname,
            "message": record.getMessage(),
            "logger": record.name,
            "timestamp": self.formatTime(record, datefmt="%Y-%m-%dT%H:%M:%SZ"),
        }

        # Include structured extra fields
        if hasattr(record, "extra") and isinstance(record.extra, dict):
            log.update(record.extra)

        return json.dumps(log, ensure_ascii=False)


# Initialize the root logger
_root_logger = _configure_root_logger()


# ----------------------------------------------------------------------
# Public Logging Helpers
# ----------------------------------------------------------------------

def info(message: str, *, trace_id: Optional[str] = None, **kwargs):
    """Log an INFO-level message with optional structured metadata."""
    _root_logger.info(message, extra={"extra": _attach_trace_id(trace_id, kwargs)})


def warning(message: str, *, trace_id: Optional[str] = None, **kwargs):
    """Log a WARNING-level message with optional structured metadata."""
    _root_logger.warning(message, extra={"extra": _attach_trace_id(trace_id, kwargs)})


def error(message: str, *, trace_id: Optional[str] = None, **kwargs):
    """Log an ERROR-level message with optional structured metadata."""
    _root_logger.error(message, extra={"extra": _attach_trace_id(trace_id, kwargs)})


def debug(message: str, *, trace_id: Optional[str] = None, **kwargs):
    """Log a DEBUG-level message with optional structured metadata."""
    _root_logger.debug(message, extra={"extra": _attach_trace_id(trace_id, kwargs)})


# ----------------------------------------------------------------------
# Internal Utility
# ----------------------------------------------------------------------

def _attach_trace_id(trace_id: Optional[str], data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Attach a trace_id to structured logs when available.
    This integrates directly with Metadata.trace_id.
    """
    if trace_id:
        data["trace_id"] = trace_id
    return data
