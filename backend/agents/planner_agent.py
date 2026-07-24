from typing import Dict, Any, Optional
from backend.agents.base_agent import BaseAgent
from backend.shared.schemas import AgentRole, TaskDAG, TaskNode, TaskStatus
from backend.shared.logging_config import logger

class PlannerAgent(BaseAgent):
    def __init__(self):
        super().__init__(role=AgentRole.PLANNER, prompt_file_name="planner.md")

    async def plan(self, project_id: str, user_prompt: str) -> TaskDAG:
        try:
            result = await self.execute(user_prompt)
            tasks_data = result.get("tasks", [])
            
            nodes = []
            if not tasks_data:
                # Default DAG fallback if LLM response didn't specify array
                nodes = [
                    TaskNode(id="research_design", name="Research Design & UX Specs", agent_role=AgentRole.RESEARCH, dependencies=[]),
                    TaskNode(id="generate_code", name="Generate Application Code", agent_role=AgentRole.CODEGEN, dependencies=["research_design"]),
                    TaskNode(id="debug_build", name="Sandbox Build & Verification", agent_role=AgentRole.DEBUG, dependencies=["generate_code"]),
                    TaskNode(id="generate_docs", name="Generate README & Docs", agent_role=AgentRole.DOCS, dependencies=["debug_build"]),
                ]
            else:
                for t in tasks_data:
                    nodes.append(
                        TaskNode(
                            id=t.get("id"),
                            name=t.get("name", "Task"),
                            agent_role=AgentRole(t.get("agent_role", "codegen")),
                            dependencies=t.get("dependencies", []),
                            metadata=t.get("metadata", {})
                        )
                    )

            return TaskDAG(project_id=project_id, nodes=nodes)
        except Exception as e:
            logger.error(f"PlannerAgent planning error: {e}")
            # Robust fallback DAG
            return TaskDAG(
                project_id=project_id,
                nodes=[
                    TaskNode(id="research_design", name="Research UX Specs", agent_role=AgentRole.RESEARCH, dependencies=[]),
                    TaskNode(id="generate_code", name="Generate Application Code", agent_role=AgentRole.CODEGEN, dependencies=["research_design"]),
                    TaskNode(id="debug_build", name="Sandbox Build & Verification", agent_role=AgentRole.DEBUG, dependencies=["generate_code"]),
                    TaskNode(id="generate_docs", name="Generate Documentation", agent_role=AgentRole.DOCS, dependencies=["debug_build"]),
                ]
            )
