"""Embedding engine handshake finalizer"""

import logging

logger = logging.getLogger(__name__)


def m550_embedding_engine_handshake_finalizer():
    logger.warning("Feature disabled. Enable in config.")
    return "Feature disabled. Enable in config."
