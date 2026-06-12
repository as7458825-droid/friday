"""Dynamic max-tokens guard rail"""

import logging

logger = logging.getLogger(__name__)


def m447_dynamic_max_tokens_parameter_guard_rail():
    logger.warning("Feature disabled. Enable in config.")
    return "Feature disabled. Enable in config."
