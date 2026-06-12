"""Embedding generation rate limiter"""

import logging

logger = logging.getLogger(__name__)


def m544_embedding_generation_rate_limit_timer():
    logger.warning("Feature disabled. Enable in config.")
    return "Feature disabled. Enable in config."
