"""API key quota exhaustion alert"""

import logging

logger = logging.getLogger(__name__)


def m417_api_key_quota_exhaustion_alert_system():
    logger.warning("Feature disabled. Enable in config.")
    return "Feature disabled. Enable in config."
