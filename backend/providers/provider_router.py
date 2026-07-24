from typing import Dict, Any, Optional
from backend.shared.schemas import AgentRole
from backend.shared.config import settings
from backend.shared.logging_config import logger
from backend.providers.base_provider import BaseProvider
from backend.providers.openai_provider import OpenAIProvider
from backend.providers.anthropic_provider import AnthropicProvider
from backend.providers.deepseek_provider import DeepSeekProvider
from backend.providers.gemini_provider import GeminiProvider

class ProviderRouter:
    """
    Provider Router handles role-to-provider dispatch and automatic fallback handling.
    If the primary provider fails or has missing credentials, it automatically falls back to secondary options.
    """
    def __init__(self):
        self._providers: Dict[str, BaseProvider] = {}
        
    def _instantiate_provider(self, provider_type: str) -> Optional[BaseProvider]:
        try:
            if provider_type == "anthropic" and settings.ANTHROPIC_API_KEY:
                return AnthropicProvider()
            elif provider_type == "openai" and settings.OPENAI_API_KEY:
                return OpenAIProvider()
            elif provider_type == "deepseek" and settings.DEEPSEEK_API_KEY:
                return DeepSeekProvider()
            elif provider_type == "gemini" and settings.GOOGLE_GEMINI_API_KEY:
                return GeminiProvider()
        except Exception as e:
            logger.warning(f"Could not instantiate provider '{provider_type}': {e}")
        return None

    def get_providers_for_role(self, role: AgentRole) -> list[tuple[str, BaseProvider]]:
        """
        Returns an ordered list of (provider_name, provider_instance) for a given agent role.
        """
        role_map = {
            AgentRole.PLANNER: ["anthropic", "openai", "gemini"],
            AgentRole.RESEARCH: ["gemini", "anthropic", "openai"],
            AgentRole.CODEGEN: ["openai", "deepseek", "anthropic"],
            AgentRole.DEBUG: ["openai", "deepseek", "anthropic"],
            AgentRole.DOCS: ["anthropic", "openai", "gemini"],
        }
        
        preferred_types = role_map.get(role, ["openai", "anthropic", "deepseek", "gemini"])
        chain = []
        
        for ptype in preferred_types:
            instance = self._instantiate_provider(ptype)
            if instance:
                chain.append((ptype, instance))
                
        # If no API keys were set, fallback to mock-friendly OpenAI or whichever instance can be constructed
        if not chain:
            logger.warning("No live AI provider keys found in environment. Initializing OpenAI provider in fallback mode.")
            chain.append(("openai_fallback", OpenAIProvider(api_key="mock_key")))
            
        return chain

    async def complete_for_role(
        self,
        role: AgentRole,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 4096,
        response_format_json: bool = False,
    ) -> str:
        chain = self.get_providers_for_role(role)
        last_exception = None

        for ptype, provider in chain:
            try:
                logger.info(f"Dispatching task for role '{role.value}' to provider '{ptype}'")
                return await provider.complete(
                    prompt=prompt,
                    system_prompt=system_prompt,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    response_format_json=response_format_json,
                )
            except Exception as e:
                logger.warning(f"Provider '{ptype}' failed for role '{role.value}': {e}. Trying fallback...")
                last_exception = e

        raise RuntimeError(f"All providers failed for role '{role.value}'. Last error: {last_exception}")

router = ProviderRouter()
