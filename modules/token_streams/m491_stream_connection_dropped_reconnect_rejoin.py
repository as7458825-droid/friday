"""Stream connection reconnect handler"""

import logging

logger = logging.getLogger(__name__)


def m491_stream_connection_dropped_reconnect_rejoin():
    logger.warning("Feature disabled. Enable in config.")
    return "Feature disabled. Enable in config."
