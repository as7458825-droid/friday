"""Per-session token allocation quota"""

import logging

logger = logging.getLogger(__name__)


def m424_token_allocation_per_session_quota_lock():
    logger.warning("Feature disabled. Enable in config.")
    return "Feature disabled. Enable in config."
