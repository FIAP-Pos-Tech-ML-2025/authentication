import logging
import sys
from src.config import settings

def get_logger(name: str = __name__):
    logger = logging.getLogger(name)
    if not logger.handlers:
        level = logging.getLevelName(settings.LOG_LEVEL)
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s %(name)s %(message)s',
            '%Y-%m-%d %H:%M:%S'
        ))
        logger.setLevel(level)
        logger.addHandler(handler)
    return logger