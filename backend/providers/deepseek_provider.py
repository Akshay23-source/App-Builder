from typing import AsyncGenerator, Optional
from backend.providers.base_provider import BaseProvider
from backend.shared.config import settings
from backend.shared.logging_config import logger

class DeepSeekProvider(BaseProvider):
    def __init__(self, api_key: Optional[str] = None, model_name: Optional[str] = None):
        super().__init__(
            api_key=api_key or settings.DEEPSEEK_API_KEY,
            model_name=model_name or settings.DEEPSEEK_MODEL
        )
        self._client = None

    def _get_client(self):
        if not self._client:
            if not self.api_key:
                raise ValueError("DEEPSEEK_API_KEY is not set.")
            from openai import AsyncOpenAI
            self._client = AsyncOpenAI(
                api_key=self.api_key,
                base_url="https://api.deepseek.com"
            )
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
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})

            kwargs = {
                "model": self.model_name,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens,
            }
            if response_format_json:
                kwargs["response_format"] = {"type": "json_object"}

            response = await client.chat.completions.create(**kwargs)
            return response.choices[0].message.content or ""
        except Exception as e:
            logger.error(f"DeepSeek completion error: {e}")
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
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})

            stream_res = await client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                stream=True,
            )
            async for chunk in stream_res:
                content = chunk.choices[0].delta.content
                if content:
                    yield content
        except Exception as e:
            logger.error(f"DeepSeek stream error: {e}")
            raise e
