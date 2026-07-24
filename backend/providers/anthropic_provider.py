from typing import AsyncGenerator, Optional
from backend.providers.base_provider import BaseProvider
from backend.shared.config import settings
from backend.shared.logging_config import logger

class AnthropicProvider(BaseProvider):
    def __init__(self, api_key: Optional[str] = None, model_name: Optional[str] = None):
        super().__init__(
            api_key=api_key or settings.ANTHROPIC_API_KEY,
            model_name=model_name or settings.ANTHROPIC_MODEL
        )
        self._client = None

    def _get_client(self):
        if not self._client:
            if not self.api_key:
                raise ValueError("ANTHROPIC_API_KEY is not set.")
            from anthropic import AsyncAnthropic
            self._client = AsyncAnthropic(api_key=self.api_key)
        return self._client

    async def complete(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 4096,
        response_format_json: bool = False,
    ) -> str:
        try:
            client = self._get_client()
            kwargs = {
                "model": self.model_name,
                "max_tokens": max_tokens,
                "temperature": temperature,
                "messages": [{"role": "user", "content": prompt}],
            }
            if system_prompt:
                kwargs["system"] = system_prompt

            response = await client.messages.create(**kwargs)
            return response.content[0].text if response.content else ""
        except Exception as e:
            logger.error(f"Anthropic completion error: {e}")
            raise e

    async def stream(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 4096,
    ) -> AsyncGenerator[str, None]:
        try:
            client = self._get_client()
            kwargs = {
                "model": self.model_name,
                "max_tokens": max_tokens,
                "temperature": temperature,
                "messages": [{"role": "user", "content": prompt}],
            }
            if system_prompt:
                kwargs["system"] = system_prompt

            async with client.messages.stream(**kwargs) as stream:
                async for text in stream.text_stream:
                    yield text
        except Exception as e:
            logger.error(f"Anthropic stream error: {e}")
            raise e
