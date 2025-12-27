"""
id_generation.py

Enterprise-grade ID generation utilities for PreMortem AI.

Goals:
    • Generate collision-resistant, sortable, human-readable identifiers
    • Maintain consistent prefix patterns required across all canonical models
    • Ensure thread-safe operation with deterministic formatting
"""

import uuid
import threading

# Thread-safe integer counters for deterministic ID generation.
# These counters are not persisted—suitable for API pipelines and ephemeral jobs.
# For distributed systems, UUID fallback ensures global safety.
_counters = {
    "risk": 1,
    "theme": 1,
    "mitigation": 1,
    "score": 1,
}

_counter_lock = threading.Lock()


# ----------------------------------------------------------------------
# Internal counter utility
# ----------------------------------------------------------------------
def _next_counter(prefix: str) -> int:
    """
    Safely increment the counter for the given prefix.
    Thread-safe to prevent ID collisions in multi-threaded runs.
    """
    with _counter_lock:
        current = _counters.get(prefix, 1)
        _counters[prefix] = current + 1
        return current


# ----------------------------------------------------------------------
# ID Format Helpers
# ----------------------------------------------------------------------
def _format_id(prefix: str, number: int) -> str:
    """
    Format IDs into a sortable, deterministic structure:
        prefix-00001
        prefix-00042
        prefix-01050
    """
    return f"{prefix}-{number:05d}"


# ----------------------------------------------------------------------
# Public ID Generators
# ----------------------------------------------------------------------
def generate_risk_id() -> str:
    num = _next_counter("risk")
    return _format_id("risk", num)


def generate_theme_id() -> str:
    num = _next_counter("theme")
    return _format_id("theme", num)


def generate_mitigation_id() -> str:
    num = _next_counter("mitigation")
    return _format_id("mitigation", num)


def generate_score_id() -> str:
    num = _next_counter("score")
    return _format_id("score", num)


# ----------------------------------------------------------------------
# Global Fallback UUID Generator
# ----------------------------------------------------------------------
def generate_uuid_id(prefix: str) -> str:
    """
    Fallback for distributed architectures or cases where counters
    do not guarantee global uniqueness.

    Output example:
        risk-550e8400-e29b-41d4-a716-446655440000
    """
    return f"{prefix}-{uuid.uuid4()}"
