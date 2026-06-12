"""API telemetry handshake finalizer"""

import logging

logger = logging.getLogger(__name__)


def m500_api_telemetry_cluster_handshake_finalizer():
    logger.warning("Feature disabled. Enable in config.")
    return "Feature disabled. Enable in config."
