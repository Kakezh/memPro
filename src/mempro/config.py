"""
memPro Configuration
"""

from typing import Literal, Optional
from pydantic import BaseModel


class LLMProfile(BaseModel):
    provider: Literal["openai", "anthropic", "openrouter", "custom"] = "openai"
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    model: str = "gpt-4o-mini"
    embed_model: Optional[str] = None


class StorageConfig(BaseModel):
    backend: Literal["memory", "sqlite", "postgres"] = "memory"
    path: Optional[str] = None
    connection_string: Optional[str] = None


class HierarchyConfig(BaseModel):
    max_theme_size: int = 50
    min_theme_coherence: float = 0.7
    auto_reorganize: bool = True


class RetrievalConfig(BaseModel):
    theme_top_k: int = 3
    semantic_top_k: int = 5
    max_tokens: int = 4000


class ProactiveConfig(BaseModel):
    enabled: bool = False
    monitor_interval: float = 1.0
    context_preload: bool = True
    intent_prediction: bool = True


class MemoryConfig(BaseModel):
    storage: StorageConfig = None
    llm: Optional[LLMProfile] = None
    hierarchy: HierarchyConfig = None
    retrieval: RetrievalConfig = None
    proactive: ProactiveConfig = None
    
    def __init__(self, **data):
        super().__init__(**data)
        if self.storage is None:
            self.storage = StorageConfig()
        if self.hierarchy is None:
            self.hierarchy = HierarchyConfig()
        if self.retrieval is None:
            self.retrieval = RetrievalConfig()
        if self.proactive is None:
            self.proactive = ProactiveConfig()
