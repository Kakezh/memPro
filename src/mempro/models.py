"""
memPro Data Models

Four-level memory hierarchy:
- Original: Raw messages
- Episode: Conversation segments
- Semantic: Reusable facts
- Theme: High-level concepts
"""

from datetime import datetime
from enum import Enum
from typing import Any, Optional
from uuid import uuid4

from pydantic import BaseModel, Field


class MemoryLevel(str, Enum):
    ORIGINAL = "original"
    EPISODE = "episode"
    SEMANTIC = "semantic"
    THEME = "theme"


class MemoryType(str, Enum):
    FACT = "fact"
    PREFERENCE = "preference"
    GOAL = "goal"
    CONSTRAINT = "constraint"
    EVENT = "event"


class MemoryBase(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    metadata: dict[str, Any] = Field(default_factory=dict)


class OriginalMemory(MemoryBase):
    level: MemoryLevel = MemoryLevel.ORIGINAL
    content: str
    speaker: str = "user"
    session_id: str = "default"
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class EpisodeMemory(MemoryBase):
    level: MemoryLevel = MemoryLevel.EPISODE
    summary: str
    original_ids: list[str] = Field(default_factory=list)
    start_time: datetime = Field(default_factory=datetime.utcnow)
    end_time: datetime = Field(default_factory=datetime.utcnow)
    coherence_score: float = Field(default=0.5, ge=0.0, le=1.0)
    boundary_type: str = "topic"


class SemanticMemory(MemoryBase):
    level: MemoryLevel = MemoryLevel.SEMANTIC
    content: str
    type: MemoryType = MemoryType.FACT
    confidence: float = Field(default=0.5, ge=0.0, le=1.0)
    source_episodes: list[str] = Field(default_factory=list)
    entity_refs: list[str] = Field(default_factory=list)
    validity_start: Optional[datetime] = None
    validity_end: Optional[datetime] = None


class ThemeMemory(MemoryBase):
    level: MemoryLevel = MemoryLevel.THEME
    name: str
    description: str = ""
    semantic_ids: list[str] = Field(default_factory=list)
    parent_theme_id: Optional[str] = None
    child_theme_ids: list[str] = Field(default_factory=list)
    coherence_score: float = Field(default=0.5, ge=0.0, le=1.0)


AnyMemory = OriginalMemory | EpisodeMemory | SemanticMemory | ThemeMemory


class MemorizeResult(BaseModel):
    success: bool = True
    original_id: Optional[str] = None
    episode_id: Optional[str] = None
    semantic_id: Optional[str] = None
    theme_id: Optional[str] = None
    message: str = ""


class RetrieveResult(BaseModel):
    themes: list[ThemeMemory] = Field(default_factory=list)
    semantics: list[SemanticMemory] = Field(default_factory=list)
    episodes: list[EpisodeMemory] = Field(default_factory=list)
    originals: list[OriginalMemory] = Field(default_factory=list)
    total_tokens: int = 0
    evidence_density: float = 0.0


class MemoryStats(BaseModel):
    total: int = 0
    by_level: dict[str, int] = Field(default_factory=dict)
    by_type: dict[str, int] = Field(default_factory=dict)
    avg_confidence: float = 0.0
