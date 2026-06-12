"""Memory cluster handshake finalizer"""

import logging

logger = logging.getLogger(__name__)


def m600_memory_cluster_handshake_finalizer():
    logger.warning("Feature disabled. Enable in config.")
    return "Feature disabled. Enable in config."
