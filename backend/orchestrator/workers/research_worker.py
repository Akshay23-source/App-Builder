import asyncio
from backend.orchestrator.celery_app import celery_app
from backend.shared.schemas import AgentRole, ProjectStatus, TaskStatus
from backend.orchestrator.state_manager import state_manager
from backend.agents.research_agent import ResearchAgent
from backend.db.session import SyncSessionLocal
from backend.db.models import Task
from backend.shared.logging_config import logger

@celery_app.task(name="research_worker.execute")
def run_research(project_id: str, prompt: str, task_key: str):
    logger.info(f"[ResearchWorker] Starting research task for project {project_id}")
    state_manager.update_project_status(project_id, ProjectStatus.RESEARCHING)
    state_manager.update_task_status(project_id, task_key, TaskStatus.RUNNING)
    state_manager.publish_event(
        project_id=project_id,
        agent_role=AgentRole.RESEARCH,
        task_id=task_key,
        event_type="status_update",
        message="Research Agent is searching web benchmarks and synthesizing UI design patterns..."
    )

    db = SyncSessionLocal()
    task_metadata = {}
    try:
        t = db.query(Task).filter(Task.project_id == project_id, Task.task_key == task_key).first()
        if t and t.task_metadata:
            task_metadata = t.task_metadata
    finally:
        db.close()

    agent = ResearchAgent()
    specs = asyncio.run(agent.research(user_prompt=prompt, task_metadata=task_metadata))

    state_manager.update_task_status(project_id, task_key, TaskStatus.SUCCESS, output=specs)
    state_manager.publish_event(
        project_id=project_id,
        agent_role=AgentRole.RESEARCH,
        task_id=task_key,
        event_type="task_completed",
        message="Research Agent finalized design tokens and UI architecture specs.",
        data={"research_specs": specs}
    )

    # Next step: Dispatch CodeGen Worker
    from backend.orchestrator.workers.codegen_worker import run_codegen
    run_codegen.delay(project_id, prompt, "generate_code")
