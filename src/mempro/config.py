"""
memPro Configuration
"""

from typing import Literal, Optional
from pydantic import BaseModel, Field


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
    max_theme_size: int = Field(default=50, ge=1, le=1000)
    min_theme_coherence: float = Field(default=0.7, ge=0.0, le=1.0)
    auto_reorganize: bool = True


class RetrievalConfig(BaseModel):
    theme_top_k: int = Field(default=3, ge=1, le=20)
    semantic_top_k: int = Field(default=5, ge=1, le=50)
    max_tokens: int = Field(default=4000, ge=100, le=32000)


class ProactiveConfig(BaseModel):
    enabled: bool = False
    monitor_interval: float = Field(default=1.0, ge=0.1, le=60.0)
    context_preload: bool = True
    intent_prediction: bool = True


class MemoryConfig(BaseModel):
    storage: StorageConfig = Field(default_factory=StorageConfig)
    llm: Optional[LLMProfile] = None
    hierarchy: HierarchyConfig = Field(default_factory=HierarchyConfig)
    retrieval: RetrievalConfig = Field(default_factory=RetrievalConfig)
    proactive: ProactiveConfig = Field(default_factory=ProactiveConfig)
