"""Workspace scanner handshake finalizer"""

import logging

logger = logging.getLogger(__name__)


def m575_workspace_scanner_handshake_finalizer():
    logger.warning("Feature disabled. Enable in config.")
    return "Feature disabled. Enable in config."
