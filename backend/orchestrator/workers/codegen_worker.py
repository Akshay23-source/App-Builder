import asyncio
from backend.orchestrator.celery_app import celery_app
from backend.shared.schemas import AgentRole, ProjectStatus, TaskStatus
from backend.orchestrator.state_manager import state_manager
from backend.agents.codegen_agent import CodeGenAgent
from backend.sandbox.runner import runner
from backend.db.session import SyncSessionLocal
from backend.db.models import Task
from backend.shared.logging_config import logger

@celery_app.task(name="codegen_worker.execute")
def run_codegen(project_id: str, prompt: str, task_key: str):
    logger.info(f"[CodeGenWorker] Starting code generation for project {project_id}")
    state_manager.update_project_status(project_id, ProjectStatus.CODING)
    state_manager.update_task_status(project_id, task_key, TaskStatus.RUNNING)
    state_manager.publish_event(
        project_id=project_id,
        agent_role=AgentRole.CODEGEN,
        task_id=task_key,
        event_type="status_update",
        message="CodeGen Agent is emitting complete Next.js 14 project file tree..."
    )

    db = SyncSessionLocal()
    research_specs = {}
    try:
        t = db.query(Task).filter(Task.project_id == project_id, Task.task_key == "research_design").first()
        if t and t.output:
            research_specs = t.output
    finally:
        db.close()

    from backend.shared.utils import run_async

    agent = CodeGenAgent()
    codegen_output = run_async(agent.generate_code(user_prompt=prompt, research_specs=research_specs))

    # Write files to physical sandbox workspace directory
    project_dir = runner.write_project_files(project_id, codegen_output.files)
    state_manager.save_generated_files(project_id, codegen_output.files)

    for f in codegen_output.files:
        state_manager.publish_event(
            project_id=project_id,
            agent_role=AgentRole.CODEGEN,
            task_id=task_key,
            event_type="file_created",
            message=f"Emitted {f.path} ({len(f.content)} bytes)",
            data={"path": f.path, "bytes": len(f.content)}
        )

    state_manager.update_task_status(
        project_id,
        task_key,
        TaskStatus.SUCCESS,
        output={"file_count": len(codegen_output.files), "workspace_dir": project_dir}
    )
    state_manager.publish_event(
        project_id=project_id,
        agent_role=AgentRole.CODEGEN,
        task_id=task_key,
        event_type="task_completed",
        message=f"CodeGen Agent emitted {len(codegen_output.files)} project files into sandbox.",
        data={"file_count": len(codegen_output.files)}
    )

    # Next step: Dispatch Debug Worker to verify build inside sandbox
    from backend.orchestrator.workers.debug_worker import run_debug
    from backend.orchestrator.dispatcher import dispatch_task
    dispatch_task(run_debug, project_id, prompt, "debug_build")
