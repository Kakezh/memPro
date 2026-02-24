"""
LangChain Adapter - Integration with LangChain framework
"""

from typing import Any, Optional, Type
from pydantic import BaseModel, Field

from mempro.service import MemoryService
from mempro.config import MemoryConfig
from mempro.models import MemoryType


class MemoryRememberInput(BaseModel):
    """Input schema for memory_remember tool."""

    content: str = Field(description="The content to remember")
    memory_type: str = Field(
        default="fact",
        description="Type of memory: fact, preference, goal, constraint, event",
    )
    entities: list[str] = Field(
        default_factory=list,
        description="Related entities",
    )
    confidence: float = Field(
        default=0.5,
        ge=0.0,
        le=1.0,
        description="Confidence score",
    )


class MemoryRecallInput(BaseModel):
    """Input schema for memory_recall tool."""

    query: str = Field(description="Search query")
    top_k: int = Field(default=5, description="Maximum results")


class LangChainAdapter:
    """Adapter for LangChain framework integration."""

    def __init__(
        self,
        service: Optional[MemoryService] = None,
        config: Optional[MemoryConfig] = None,
    ):
        self.service = service or MemoryService(config)

    async def init(self) -> None:
        """Initialize the adapter."""
        await self.service.init()

    async def remember(
        self,
        content: str,
        memory_type: str = "fact",
        entities: Optional[list[str]] = None,
        confidence: float = 0.5,
    ) -> str:
        """Store a memory and return a summary."""
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
            entities=entities or [],
            confidence=confidence,
        )

        if result.success:
            return f"Remembered: {content[:100]}..."
        return f"Failed to remember: {result.message}"

    async def recall(self, query: str, top_k: int = 5) -> str:
        """Retrieve memories and return formatted result."""
        result = await self.service.retrieve(query, top_k)

        if not result.semantics:
            return "No relevant memories found."

        lines = ["Found the following relevant memories:"]
        for i, m in enumerate(result.semantics, 1):
            lines.append(f"{i}. [{m.type.value}] {m.content}")

        return "\n".join(lines)

    async def close(self) -> None:
        """Close the adapter."""
        await self.service.close()

    def get_tools(self) -> list[dict]:
        """Return tool definitions for LangChain."""
        return [
            {
                "name": "memory_remember",
                "description": "Store information in long-term memory for future reference",
                "args_schema": MemoryRememberInput,
                "func": self._sync_remember,
            },
            {
                "name": "memory_recall",
                "description": "Retrieve relevant memories from long-term memory",
                "args_schema": MemoryRecallInput,
                "func": self._sync_recall,
            },
        ]

    def _sync_remember(self, content: str, **kwargs) -> str:
        """Synchronous wrapper for remember."""
        import asyncio
        return asyncio.run(self.remember(content, **kwargs))

    def _sync_recall(self, query: str, **kwargs) -> str:
        """Synchronous wrapper for recall."""
        import asyncio
        return asyncio.run(self.recall(query, **kwargs))

    def as_langchain_tools(self):
        """Return as LangChain StructuredTool objects."""
        try:
            from langchain.tools import StructuredTool

            return [
                StructuredTool(
                    name="memory_remember",
                    description="Store information in long-term memory",
                    func=self._sync_remember,
                    args_schema=MemoryRememberInput,
                ),
                StructuredTool(
                    name="memory_recall",
                    description="Retrieve memories from long-term memory",
                    func=self._sync_recall,
                    args_schema=MemoryRecallInput,
                ),
            ]
        except ImportError:
            raise ImportError("langchain package required: pip install langchain")


def create_langchain_tools(config: Optional[MemoryConfig] = None) -> list:
    """Create LangChain tools for memory operations."""
    adapter = LangChainAdapter(config=config)
    return adapter.as_langchain_tools()
