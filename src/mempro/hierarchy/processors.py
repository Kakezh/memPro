"""
Hierarchy Processors - Four-level memory processing
"""

from datetime import datetime
from typing import Optional

from mempro.models import (
    OriginalMemory,
    EpisodeMemory,
    SemanticMemory,
    ThemeMemory,
    MemoryType,
)


class OriginalProcessor:
    """Process raw messages into Original memories."""
    
    async def process(
        self,
        content: str,
        speaker: str = "user",
        session_id: str = "default",
        metadata: Optional[dict] = None,
    ) -> OriginalMemory:
        return OriginalMemory(
            content=content,
            speaker=speaker,
            session_id=session_id,
            timestamp=datetime.utcnow(),
            metadata=metadata or {},
        )


class EpisodeProcessor:
    """Group Original memories into Episodes."""
    
    async def process(
        self,
        originals: list[OriginalMemory],
        boundary_type: str = "topic",
    ) -> EpisodeMemory:
        contents = [o.content for o in originals]
        summary = " ".join(contents)[:500]
        
        return EpisodeMemory(
            summary=summary,
            original_ids=[o.id for o in originals],
            start_time=min(o.timestamp for o in originals),
            end_time=max(o.timestamp for o in originals),
            boundary_type=boundary_type,
            coherence_score=self._calculate_coherence(originals),
        )
    
    def _calculate_coherence(self, originals: list[OriginalMemory]) -> float:
        if len(originals) <= 1:
            return 1.0
        return 0.7


class SemanticProcessor:
    """Extract Semantic memories from Episodes."""
    
    async def process(
        self,
        episode: EpisodeMemory,
        content: str,
        memory_type: MemoryType = MemoryType.FACT,
        entities: Optional[list[str]] = None,
        confidence: float = 0.5,
    ) -> SemanticMemory:
        return SemanticMemory(
            content=content,
            type=memory_type,
            confidence=confidence,
            source_episodes=[episode.id],
            entity_refs=entities or [],
        )


class ThemeProcessor:
    """Organize Semantic memories into Themes."""
    
    async def find_or_create(
        self,
        semantic: SemanticMemory,
        existing_themes: list[ThemeMemory],
    ) -> Optional[ThemeMemory]:
        for entity in semantic.entity_refs:
            for theme in existing_themes:
                if entity.lower() in theme.name.lower():
                    theme.semantic_ids.append(semantic.id)
                    theme.updated_at = datetime.utcnow()
                    return theme
        
        if semantic.entity_refs:
            return ThemeMemory(
                name=semantic.entity_refs[0],
                description=f"Theme for {semantic.entity_refs[0]}",
                semantic_ids=[semantic.id],
            )
        
        return None
