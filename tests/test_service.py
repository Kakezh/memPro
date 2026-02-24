"""
Tests for memPro
"""

import pytest
from mempro import MemoryService, MemoryConfig, MemoryType, MemoryLevel
from mempro.models import OriginalMemory, EpisodeMemory, SemanticMemory, ThemeMemory


@pytest.fixture
async def service():
    """Create a memory service for testing."""
    config = MemoryConfig()
    service = MemoryService(config)
    await service.init()
    yield service
    await service.close()


@pytest.mark.asyncio
async def test_memorize(service):
    """Test storing a memory."""
    result = await service.memorize(
        content="Test content",
        type=MemoryType.FACT,
        entities=["Test"],
        confidence=0.8,
    )
    
    assert result.success is True
    assert result.original_id is not None
    assert result.episode_id is not None
    assert result.semantic_id is not None


@pytest.mark.asyncio
async def test_retrieve(service):
    """Test retrieving memories."""
    # Store a memory
    await service.memorize(
        content="User likes Python programming",
        type=MemoryType.PREFERENCE,
        entities=["User", "Python"],
    )
    
    # Retrieve it
    result = await service.retrieve("Python")
    
    assert len(result.semantics) > 0
    assert "Python" in result.semantics[0].content


@pytest.mark.asyncio
async def test_stats(service):
    """Test getting memory statistics."""
    # Store some memories
    await service.memorize("Memory 1", type=MemoryType.FACT)
    await service.memorize("Memory 2", type=MemoryType.PREFERENCE)
    
    stats = await service.stats()
    
    assert stats.total >= 2
    assert stats.by_level[MemoryLevel.ORIGINAL] >= 2
    assert stats.by_level[MemoryLevel.SEMANTIC] >= 2


def test_models():
    """Test model creation."""
    original = OriginalMemory(content="Test")
    assert original.level == MemoryLevel.ORIGINAL
    
    episode = EpisodeMemory(summary="Test episode")
    assert episode.level == MemoryLevel.EPISODE
    
    semantic = SemanticMemory(content="Test semantic")
    assert semantic.level == MemoryLevel.SEMANTIC
    
    theme = ThemeMemory(name="Test theme")
    assert theme.level == MemoryLevel.THEME
