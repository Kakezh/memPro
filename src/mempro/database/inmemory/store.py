"""
InMemory Storage Backend
"""

from typing import Optional, Any
from mempro.database.interfaces import IMemoryStore
from mempro.models import MemoryLevel, MemoryStats


class InMemoryStore(IMemoryStore):
    def __init__(self):
        self._data: dict[MemoryLevel, dict[str, Any]] = {
            MemoryLevel.ORIGINAL: {},
            MemoryLevel.EPISODE: {},
            MemoryLevel.SEMANTIC: {},
            MemoryLevel.THEME: {},
        }

    async def save(self, memory: Any) -> None:
        level = memory.level
        self._data[level][memory.id] = memory

    async def get(self, id: str, level: MemoryLevel) -> Optional[Any]:
        return self._data[level].get(id)

    async def search(self, query: str, level: Optional[MemoryLevel] = None, limit: int = 10) -> list[Any]:
        results = []
        levels = [level] if level else list(MemoryLevel)
        query_lower = query.lower()
        
        for lvl in levels:
            for memory in self._data[lvl].values():
                content = getattr(memory, 'content', None) or getattr(memory, 'summary', None) or getattr(memory, 'name', None) or ''
                if query_lower in content.lower():
                    results.append(memory)
                    if len(results) >= limit:
                        return results
        return results

    async def stats(self) -> MemoryStats:
        return MemoryStats(
            total=sum(len(v) for v in self._data.values()),
            by_level={lvl: len(memories) for lvl, memories in self._data.items()},
        )

    async def delete(self, id: str, level: MemoryLevel) -> bool:
        if id in self._data[level]:
            del self._data[level][id]
            return True
        return False

    async def close(self) -> None:
        self._data.clear()
