"""
Observability Layer for PreMortem AI.

This package provides lightweight but enterprise-ready telemetry primitives:
    
    - metrics   → counters, gauges, and event markers
    - tracing   → span-based timing and contextual operation visibility

Design goals:
    - Zero external dependencies (OTEL/Datadog optional later)
    - Stable, governed API for instrumentation across the entire system
    - Consistent logging-based fallback for local and CI environments

Modules:
    metrics.py   → Metrics abstraction with increment/observe/event
    tracing.py   → Span/Tracer primitives for pipeline-level visibility

Example usage:

    from premortem_ai.observability import metrics, tracer

    metrics.increment("pipeline.run.count")
    with tracer.start_span("risk.discovery"):
        ...

This ensures the rest of the codebase has unified, framework-agnostic observability.
"""

from .metrics import metrics
from .tracing import tracer

__all__ = [
    "metrics",
    "tracer",
]
