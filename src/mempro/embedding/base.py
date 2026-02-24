"""
Embedding Base Classes
"""

from abc import ABC, abstractmethod


class EmbeddingProvider(ABC):
    """Abstract base class for embedding providers."""
    
    @abstractmethod
    async def embed(self, text: str) -> list[float]:
        """Generate embedding for text."""
        ...
    
    @abstractmethod
    async def embed_batch(self, texts: list[str]) -> list[list[float]]:
        """Generate embeddings for multiple texts."""
        ...
    
    @property
    @abstractmethod
    def dimension(self) -> int:
        """Return embedding dimension."""
        ...
