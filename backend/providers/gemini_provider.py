from typing import AsyncGenerator, Optional
from backend.providers.base_provider import BaseProvider
from backend.shared.config import settings
from backend.shared.logging_config import logger

class GeminiProvider(BaseProvider):
    def __init__(self, api_key: Optional[str] = None, model_name: Optional[str] = None):
        super().__init__(
            api_key=api_key or settings.GOOGLE_GEMINI_API_KEY,
            model_name=model_name or settings.GEMINI_MODEL
        )
        self._configured = False

    def _ensure_configured(self):
        if not self._configured:
            if not self.api_key:
                raise ValueError("GOOGLE_GEMINI_API_KEY is not set.")
            import google.generativeai as genai
            genai.configure(api_key=self.api_key)
            self._configured = True

    async def complete(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 4096,
        response_format_json: bool = False,
    ) -> str:
        try:
            self._ensure_configured()
            import google.generativeai as genai
            
            model = genai.GenerativeModel(
                model_name=self.model_name,
                system_instruction=system_prompt if system_prompt else None
            )
            
            gen_config = genai.GenerationConfig(
                temperature=temperature,
                max_output_tokens=max_tokens,
                response_mime_type="application/json" if response_format_json else "text/plain"
            )
            
            res = await model.generate_content_async(prompt, generation_config=gen_config)
            return res.text or ""
        except Exception as e:
            logger.error(f"Gemini completion error: {e}")
            raise e

    async def stream(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 4096,
    ) -> AsyncGenerator[str, None]:
        try:
            self._ensure_configured()
            import google.generativeai as genai
            
            model = genai.GenerativeModel(
                model_name=self.model_name,
                system_instruction=system_prompt if system_prompt else None
            )
            
            gen_config = genai.GenerationConfig(
                temperature=temperature,
                max_output_tokens=max_tokens,
            )
            
            res = await model.generate_content_async(prompt, generation_config=gen_config, stream=True)
            async for chunk in res:
                if chunk.text:
                    yield chunk.text
        except Exception as e:
            logger.error(f"Gemini stream error: {e}")
            raise e
