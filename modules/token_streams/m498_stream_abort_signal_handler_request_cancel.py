"""Stream abort signal handler"""

import logging

logger = logging.getLogger(__name__)


def m498_stream_abort_signal_handler_request_cancel():
    logger.warning("Feature disabled. Enable in config.")
    return "Feature disabled. Enable in config."
