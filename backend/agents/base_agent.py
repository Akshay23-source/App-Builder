import os
import json
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from backend.shared.schemas import AgentRole
from backend.shared.logging_config import logger
from backend.providers.provider_router import router

class BaseAgent(ABC):
    def __init__(self, role: AgentRole, prompt_file_name: str):
        self.role = role
        self.prompt_file_name = prompt_file_name
        self.system_prompt = self._load_system_prompt()

    def _load_system_prompt(self) -> str:
        prompt_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "prompts", self.prompt_file_name)
        )
        if os.path.exists(prompt_path):
            with open(prompt_path, "r", encoding="utf-8") as f:
                return f.read()
        logger.warning(f"Prompt file {prompt_path} not found. Using default prompt.")
        return f"You are the {self.role.value} agent for ForgeAI."

    async def execute(self, user_prompt: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Executes the agent logic by formatting prompt, dispatching to provider router, and parsing response.
        """
        logger.info(f"Agent [{self.role.value}] starting task execution...")
        full_prompt = self._format_prompt(user_prompt, context)
        
        raw_response = await router.complete_for_role(
            role=self.role,
            prompt=full_prompt,
            system_prompt=self.system_prompt,
            temperature=0.4 if self.role in [AgentRole.CODEGEN, AgentRole.DEBUG] else 0.7,
            response_format_json=True
        )
        
        parsed = self._clean_and_parse_json(raw_response)
        return parsed

    def _format_prompt(self, user_prompt: str, context: Optional[Dict[str, Any]] = None) -> str:
        formatted = f"USER REQUEST: {user_prompt}\n"
        if context:
            formatted += f"\nCONTEXT & PREVIOUS AGENT OUTPUTS:\n{json.dumps(context, indent=2)}\n"
        return formatted

    def _clean_and_parse_json(self, response_text: str) -> Dict[str, Any]:
        text = response_text.strip()
        if text.startswith("```json"):
            text = text[7:]
        if text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
        text = text.strip()

        try:
            return json.loads(text)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse agent JSON output: {e}\nRaw output: {response_text[:300]}")
            return {"raw_text": response_text, "parse_error": str(e)}
