from typing import Dict, Any, List, Optional
from backend.agents.base_agent import BaseAgent
from backend.shared.schemas import AgentRole, GeneratedFile
from backend.shared.logging_config import logger

class DebugAgent(BaseAgent):
    def __init__(self):
        super().__init__(role=AgentRole.DEBUG, prompt_file_name="debug.md")

    async def fix_errors(
        self,
        user_prompt: str,
        current_files: List[GeneratedFile],
        error_logs: str
    ) -> List[GeneratedFile]:
        context = {
            "current_files": [{"path": f.path, "content": f.content[:1500]} for f in current_files],
            "error_logs": error_logs
        }
        
        result = await self.execute(user_prompt=user_prompt, context=context)
        repaired_raw = result.get("repaired_files", [])
        
        repaired_map = {}
        for item in repaired_raw:
            if isinstance(item, dict) and "path" in item and "content" in item:
                repaired_map[item["path"]] = item["content"]

        # Merge repaired files into original files set
        final_files: List[GeneratedFile] = []
        for f in current_files:
            if f.path in repaired_map:
                final_files.append(GeneratedFile(path=f.path, content=repaired_map[f.path]))
            else:
                final_files.append(f)
                
        for path, content in repaired_map.items():
            if not any(f.path == path for f in final_files):
                final_files.append(GeneratedFile(path=path, content=content))

        return final_files
