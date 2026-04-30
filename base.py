"""
BaseStage - Abstract base class for all pipeline stages
"""

from abc import ABC, abstractmethod
from typing import Any


class BaseStage(ABC):
    """Abstract base class for pipeline stages"""
    
    @abstractmethod
    async def run(self, context) -> Any:
        """Run the stage with given context"""
        pass
    
    def get_name(self) -> str:
        """Get stage name"""
        return self.__class__.__name__.replace('Stage', '')
