"""
OpenAI LLM Provider
"""

from typing import Optional
import json

from mempro.llm.base import LLMProvider


class OpenAIProvider(LLMProvider):
    """OpenAI LLM provider."""

    def __init__(
        self,
        api_key: str,
        model: str = "gpt-4o-mini",
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

    async def complete(
        self,
        prompt: str,
        system: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000,
    ) -> str:
        client = await self._get_client()

        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        response = await client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )

        return response.choices[0].message.content or ""

    async def embed(self, text: str) -> list[float]:
        client = await self._get_client()

        response = await client.embeddings.create(
            model="text-embedding-3-small",
            input=text,
        )

        return response.data[0].embedding
