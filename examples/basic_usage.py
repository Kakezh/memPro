"""
Basic usage example for memPro
"""

import asyncio
from mempro import MemoryService, MemoryConfig, MemoryType


async def main():
    # Initialize memory service
    config = MemoryConfig()
    service = MemoryService(config)
    await service.init()
    
    # Store memories
    print("Storing memories...")
    
    result1 = await service.memorize(
        content="User prefers dark mode for coding",
        type=MemoryType.PREFERENCE,
        entities=["User", "dark mode", "coding"],
        confidence=0.9,
    )
    print(f"Stored: {result1.semantic_id}")
    
    result2 = await service.memorize(
        content="Project deadline is next Friday",
        type=MemoryType.CONSTRAINT,
        entities=["Project", "deadline"],
        confidence=0.8,
    )
    print(f"Stored: {result2.semantic_id}")
    
    result3 = await service.memorize(
        content="User is learning TypeScript",
        type=MemoryType.FACT,
        entities=["User", "TypeScript"],
        confidence=0.7,
    )
    print(f"Stored: {result3.semantic_id}")
    
    # Retrieve memories
    print("\nRetrieving memories...")
    
    results = await service.retrieve("user preferences")
    print(f"Found {len(results.semantics)} semantic memories")
    for sem in results.semantics:
        print(f"  - {sem.content} (confidence: {sem.confidence})")
    
    # Get stats
    print("\nMemory stats:")
    stats = await service.stats()
    print(f"  Total: {stats.total}")
    print(f"  By level: {stats.by_level}")
    
    # Close
    await service.close()
    print("\nDone!")


if __name__ == "__main__":
    asyncio.run(main())
