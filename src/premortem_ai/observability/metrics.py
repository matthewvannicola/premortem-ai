"""
metrics.py

Lightweight metrics interface for PreMortem AI.

This module provides a minimal but enterprise-ready metrics abstraction used
throughout the system. It intentionally avoids hard dependencies on Prometheus,
StatsD, Datadog, or OpenTelemetry.

Core design goals:
    - Provide a *stable API* for recording metrics
    - Allow easy adaptation to real telemetry backends later
    - Keep runtime overhead minimal for local/dev environments
    - Make instrumentation calls safe and non-blocking

Usage:

    from premortem_ai.observability.metrics import metrics

    metrics.increment("pipeline.run.count")
    metrics.observe("pipeline.latency.ms", execution_time_ms)
"""

from typing import Dict, Any, Optional
from premortem_ai.utils.logger import logger


class Metrics:
    """
    Lightweight in-process metrics recorder.
    """

    def __init__(self, enabled: bool = True):
        self.enabled = enabled

    def increment(self, name: str, value: int = 1, tags: Optional[Dict[str, Any]] = None):
        if not self.enabled:
            return
        logger.info(f"[metric] increment | {name}={value} | tags={tags or {}}")

    def observe(self, name: str, value: float, tags: Optional[Dict[str, Any]] = None):
        if not self.enabled:
            return
        logger.info(f"[metric] observe | {name}={value} | tags={tags or {}}")

    def event(self, name: str, tags: Optional[Dict[str, Any]] = None):
        if not self.enabled:
            return
        logger.info(f"[metric] event | {name} | tags={tags or {}}")


# Shared global instance
metrics = Metrics()

# ----------------------------------------------------------------------
# LLM-specific metric helpers
# ----------------------------------------------------------------------

def llm_latency(model_name: str, duration: float):
    """
    Records latency for an LLM request.
    """
    metrics.observe("llm.latency", duration, tags={"model": model_name})


def llm_requests_total(model_name: str):
    """
    Increments a counter tracking requests made to a given model.
    """
    metrics.increment("llm.requests.total", tags={"model": model_name})


