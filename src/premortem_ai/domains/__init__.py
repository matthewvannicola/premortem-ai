"""
Domain modules for the PreMortem AI pipeline.

Each subpackage corresponds to a distinct analytical phase of the pipeline:
    - discovery: Extract and structure raw risks from project descriptions
    - scoring: Compute severity scores using deterministic + LLM-assisted logic
    - themes: Cluster risks into emergent themes
    - mitigation: Generate actionable mitigation strategies
    - summary: Produce executive-ready narrative summaries
    - reporting: Assemble artifacts into final output documents

Design Principles:
    - Each domain owns a single, well-defined responsibility.
    - Cross-domain dependencies flow only forward (no circular imports).
    - Domain modules should expose a single entrypoint function per step
      (e.g., `run_discovery`, `run_scoring`, etc.).
    - All business logic stays within its domain folder; pipeline modules
      orchestrate execution but do not implement domain-specific behavior.

External modules should import domain entrypoints explicitly from their
respective subpackages, not from this package root.
"""

__all__ = []
