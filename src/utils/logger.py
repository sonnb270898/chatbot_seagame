"""
Logger file config
"""
import os
import logging
from dotenv import load_dotenv

# load all env in .env file
load_dotenv()

# Setup logging configuration
LOG_FORMAT = ("%(asctime)s - %(levelname)s - %(message)s")
LOG_LEVEL = os.environ.get("LOG_LEVEL") or 'INFO'
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(LOG_LEVEL)
logging.basicConfig(format=LOG_FORMAT)


def log_info(message: str = ""):
    """
    Log info
    """
    LOGGER.info(message)


def log_debug(message: str = ""):
    """
    Log debug
    """
    LOGGER.debug(message)


def log_warning(message: str = ""):
    """
    Log debug
    """
    LOGGER.warning(message)


def log_error(message: str = ""):
    """
    Log error
    """
    LOGGER.error(message)
