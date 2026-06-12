"""Memory schema migration handler"""

import logging

logger = logging.getLogger(__name__)


def m512_memory_migration_schema_upgrade_handler():
    logger.warning("Feature disabled. Enable in config.")
    return "Feature disabled. Enable in config."
