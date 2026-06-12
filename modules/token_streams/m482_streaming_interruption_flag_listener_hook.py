"""Streaming interruption flag listener"""

import logging

logger = logging.getLogger(__name__)


def m482_streaming_interruption_flag_listener_hook():
    logger.warning("Feature disabled. Enable in config.")
    return "Feature disabled. Enable in config."
