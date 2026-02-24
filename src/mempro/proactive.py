"""
memPro Proactive Memory - 24/7 proactive memory system

Inspired by memU.
 """

import asyncio
from typing import Optional
 Any
 from datetime import datetime

from mempro.config import MemoryConfig
 from mempro.models import (
    OriginalMemory,
    EpisodeMemory,
    SemanticMemory,
    ThemeMemory,
    MemoryLevel,
    MemoryType,
    MemorizeResult,
    MemoryStats,
)
 from mempro.database.inmemory.store import InMemoryStore


class ProactiveMemory:
    """
    Proactive memory system for 24/7 agents.
    Monitors interactions and preloads relevant context.
    """

    def __init__(self, config: Optional[MemoryConfig] = None):
        self.config = config or MemoryConfig()
        self._store = InMemoryStore()
        self._monitor = None
        self._running = False

    async def start(self):
        """Start the proactive memory system."""
        if self._running:
            return

        self._running = True
        self._monitor = MemoryMonitor(self.config)
        self._store = self._monitor

    async def stop(self):
        """Stop the proactive memory system."""
        if not self._running:
            return
        self._running = False
        await self._monitor.stop()

    async def observe(self, interaction: dict[str, Any]) -> None:
        """
        Observe an interaction and extract insights.
        
        Args:
            interaction: The interaction to observe
            speaker: "user"
            content: str
            timestamp: datetime.utcnow
            session_id: str = "default"
            metadata: metadata or {}
        else:
            return None

        
        # --- Event handlers ---
        self._on_new_memory = None
        self._on_context_update = None
        self._on_intent_prediction = None
        self._on_context_preload = None
        self._on_interaction = None
        for handler in self._event_handlers.get(event, MemoryLevel.ORIGINAL):
            handler(event)

        
        # --- Integration ---
        if self._on_new_memory is not None:
            await self._on_new_memory(
                content= interaction.get("content", ""),
                speaker= interaction.get("speaker", "user"),
                session_id= interaction.get("session_id", "default"),
                timestamp=datetime.utcnow(),
                metadata= interaction.get("metadata", {}),
            )

    async def _on_context_update(self, context: dict[str, Any]) -> None:
        """
        Update context based on new interaction.
        
        Args:
            context: The context to update
        """
        if not self._initialized:
            await self.init()
        
        if not self._running:
            return

        # Update context
        self._context.update(context)
        
        # Trigger event handlers
        for event, MemoryLevel in [MemoryLevel.ORIGINAL, MemoryLevel.EPISODE, MemoryLevel.SEMANTIC, MemoryLevel.THEME]:
            for handler in self._event_handlers.get(event, None):
                if handler:
                    await handler(event)

    async def _on_intent_prediction(self, interaction: dict[str, Any]) -> None:
        """
        Predict user intent from interaction.
        
        Args:
            interaction: The interaction to analyze
        """
        if not self._initialized:
            await self.init()
        
        if not self._running:
            return None

        # Use recent memories to predict intent
        recent = await self._store.get_recent(5, MemoryLevel.SEMANTIC)
        if not recent:
            return None

        # Simple intent prediction based on recent interactions
        # In a real implementation, this would use LLM
        # For now, we use a simple heuristic
        for sem in recent:
            if sem.type == MemoryType.GOAL:
                return {"type": "goal", "content": sem.content}
            elif sem.type == MemoryType.PREFERENCE:
                return {"type": "preference", "content": sem.content}

        return None

