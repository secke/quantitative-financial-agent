"""Logging configuration for the Financial Agent."""

import sys
from loguru import logger
from src.config.settings import settings

def setup_logger():
    """Configure loguru logger with file and console output."""
    
    # Remove default handler
    logger.remove()
    
    # Add console handler with color
    logger.add(
        sys.stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>",
        level="INFO",
        colorize=True,
    )
    
    # Add file handler
    logger.add(
        settings.LOGS_DIR / "financial_agent.log",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function} - {message}",
        level="DEBUG",
        rotation="10 MB",
        retention="7 days",
        compression="zip",
    )
    
    return logger

# Initialize logger
log = setup_logger()
