"""
OpenAI Embeddings Provider
"""

from typing import Optional

from mempro.embedding.base import EmbeddingProvider


class OpenAIEmbedding(EmbeddingProvider):
    """OpenAI embeddings provider."""

    def __init__(
        self,
        api_key: str,
        model: str = "text-embedding-3-small",
        base_url: Optional[str] = None,
    ):
        self.api_key = api_key
        self.model = model
        self.base_url = base_url or "https://api.openai.com/v1"
        self._client = None

    async def _get_client(self):
        if self._client is None:
            try:
                import openai
                self._client = openai.AsyncOpenAI(
                    api_key=self.api_key,
                    base_url=self.base_url,
                )
            except ImportError:
                raise ImportError("openai package required: pip install openai")
        return self._client

    async def embed(self, text: str) -> list[float]:
        client = await self._get_client()

        response = await client.embeddings.create(
            model=self.model,
            input=text,
        )

        return response.data[0].embedding

    async def embed_batch(self, texts: list[str]) -> list[list[float]]:
        client = await self._get_client()

        response = await client.embeddings.create(
            model=self.model,
            input=texts,
        )

        return [item.embedding for item in response.data]

    @property
    def dimension(self) -> int:
        dimensions = {
            "text-embedding-3-small": 1536,
            "text-embedding-3-large": 3072,
            "text-embedding-ada-002": 1536,
        }
        return dimensions.get(self.model, 1536)
