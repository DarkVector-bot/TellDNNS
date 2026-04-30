"""
Utility modules for TellDNS
"""

from .logger import setup_logger, get_logger
from .config import load_config, save_config
from .wordlist import load_wordlist, save_wordlist

__all__ = [
    "setup_logger",
    "get_logger",
    "load_config",
    "save_config",
    "load_wordlist",
    "save_wordlist"
]
