"""Logger configuration for PyPostgres."""

import logging
import logging.config

from config.settings import LOGGING_CONFIG


def setup_logging():
    """Configure logging based on settings."""
    logging.config.dictConfig(LOGGING_CONFIG)
    return logging.getLogger(__name__)
