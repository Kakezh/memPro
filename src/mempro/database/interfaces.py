"""
memPro Database Interfaces
"""

from abc import ABC, abstractmethod
from typing import Optional, Any

from mempro.models import (
    OriginalMemory,
    EpisodeMemory,
    SemanticMemory,
    ThemeMemory,
    MemoryLevel,
    MemoryStats,
)


class IMemoryStore(ABC):
    @abstractmethod
    async def save(self, memory: Any) -> None: ...
    
    @abstractmethod
    async def get(self, id: str, level: MemoryLevel) -> Optional[Any]: ...
    
    @abstractmethod
    async def search(self, query: str, level: Optional[MemoryLevel] = None, limit: int = 10) -> list[Any]: ...
    
    @abstractmethod
    async def stats(self) -> MemoryStats: ...
    
    @abstractmethod
    async def delete(self, id: str, level: MemoryLevel) -> bool: ...
    
    @abstractmethod
    async def close(self) -> None: ...
