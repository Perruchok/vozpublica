"""
Structured logging configuration for VozPública.
Compatible with Azure Application Insights.
"""

import logging
import sys
import os
from typing import Optional


def setup_logger(name: str, level: Optional[str] = None) -> logging.Logger:
    """
    Configures a logger with structured JSON format.
    
    Args:
        name: Logger name (typically __name__)
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
               If not specified, uses LOG_LEVEL environment variable or INFO
    
    Returns:
        Configured logger
        
    Example:
        >>> from backend.utils.logger import setup_logger
        >>> logger = setup_logger(__name__)
        >>> logger.info("Operation completed", extra={"user_id": 123, "duration_ms": 45})
    """
    log_level = level or os.getenv("LOG_LEVEL", "INFO")
    
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, log_level.upper()))
    
    # Avoid duplicating handlers if already exists
    if logger.handlers:
        return logger
    
    # Handler for stdout (Azure Application Insights captures it automatically)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(getattr(logging, log_level.upper()))
    
    # JSON format to facilitate parsing in Application Insights
    # Azure prefers logs in structured format
    formatter = logging.Formatter(
        '{"timestamp":"%(asctime)s", "level":"%(levelname)s", "logger":"%(name)s", '
        '"message":"%(message)s", "module":"%(module)s", "function":"%(funcName)s", '
        '"line":%(lineno)d}'
    )
    
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    # Don't propagate to root logger to avoid duplicates
    logger.propagate = False
    
    return logger


# Default logger for the module
logger = setup_logger(__name__)
