"""HuggingFace remote embedding fallback"""

import logging

logger = logging.getLogger(__name__)


def m535_huggingface_api_remote_embedding_fallback():
    logger.warning("Feature disabled. Enable in config.")
    return "Feature disabled. Enable in config."
