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


# ================================================================
# GLOBAL METRICS INSTANCE  ← MUST NOT BE INDENTED
# ================================================================

metrics = Metrics()


# ================================================================
# LLM HELPERS (TOP LEVEL FUNCTIONS)
# ================================================================

def llm_latency(model_name: str, duration: float):
    metrics.observe(
        "llm.latency",
        duration,
        tags={"model": model_name}
    )


def llm_requests_total(model_name: str):
    metrics.increment(
        "llm.requests.total",
        tags={"model": model_name}
    )
