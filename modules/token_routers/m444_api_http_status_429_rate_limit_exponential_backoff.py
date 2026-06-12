"""HTTP 429 rate limit backof"""

import logging

logger = logging.getLogger(__name__)


def m444_api_http_status_429_rate_limit_exponential_backoff():
    logger.warning("Feature disabled. Enable in config.")
    return "Feature disabled. Enable in config."
