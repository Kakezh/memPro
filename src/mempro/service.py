"""
memPro MemoryService - Main Entry Point
"""

from typing import Optional, Any
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
    RetrieveResult,
    MemoryStats,
)
from mempro.database.inmemory.store import InMemoryStore


class MemoryService:
    """
    Main memory service providing memorize, retrieve, and proactive operations.
    """

    def __init__(self, config: Optional[MemoryConfig] = None):
        self.config = config or MemoryConfig()
        self._store = InMemoryStore()
        self._initialized = False

    async def init(self) -> None:
        """Initialize the memory service."""
        if self._initialized:
            return
        await self._store.stats()
        self._initialized = True

    async def memorize(
        self,
        content: str,
        type: MemoryType = MemoryType.FACT,
        entities: Optional[list[str]] = None,
        confidence: float = 0.5,
        metadata: Optional[dict[str, Any]] = None,
    ) -> MemorizeResult:
        """
        Store a memory with automatic hierarchy classification.
        """
        if not self._initialized:
            await self.init()

        now = datetime.utcnow()
        entities = entities or []
        metadata = metadata or {}

        # Level 1: Original
        original = OriginalMemory(
            content=content,
            speaker=metadata.get("speaker", "user"),
            session_id=metadata.get("session_id", "default"),
            timestamp=now,
            metadata=metadata,
        )
        await self._store.save(original)

        # Level 2: Episode
        episode = EpisodeMemory(
            summary=content[:200] if len(content) > 200 else content,
            original_ids=[original.id],
            start_time=now,
            end_time=now,
            coherence_score=confidence,
        )
        await self._store.save(episode)

        # Level 3: Semantic
        semantic = SemanticMemory(
            content=content,
            type=type,
            confidence=confidence,
            source_episodes=[episode.id],
            entity_refs=entities,
        )
        await self._store.save(semantic)

        # Level 4: Theme
        theme = await self._find_or_create_theme(semantic, entities)
        if theme:
            theme.semantic_ids.append(semantic.id)
            await self._store.save(theme)

        return MemorizeResult(
            success=True,
            original_id=original.id,
            episode_id=episode.id,
            semantic_id=semantic.id,
            theme_id=theme.id if theme else None,
            message="Memory stored successfully",
        )

    async def retrieve(
        self,
        query: str,
        top_k: int = 5,
    ) -> RetrieveResult:
        """
        Retrieve memories using semantic search.
        """
        if not self._initialized:
            await self.init()

        # Search semantics
        semantics = await self._store.search(query, MemoryLevel.SEMANTIC, top_k)

        # Get related themes
        theme_ids = set()
        for sem in semantics:
            for entity in sem.entity_refs:
                themes = await self._store.search(entity, MemoryLevel.THEME, 1)
                for t in themes:
                    theme_ids.add(t.id)

        themes = []
        for tid in theme_ids:
            theme = await self._store.get(tid, MemoryLevel.THEME)
            if theme:
                themes.append(theme)

        # Get related episodes
        episode_ids = set()
        for sem in semantics:
            episode_ids.update(sem.source_episodes)

        episodes = []
        for eid in episode_ids:
            episode = await self._store.get(eid, MemoryLevel.EPISODE)
            if episode:
                episodes.append(episode)

        return RetrieveResult(
            themes=themes,
            semantics=semantics,
            episodes=episodes,
            total_tokens=sum(len(s.content) for s in semantics) // 4,
            evidence_density=len(semantics) / max(1, top_k),
        )

    async def stats(self) -> MemoryStats:
        """Get memory statistics."""
        return await self._store.stats()

    async def close(self) -> None:
        """Close the memory service."""
        await self._store.close()
        self._initialized = False

    async def _find_or_create_theme(
        self, semantic: SemanticMemory, entities: list[str]
    ) -> Optional[ThemeMemory]:
        """Find existing theme or create new one."""
        for entity in entities:
            themes = await self._store.search(entity, MemoryLevel.THEME, 1)
            if themes:
                return themes[0]

        if entities:
            theme = ThemeMemory(
                name=entities[0],
                description=f"Theme for {entities[0]}",
                semantic_ids=[],
            )
            await self._store.save(theme)
            return theme

        return None
