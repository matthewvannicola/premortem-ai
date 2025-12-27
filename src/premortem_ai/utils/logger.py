"""
logger.py

Centralized logging utility for PreMortem AI.
"""

import logging
from premortem_ai.config import settings

logger = logging.getLogger("premortem_ai")

# Prevent duplicate handlers
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        fmt="[%(levelname)s] %(asctime)s — %(name)s — %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

logger.setLevel(settings.LOG_LEVEL.upper())

# Convenience exports (for full compatibility)
info = logger.info
warning = logger.warning
error = logger.error
debug = logger.debug
