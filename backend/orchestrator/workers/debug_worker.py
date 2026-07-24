import asyncio
from backend.orchestrator.celery_app import celery_app
from backend.shared.schemas import AgentRole, ProjectStatus, TaskStatus, GeneratedFile
from backend.orchestrator.state_manager import state_manager
from backend.agents.debug_agent import DebugAgent
from backend.sandbox.runner import runner
from backend.db.session import SyncSessionLocal
from backend.db.models import ProjectFile
from backend.shared.config import settings
from backend.shared.logging_config import logger

@celery_app.task(name="debug_worker.execute")
def run_debug(project_id: str, prompt: str, task_key: str):
    logger.info(f"[DebugWorker] Starting build verification and debug loop for project {project_id}")
    state_manager.update_project_status(project_id, ProjectStatus.DEBUGGING)
    state_manager.update_task_status(project_id, task_key, TaskStatus.RUNNING)
    state_manager.publish_event(
        project_id=project_id,
        agent_role=AgentRole.DEBUG,
        task_id=task_key,
        event_type="status_update",
        message="Debug Agent is running `npm install && npm run build` inside sandbox environment..."
    )

    db = SyncSessionLocal()
    db_files = []
    try:
        db_files = db.query(ProjectFile).filter(ProjectFile.project_id == project_id).all()
    finally:
        db.close()

    current_files = [GeneratedFile(path=f.path, content=f.content) for f in db_files]
    max_retries = settings.MAX_DEBUG_RETRIES
    attempt = 0
    build_success = False
    build_logs = ""

    while attempt < max_retries:
        attempt += 1
        state_manager.publish_event(
            project_id=project_id,
            agent_role=AgentRole.DEBUG,
            task_id=task_key,
            event_type="log",
            message=f"Build Attempt #{attempt}/{max_retries} executing..."
        )

        from backend.shared.utils import run_async

        build_success, build_logs = run_async(runner.run_build_check(project_id))
        
        if build_success:
            state_manager.publish_event(
                project_id=project_id,
                agent_role=AgentRole.DEBUG,
                task_id=task_key,
                event_type="log",
                message=f"✓ Build succeeded on attempt #{attempt}! Zero compilation errors."
            )
            break
        else:
            state_manager.publish_event(
                project_id=project_id,
                agent_role=AgentRole.DEBUG,
                task_id=task_key,
                event_type="error",
                message=f"Build failed on attempt #{attempt}. Invoking Debug Agent for automated repair..."
            )
            
            debug_agent = DebugAgent()
            repaired_files = run_async(
                debug_agent.fix_errors(user_prompt=prompt, current_files=current_files, error_logs=build_logs)
            )
            
            # Save and update workspace files
            current_files = repaired_files
            runner.write_project_files(project_id, current_files)
            state_manager.save_generated_files(project_id, current_files)

    if not build_success:
        logger.warning(f"Debug loop reached max retries ({max_retries}) for project {project_id}")
        state_manager.update_task_status(project_id, task_key, TaskStatus.FAILED)
        state_manager.publish_event(
            project_id=project_id,
            agent_role=AgentRole.DEBUG,
            task_id=task_key,
            event_type="error",
            message="Build verification completed with warnings/retry cap."
        )

    preview_url = f"/api/v1/projects/{project_id}/preview"
    state_manager.update_task_status(project_id, task_key, TaskStatus.SUCCESS, output={"build_logs": build_logs})
    state_manager.publish_event(
        project_id=project_id,
        agent_role=AgentRole.DEBUG,
        task_id=task_key,
        event_type="task_completed",
        message="Sandbox build verification complete. Container preview image ready.",
        data={"preview_url": preview_url}
    )

    # Next step: Dispatch Documentation Worker
    from backend.orchestrator.workers.docs_worker import run_docs
    from backend.orchestrator.dispatcher import dispatch_task
    dispatch_task(run_docs, project_id, prompt, "generate_docs")
