# memPro

> **Proactive Memory Framework for AI Agents**

A 24/7 hierarchical memory system inspired by [xMemory](https://arxiv.org/html/2602.02007v1) and [memU](https://github.com/NevaMind-AI/memU).

## Features

- **24/7 Proactive Memory**: Continuous background monitoring and learning
- **Four-Level Hierarchy**: Original → Episode → Semantic → Theme
- **Multi-Backend Storage**: InMemory, SQLite, PostgreSQL
- **LLM Abstraction**: OpenAI, Anthropic, OpenRouter support
- **Framework Integration**: OpenClaw, LangChain adapters

## Installation

```bash
pip install mempro

# With optional dependencies
pip install mempro[sqlite,openai]
```

## Quick Start

```python
from mempro import MemoryService, MemoryConfig

# Initialize
service = MemoryService()
await service.init()

# Memorize
result = await service.memorize(
    content="User prefers dark mode",
    type="preference",
    entities=["User"],
    confidence=0.9
)

# Retrieve
result = await service.retrieve("user preferences")
print(result.evidence)
```

## Architecture

```
memPro/
├── src/mempro/
│   ├── app/           # Core services
│   ├── database/      # Storage backends
│   ├── embedding/     # Embedding providers
│   ├── llm/           # LLM providers
│   ├── hierarchy/     # Four-level processing
│   └── integrations/  # Framework adapters
```

## Four-Level Hierarchy

| Level | Description | Example |
|-------|-------------|---------|
| Original | Raw messages | User input, Agent response |
| Episode | Conversation segments | Continuous message blocks |
| Semantic | Reusable facts | Preferences, goals, constraints |
| Theme | High-level concepts | Projects, domain knowledge |

## License

MIT © Kakezh
