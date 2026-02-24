"""
Generic Adapter - Works with any agent framework
"""

from typing import Any, Optional
from mempro.service import MemoryService
from mempro.config import MemoryConfig


class GenericAdapter:
    """Generic adapter for any agent framework."""
    
    def __init__(self, service: Optional[MemoryService] = None, config: Optional[MemoryConfig] = None):
        self.service = service or MemoryService(config)
    
    async def init(self) -> None:
        await self.service.init()
    
    async def memorize(self, content: str, **kwargs) -> Any:
        return await self.service.memorize(content, **kwargs)
    
    async def retrieve(self, query: str, **kwargs) -> Any:
        return await self.service.retrieve(query, **kwargs)
    
    async def stats(self) -> Any:
        return await self.service.stats()
    
    def get_tools(self) -> list[dict]:
        """Return tool definitions for agent frameworks."""
        return [
            {
                "name": "memory_memorize",
                "description": "Store a memory with automatic hierarchy classification",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "content": {"type": "string", "description": "Content to remember"},
                        "type": {"type": "string", "enum": ["fact", "preference", "goal", "constraint", "event"]},
                        "entities": {"type": "array", "items": {"type": "string"}},
                        "confidence": {"type": "number", "minimum": 0, "maximum": 1},
                    },
                    "required": ["content"],
                },
            },
            {
                "name": "memory_retrieve",
                "description": "Retrieve memories using semantic search",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "Search query"},
                        "top_k": {"type": "integer", "default": 5},
                    },
                    "required": ["query"],
                },
            },
            {
                "name": "memory_stats",
                "description": "Get memory system statistics",
                "parameters": {"type": "object", "properties": {}},
            },
        ]
    
    async def execute_tool(self, name: str, params: dict) -> Any:
        """Execute a tool by name."""
        if name == "memory_memorize":
            return await self.memorize(**params)
        elif name == "memory_retrieve":
            return await self.retrieve(**params)
        elif name == "memory_stats":
            return await self.stats()
        else:
            raise ValueError(f"Unknown tool: {name}")
