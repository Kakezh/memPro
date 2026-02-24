"""
SQLite Storage Backend
"""

import json
from datetime import datetime
from typing import Optional, Any
import sqlite3

from mempro.database.interfaces import IMemoryStore
from mempro.models import (
    MemoryLevel,
    MemoryStats,
    OriginalMemory,
    EpisodeMemory,
    SemanticMemory,
    ThemeMemory,
)


class SQLiteStore(IMemoryStore):
    """SQLite-based persistent storage backend."""

    def __init__(self, path: str = "memory.db"):
        self.path = path
        self._conn: Optional[sqlite3.Connection] = None

    async def _get_conn(self) -> sqlite3.Connection:
        if self._conn is None:
            self._conn = sqlite3.connect(self.path)
            self._conn.row_factory = sqlite3.Row
            await self._create_tables()
        return self._conn

    async def _create_tables(self) -> None:
        conn = self._conn
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS memories (
                id TEXT PRIMARY KEY,
                level TEXT NOT NULL,
                data TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_level ON memories(level)
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_created ON memories(created_at)
        """)

        conn.commit()

    async def save(self, memory: Any) -> None:
        conn = await self._get_conn()
        cursor = conn.cursor()

        data = memory.model_dump_json()
        cursor.execute(
            """
            INSERT OR REPLACE INTO memories (id, level, data, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                memory.id,
                memory.level.value,
                data,
                memory.created_at.isoformat(),
                memory.updated_at.isoformat(),
            ),
        )
        conn.commit()

    async def get(self, id: str, level: MemoryLevel) -> Optional[Any]:
        conn = await self._get_conn()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT data FROM memories WHERE id = ? AND level = ?",
            (id, level.value),
        )
        row = cursor.fetchone()

        if row is None:
            return None

        return self._deserialize(row["data"], level)

    async def search(self, query: str, level: Optional[MemoryLevel] = None, limit: int = 10) -> list[Any]:
        conn = await self._get_conn()
        cursor = conn.cursor()

        if level:
            cursor.execute(
                """
                SELECT id, level, data FROM memories 
                WHERE level = ? AND data LIKE ?
                ORDER BY created_at DESC
                LIMIT ?
                """,
                (level.value, f"%{query}%", limit),
            )
        else:
            cursor.execute(
                """
                SELECT id, level, data FROM memories 
                WHERE data LIKE ?
                ORDER BY created_at DESC
                LIMIT ?
                """,
                (f"%{query}%", limit),
            )

        results = []
        for row in cursor.fetchall():
            memory_level = MemoryLevel(row["level"])
            memory = self._deserialize(row["data"], memory_level)
            if memory:
                results.append(memory)

        return results

    async def stats(self) -> MemoryStats:
        conn = await self._get_conn()
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) as total FROM memories")
        total = cursor.fetchone()["total"]

        cursor.execute(
            "SELECT level, COUNT(*) as count FROM memories GROUP BY level"
        )
        by_level = {MemoryLevel(row["level"]): row["count"] for row in cursor.fetchall()}

        return MemoryStats(total=total, by_level=by_level)

    async def delete(self, id: str, level: MemoryLevel) -> bool:
        conn = await self._get_conn()
        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM memories WHERE id = ? AND level = ?",
            (id, level.value),
        )
        conn.commit()

        return cursor.rowcount > 0

    async def close(self) -> None:
        if self._conn:
            self._conn.close()
            self._conn = None

    def _deserialize(self, data: str, level: MemoryLevel) -> Optional[Any]:
        try:
            raw = json.loads(data)
            if level == MemoryLevel.ORIGINAL:
                return OriginalMemory(**raw)
            elif level == MemoryLevel.EPISODE:
                return EpisodeMemory(**raw)
            elif level == MemoryLevel.SEMANTIC:
                return SemanticMemory(**raw)
            elif level == MemoryLevel.THEME:
                return ThemeMemory(**raw)
        except Exception:
            return None
        return None
