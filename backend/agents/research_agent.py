from typing import Dict, Any, Optional
from backend.agents.base_agent import BaseAgent
from backend.shared.schemas import AgentRole
from backend.providers.search_provider import SearchProvider
from backend.shared.logging_config import logger

class ResearchAgent(BaseAgent):
    def __init__(self):
        super().__init__(role=AgentRole.RESEARCH, prompt_file_name="research.md")
        self.search_provider = SearchProvider()

    async def research(self, user_prompt: str, task_metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        query = task_metadata.get("query", user_prompt) if task_metadata else user_prompt
        logger.info(f"ResearchAgent executing live web search grounding for query: '{query}'")
        
        search_results = await self.search_provider.search(query=query, max_results=3)
        context = {
            "search_grounding": search_results,
            "task_metadata": task_metadata or {}
        }
        
        return await self.execute(user_prompt=user_prompt, context=context)
