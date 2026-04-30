"""
TellDNS - Fast Subdomain Discovery Tool
High-performance subdomain enumeration with AI & automation
"""

__version__ = "1.0.0"
__author__ = "DarkVector-bot"
__license__ = "MIT"

from .core.engine import TellDNSEngine
from .stages.passive import PassiveStage
from .stages.active import ActiveStage

__all__ = [
    "TellDNSEngine",
    "PassiveStage",
    "ActiveStage"
]
