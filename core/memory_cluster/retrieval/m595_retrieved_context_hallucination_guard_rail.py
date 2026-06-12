"""Context hallucination guard"""

import logging

logger = logging.getLogger(__name__)


def m595_retrieved_context_hallucination_guard_rail():
    logger.warning("Feature disabled. Enable in config.")
    return "Feature disabled. Enable in config."
