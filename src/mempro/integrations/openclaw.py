"""
OpenClaw Adapter - Integration with OpenClaw framework
"""

from typing import Any, Optional
from mempro.service import MemoryService
from mempro.config import MemoryConfig
from mempro.models import MemoryType


class OpenClawAdapter:
    """Adapter for OpenClaw framework integration."""

    def __init__(
        self,
        service: Optional[MemoryService] = None,
        config: Optional[MemoryConfig] = None,
        workspace_path: str = "./memory-data",
    ):
        if service:
            self.service = service
        else:
            config = config or MemoryConfig()
            self.service = MemoryService(config)

        self.workspace_path = workspace_path

    async def init(self) -> None:
        """Initialize the adapter."""
        await self.service.init()

    async def remember(
        self,
        content: str,
        memory_type: str = "fact",
        entities: Optional[list[str]] = None,
        confidence: float = 0.5,
    ) -> dict[str, Any]:
        """
        Store a memory (OpenClaw-style API).

        Args:
            content: Content to remember
            memory_type: Type of memory (fact, preference, goal, constraint, event)
            entities: Entity references
            confidence: Confidence score (0-1)

        Returns:
            Result dict with memory IDs
        """
        type_map = {
            "fact": MemoryType.FACT,
            "preference": MemoryType.PREFERENCE,
            "goal": MemoryType.GOAL,
            "constraint": MemoryType.CONSTRAINT,
            "event": MemoryType.EVENT,
        }

        result = await self.service.memorize(
            content=content,
            type=type_map.get(memory_type, MemoryType.FACT),
            entities=entities,
            confidence=confidence,
        )

        return {
            "success": result.success,
            "memory_id": result.semantic_id,
            "message": result.message,
        }

    async def recall(
        self,
        query: str,
        top_k: int = 5,
    ) -> dict[str, Any]:
        """
        Retrieve memories (OpenClaw-style API).

        Args:
            query: Search query
            top_k: Maximum results

        Returns:
            Result dict with memories
        """
        result = await self.service.retrieve(query, top_k)

        return {
            "memories": [
                {
                    "id": m.id,
                    "content": m.content,
                    "type": m.type.value,
                    "confidence": m.confidence,
                    "entities": m.entity_refs,
                }
                for m in result.semantics
            ],
            "themes": [
                {
                    "id": t.id,
                    "name": t.name,
                    "description": t.description,
                }
                for t in result.themes
            ],
            "total_tokens": result.total_tokens,
        }

    async def stats(self) -> dict[str, Any]:
        """Get memory statistics."""
        stats = await self.service.stats()
        return {
            "total": stats.total,
            "by_level": stats.by_level,
        }

    async def close(self) -> None:
        """Close the adapter."""
        await self.service.close()

    def get_tools(self) -> list[dict]:
        """Return tool definitions for OpenClaw."""
        return [
            {
                "type": "function",
                "function": {
                    "name": "memory_remember",
                    "description": "Store information in long-term memory",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "content": {
                                "type": "string",
                                "description": "The content to remember",
                            },
                            "memory_type": {
                                "type": "string",
                                "enum": ["fact", "preference", "goal", "constraint", "event"],
                                "description": "Type of memory",
                            },
                            "entities": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Related entities",
                            },
                            "confidence": {
                                "type": "number",
                                "minimum": 0,
                                "maximum": 1,
                                "description": "Confidence score",
                            },
                        },
                        "required": ["content"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "memory_recall",
                    "description": "Retrieve memories from long-term memory",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "Search query",
                            },
                            "top_k": {
                                "type": "integer",
                                "default": 5,
                                "description": "Maximum results",
                            },
                        },
                        "required": ["query"],
                    },
                },
            },
        ]

    async def execute_tool(self, name: str, params: dict) -> Any:
        """Execute a tool by name."""
        if name == "memory_remember":
            return await self.remember(**params)
        elif name == "memory_recall":
            return await self.recall(**params)
        elif name == "memory_stats":
            return await self.stats()
        else:
            raise ValueError(f"Unknown tool: {name}")


def create_openclaw_plugin(config: Optional[dict] = None) -> OpenClawAdapter:
    """Create an OpenClaw plugin instance."""
    memory_config = MemoryConfig()
    if config:
        if "workspace_path" in config:
            memory_config.storage.path = config["workspace_path"]
        if "storage_backend" in config:
            memory_config.storage.backend = config["storage_backend"]

    return OpenClawAdapter(config=memory_config)
