"""
logger.py

Centralized logging utility for PreMortem AI.

This module provides:
    - A single shared logger instance for the entire application
    - Consistent formatting across all modules
    - Log level controlled via global settings
    - Future extensibility for JSON logs, handlers, or observability integrations

Usage:

    from premortem_ai.utils.logger import logger
    logger.info("Pipeline started")
"""

import logging
from premortem_ai.config import settings


# ------------------------------------------------------------------------------
# Logger Setup
# ------------------------------------------------------------------------------

logger = logging.getLogger("premortem_ai")

# Prevent duplicate handler registration if module reloaded
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        fmt="[%(levelname)s] %(asctime)s — %(name)s — %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    handler.setFormatter(formatter)

    logger.addHandler(handler)

# Apply global log level from settings
logger.setLevel(settings.LOG_LEVEL.upper())


# ------------------------------------------------------------------------------
# Future Enhancements (Enterprise Patterns)
# ------------------------------------------------------------------------------
#
# - JSON log formatting for structured logging in cloud environments
# - FileHandler or RotatingFileHandler for long-term storage
# - Integrations with:
#       - OpenTelemetry
#       - Datadog
#       - CloudWatch
# - Redaction helpers for sensitive content
#
# The logger instance above is intentionally minimal but production-ready.
# Extending it does NOT require modifying application-level modules.
#
