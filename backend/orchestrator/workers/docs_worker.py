import asyncio
from backend.orchestrator.celery_app import celery_app
from backend.shared.schemas import AgentRole, ProjectStatus, TaskStatus
from backend.orchestrator.state_manager import state_manager
from backend.agents.docs_agent import DocsAgent
from backend.shared.logging_config import logger

@celery_app.task(name="docs_worker.execute")
def run_docs(project_id: str, prompt: str, task_key: str):
    logger.info(f"[DocsWorker] Starting documentation generation for project {project_id}")
    state_manager.update_project_status(project_id, ProjectStatus.DOCUMENTING)
    state_manager.update_task_status(project_id, task_key, TaskStatus.RUNNING)
    state_manager.publish_event(
        project_id=project_id,
        agent_role=AgentRole.DOCS,
        task_id=task_key,
        event_type="status_update",
        message="Documentation Agent is writing project README.md and component architecture specs..."
    )

    from backend.shared.utils import run_async

    docs_agent = DocsAgent()
    docs = run_async(docs_agent.generate_documentation(user_prompt=prompt))

    state_manager.update_task_status(project_id, task_key, TaskStatus.SUCCESS, output=docs)
    
    # Mark whole project as COMPLETED
    preview_url = f"http://localhost:3000/dashboard/{project_id}/preview"
    state_manager.update_project_status(project_id, ProjectStatus.COMPLETED, preview_url=preview_url)
    
    state_manager.publish_event(
        project_id=project_id,
        agent_role=AgentRole.DOCS,
        task_id=task_key,
        event_type="task_completed",
        message="🎉 Build process complete! Web application is live and running.",
        data={"preview_url": preview_url, "docs": docs}
    )
