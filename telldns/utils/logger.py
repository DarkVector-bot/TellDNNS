"""
Logger - Centralized logging system
"""

import logging
import sys
from typing import Optional


_logger = None
_verbose = False


def setup_logger(verbose: bool = False, log_file: Optional[str] = None) -> logging.Logger:
    """Setup logger for TellDNS"""
    global _logger, _verbose
    _verbose = verbose
    
    # Create logger
    logger = logging.getLogger("TellDNS")
    logger.setLevel(logging.DEBUG if verbose else logging.INFO)
    
    # Clear existing handlers
    logger.handlers.clear()
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG if verbose else logging.INFO)
    
    # Format
    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s: %(message)s',
        datefmt='%H:%M:%S'
    )
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler (optional)
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    _logger = logger
    return logger


def get_logger() -> logging.Logger:
    """Get the logger instance"""
    global _logger
    if _logger is None:
        setup_logger()
    return _logger


def log_info(message: str):
    """Log info message"""
    get_logger().info(message)


def log_warning(message: str):
    """Log warning message"""
    get_logger().warning(message)


def log_error(message: str):
    """Log error message"""
    get_logger().error(message)


def log_debug(message: str):
    """Log debug message (only in verbose mode)"""
    if _verbose:
        get_logger().debug(message)
