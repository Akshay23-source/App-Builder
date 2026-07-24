import asyncio
from backend.orchestrator.celery_app import celery_app
from backend.shared.schemas import AgentRole, ProjectStatus, TaskStatus
from backend.orchestrator.state_manager import state_manager
from backend.agents.planner_agent import PlannerAgent
from backend.db.session import SyncSessionLocal
from backend.db.models import Project, Task
from backend.shared.logging_config import logger

@celery_app.task(name="planner_worker.execute")
def run_planner(project_id: str, prompt: str):
    logger.info(f"[PlannerWorker] Starting planning phase for project {project_id}")
    state_manager.update_project_status(project_id, ProjectStatus.PLANNING)
    state_manager.publish_event(
        project_id=project_id,
        agent_role=AgentRole.PLANNER,
        event_type="status_update",
        message="Planner Agent is breaking down your idea into a task graph..."
    )

    planner = PlannerAgent()
    dag = asyncio.run(planner.plan(project_id=project_id, user_prompt=prompt))

    # Persist DAG task nodes to DB
    db = SyncSessionLocal()
    try:
        for node in dag.nodes:
            db_task = Task(
                project_id=project_id,
                task_key=node.id,
                name=node.name,
                agent_role=node.agent_role,
                status=TaskStatus.PENDING,
                dependencies=node.dependencies,
                task_metadata=node.metadata
            )
            db.add(db_task)
        db.commit()
    except Exception as e:
        db.rollback()
        logger.error(f"Error persisting DAG tasks: {e}")
        state_manager.update_project_status(project_id, ProjectStatus.FAILED)
        return
    finally:
        db.close()

    state_manager.publish_event(
        project_id=project_id,
        agent_role=AgentRole.PLANNER,
        event_type="task_completed",
        message=f"Planner generated DAG with {len(dag.nodes)} execution stages.",
        data={"dag": dag.model_dump()}
    )

    # Dispatch initial ready tasks (Research worker)
    from backend.orchestrator.workers.research_worker import run_research
    run_research.delay(project_id, prompt, "research_design")
