"""
memPro - Proactive Memory Framework for AI Agents

A 24/7 hierarchical memory system inspired by xMemory and memU.
"""

from mempro.service import MemoryService
from mempro.models import (
    OriginalMemory,
    EpisodeMemory,
    SemanticMemory,
    ThemeMemory,
    MemoryType,
    MemoryLevel,
)
from mempro.config import MemoryConfig

__version__ = "0.1.0"
__all__ = [
    "MemoryService",
    "MemoryConfig",
    "OriginalMemory",
    "EpisodeMemory",
    "SemanticMemory",
    "ThemeMemory",
    "MemoryType",
    "MemoryLevel",
]
