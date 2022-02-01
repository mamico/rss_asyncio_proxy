"""Top-level package for RSS Asyncio Proxy."""

__author__ = """Mauro Amico"""
__email__ = 'mauro.amico@gmail.com'
__version__ = '0.1.0'

import logging


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(threadName)s %(name)s %(message)s",
)
logger = logging.getLogger(__name__)

TTL = 10 * 60  # 10 minutes
GRACE = 24 * 60 * 60  # 24 hours
