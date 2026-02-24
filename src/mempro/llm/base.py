"""
LLM Base Classes
"""

from abc import ABC, abstractmethod
from typing import Optional


class LLMProvider(ABC):
    """Abstract base class for LLM providers."""
    
    @abstractmethod
    async def complete(
        self,
        prompt: str,
        system: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000,
    ) -> str:
        """Generate completion from prompt."""
        ...
    
    @abstractmethod
    async def embed(self, text: str) -> list[float]:
        """Generate embedding for text."""
        ...
