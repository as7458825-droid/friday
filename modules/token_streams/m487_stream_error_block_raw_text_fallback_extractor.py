"""Stream error raw text fallback"""

import logging

logger = logging.getLogger(__name__)


def m487_stream_error_block_raw_text_fallback_extractor():
    logger.warning("Feature disabled. Enable in config.")
    return "Feature disabled. Enable in config."
