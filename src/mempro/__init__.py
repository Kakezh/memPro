"""
memPro - Proactive Memory Framework for AI Agents

A 24/7 hierarchical memory system inspired by xMemory and memU.
"""

from mempro.service import MemoryService
from mempro.config import MemoryConfig
from mempro.models import (
    OriginalMemory,
    EpisodeMemory,
    SemanticMemory,
    ThemeMemory,
    MemoryLevel,
    MemoryType,
)

__version__ = "0.1.0"
__all__ = [
    "MemoryService",
    "MemoryConfig",
    "OriginalMemory",
    "EpisodeMemory",
    "SemanticMemory",
    "ThemeMemory",
    "MemoryLevel",
    "MemoryType",
]
