from abc import ABC, abstractmethod
from typing import AsyncGenerator, Optional, Dict, Any

class BaseProvider(ABC):
    """
    Abstract AI Provider Interface using Adapter Pattern.
    Every agent interacts with this interface so backends can be swapped seamlessly.
    """
    def __init__(self, api_key: Optional[str] = None, model_name: Optional[str] = None):
        self.api_key = api_key
        self.model_name = model_name

    @abstractmethod
    async def complete(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 4096,
        response_format_json: bool = False,
    ) -> str:
        """
        Generate complete text response from the model.
        """
        pass

    @abstractmethod
    async def stream(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 4096,
    ) -> AsyncGenerator[str, None]:
        """
        Stream text response token-by-token from the model.
        """
        pass
