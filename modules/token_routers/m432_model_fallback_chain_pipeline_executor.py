"""Model fallback chain pipeline"""

import logging

logger = logging.getLogger(__name__)


def m432_model_fallback_chain_pipeline_executor():
    logger.warning("Feature disabled. Enable in config.")
    return "Feature disabled. Enable in config."
