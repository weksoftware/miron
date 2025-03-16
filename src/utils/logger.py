import os
import sys
from loguru import logger

STDERR_FORMAT = (
    "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green>"
    " | <level>{level}</level>"
    " | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan>"
    " | - <level>{message}</level>"
)
FILE_FORMAT = (
    "{time:YYYY-MM-DD HH:mm:ss.SSS}"
    " | {level}"
    " | {name}:{function}:{line}"
    " | - {message}"
)


def setup_logger():
    """Setup loguru logger
    """
    logger.remove()
    
    logger.add(sys.stderr, format=STDERR_FORMAT)
    
    for level in ["DEBUG", "INFO", "ERROR"]:
        logger.add(os.path.join("logs", f"{level.lower()}.log"), level=level, format=FILE_FORMAT, rotation="5 MB", enqueue=True)

