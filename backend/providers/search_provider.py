from typing import List, Dict, Any, Optional
import httpx
from backend.shared.config import settings
from backend.shared.logging_config import logger

class SearchProvider:
    """
    Search Provider adapter using Tavily API for web search grounding.
    Falls back gracefully if key is missing or search fails.
    """
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or settings.TAVILY_API_KEY

    async def search(self, query: str, max_results: int = 5) -> List[Dict[str, Any]]:
        if not self.api_key:
            logger.warning("TAVILY_API_KEY is not set. Returning mock web search grounding.")
            return [
                {
                    "title": f"Best UX practices for {query}",
                    "url": "https://developer.mozilla.org/en-US/docs/Learn",
                    "content": f"Modern web patterns and responsive layout benchmarks for building {query}."
                },
                {
                    "title": f"Next.js Tailwind Components for {query}",
                    "url": "https://ui.shadcn.com",
                    "content": "Use sleek modern dark theme aesthetic, Framer Motion animations, glassmorphism card layouts."
                }
            ]

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                res = await client.post(
                    "https://api.tavily.com/search",
                    json={
                        "api_key": self.api_key,
                        "query": query,
                        "search_depth": "basic",
                        "max_results": max_results,
                    }
                )
                res.raise_for_status()
                data = res.json()
                results = data.get("results", [])
                return [
                    {
                        "title": r.get("title", ""),
                        "url": r.get("url", ""),
                        "content": r.get("content", "")
                    }
                    for r in results
                ]
        except Exception as e:
            logger.error(f"Search provider query error: {e}")
            return []
