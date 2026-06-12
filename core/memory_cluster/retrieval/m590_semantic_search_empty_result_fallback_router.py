"""Empty result fallback router"""

import logging

logger = logging.getLogger(__name__)


def m590_semantic_search_empty_result_fallback_router():
    logger.warning("Feature disabled. Enable in config.")
    return "Feature disabled. Enable in config."
