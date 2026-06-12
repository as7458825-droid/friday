"""Corrupted file skip logger"""

import logging

logger = logging.getLogger(__name__)


def m565_broken_corrupted_file_reading_skip_logger():
    logger.warning("Feature disabled. Enable in config.")
    return "Feature disabled. Enable in config."
