from typing import Dict, Any, List, Optional
from backend.agents.base_agent import BaseAgent
from backend.shared.schemas import AgentRole, CodeGenOutput, GeneratedFile
from backend.shared.logging_config import logger

class CodeGenAgent(BaseAgent):
    def __init__(self):
        super().__init__(role=AgentRole.CODEGEN, prompt_file_name="codegen.md")

    async def generate_code(self, user_prompt: str, research_specs: Optional[Dict[str, Any]] = None) -> CodeGenOutput:
        context = {
            "research_specs": research_specs or {}
        }
        
        result = await self.execute(user_prompt=user_prompt, context=context)
        raw_files = result.get("files", [])
        
        files: List[GeneratedFile] = []
        for f in raw_files:
            if isinstance(f, dict) and "path" in f and "content" in f:
                files.append(GeneratedFile(path=f["path"], content=f["content"]))
                
        # Guarantee minimal Next.js files if LLM output was partial
        file_paths = {f.path for f in files}
        if "package.json" not in file_paths:
            files.append(GeneratedFile(
                path="package.json",
                content='{\n  "name": "forgeai-app",\n  "version": "0.1.0",\n  "private": true,\n  "scripts": {\n    "dev": "next dev",\n    "build": "next build",\n    "start": "next start"\n  },\n  "dependencies": {\n    "next": "^14.2.0",\n    "react": "^18.3.0",\n    "react-dom": "^18.3.0",\n    "lucide-react": "^0.380.0",\n    "framer-motion": "^11.2.0",\n    "clsx": "^2.1.0",\n    "tailwind-merge": "^2.3.0"\n  },\n  "devDependencies": {\n    "typescript": "^5.4.0",\n    "@types/node": "^20.12.0",\n    "@types/react": "^18.3.0",\n    "@types/react-dom": "^18.3.0",\n    "tailwindcss": "^3.4.0",\n    "postcss": "^8.4.0",\n    "autoprefixer": "^10.4.0"\n  }\n}'
            ))

        return CodeGenOutput(files=files)
