"""Context window overflow handler"""

import logging

logger = logging.getLogger(__name__)


def m412_token_limit_context_window_overflow_handler():
    logger.warning("Feature disabled. Enable in config.")
    return "Feature disabled. Enable in config."
