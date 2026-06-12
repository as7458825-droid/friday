"""Request interceptor adblocker"""

import logging

logger = logging.getLogger(__name__)


def mod_044_request_interceptor_adblock():
    logger.warning("Feature disabled. Enable in config.")
    return "Feature disabled. Enable in config."
