"""
tracing.py

Lightweight tracing abstraction for PreMortem AI.

This module provides:
    - Span objects for timing and context propagation
    - A global tracer instance used throughout the system
    - Minimal overhead for local/dev environments
    - A clean upgrade path to full OpenTelemetry or Datadog APM

Design goals:
    - Zero external dependencies
    - Non-blocking instrumentation
    - Clear, consistent visibility into pipeline behavior
"""

import time
from contextlib import contextmanager
from typing import Optional, Dict, Any

from premortem_ai.utils.logger import logger


# ------------------------------------------------------------------------------
# Span Object
# ------------------------------------------------------------------------------

class Span:
    """
    Represents a single traced operation.

    Automatically records:
        - start and end timestamps
        - duration in ms
        - optional tags for debugging or observability

    Intended usage:
        with tracer.start_span("risk.discovery") as span:
            ...
            span.tag("n_risks", len(risks))
    """

    def __init__(self, name: str, tags: Optional[Dict[str, Any]] = None):
        self.name = name
        self.tags = tags or {}
        self.start_time = None
        self.end_time = None

    def __enter__(self):
        self.start_time = time.perf_counter()
        logger.info(f"[trace] start_span | {self.name} | tags={self.tags}")
        return self

    def __exit__(self, exc_type, exc, tb):
        self.end_time = time.perf_counter()
        duration_ms = (self.end_time - self.start_time) * 1000

        logger.info(
            f"[trace] end_span   | {self.name} | duration_ms={duration_ms:.2f} "
            f"| tags={self.tags}"
        )

        # Do not suppress exceptions
        return False

    def tag(self, key: str, value: Any):
        """Attach metadata to the span."""
        self.tags[key] = value


# ------------------------------------------------------------------------------
# Tracer
# ------------------------------------------------------------------------------

class Tracer:
    """
    Central tracing interface.

    Allows:
        - manual span creation
        - automatic function instrumentation (future)
        - propagation of trace context across pipeline stages

    This is intentionally simple but provides everything needed for
    pipeline-level observability.
    """

    def __init__(self, enabled: bool = True):
        self.enabled = enabled

    @contextmanager
    def start_span(self, name: str, tags: Optional[Dict[str, Any]] = None):
        """
        Context manager for tracing a named operation.

        Example:
            with tracer.start_span("scoring.compute", {"risk_count": len(risks)}):
                compute_scores()
        """
        if not self.enabled:
            yield None
            return

        span = Span(name=name, tags=tags)
        try:
            span.__enter__()
            yield span
        finally:
            span.__exit__(None, None, None)


# Global shared tracer instance
tracer = Tracer()
