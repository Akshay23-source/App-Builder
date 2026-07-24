from typing import Dict, Any, Optional
from backend.agents.base_agent import BaseAgent
from backend.shared.schemas import AgentRole
from backend.shared.logging_config import logger

class DocsAgent(BaseAgent):
    def __init__(self):
        super().__init__(role=AgentRole.DOCS, prompt_file_name="docs.md")

    async def generate_documentation(self, user_prompt: str, code_summary: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        context = {
            "code_summary": code_summary or {}
        }
        return await self.execute(user_prompt=user_prompt, context=context)
