import json
import redis
from datetime import datetime
from typing import Dict, Any, Optional
from backend.shared.config import settings
from backend.shared.schemas import ProjectStatus, TaskStatus, AgentRole, BuildEvent
from backend.shared.logging_config import logger
from backend.db.session import SyncSessionLocal
from backend.db.models import Project, Task, AgentLog, ProjectFile

class StateManager:
    def __init__(self):
        self.redis_client = redis.Redis.from_url(settings.REDIS_URL, decode_responses=True)

    def publish_event(
        self,
        project_id: str,
        agent_role: AgentRole,
        event_type: str,
        message: str,
        data: Optional[Dict[str, Any]] = None,
        task_id: Optional[str] = None
    ):
        event = BuildEvent(
            project_id=project_id,
            agent_role=agent_role,
            task_id=task_id,
            event_type=event_type,
            message=message,
            data=data
        )

        # 1. Publish to Redis channel for live WebSocket broadcast
        channel = f"project:{project_id}:stream"
        payload = event.model_dump_json()
        self.redis_client.publish(channel, payload)
        logger.info(f"Published state event to [{channel}]: {message}")

        # 2. Persist AgentLog in Postgres DB
        db = SyncSessionLocal()
        try:
            log_entry = AgentLog(
                project_id=project_id,
                agent_role=agent_role.value if isinstance(agent_role, AgentRole) else str(agent_role),
                event_type=event_type,
                message=message,
                log_data=data
            )
            db.add(log_entry)
            db.commit()
        except Exception as e:
            db.rollback()
            logger.error(f"Failed to persist agent log to DB: {e}")
        finally:
            db.close()

    def update_project_status(self, project_id: str, status: ProjectStatus, preview_url: Optional[str] = None):
        db = SyncSessionLocal()
        try:
            proj = db.query(Project).filter(Project.id == project_id).first()
            if proj:
                proj.status = status
                if preview_url:
                    proj.preview_url = preview_url
                db.commit()
        except Exception as e:
            db.rollback()
            logger.error(f"Failed to update project status: {e}")
        finally:
            db.close()

    def update_task_status(
        self,
        project_id: str,
        task_key: str,
        status: TaskStatus,
        output: Optional[Dict[str, Any]] = None
    ):
        db = SyncSessionLocal()
        try:
            task = db.query(Task).filter(
                Task.project_id == project_id,
                Task.task_key == task_key
            ).first()
            if task:
                task.status = status
                if output:
                    task.output = output
                db.commit()
        except Exception as e:
            db.rollback()
            logger.error(f"Failed to update task status: {e}")
        finally:
            db.close()

    def save_generated_files(self, project_id: str, files: list):
        db = SyncSessionLocal()
        try:
            # Clear old files for this project if repairing
            db.query(ProjectFile).filter(ProjectFile.project_id == project_id).delete()
            for f in files:
                pf = ProjectFile(
                    project_id=project_id,
                    path=f.path if hasattr(f, 'path') else f['path'],
                    content=f.content if hasattr(f, 'content') else f['content']
                )
                db.add(pf)
            db.commit()
        except Exception as e:
            db.rollback()
            logger.error(f"Failed to save project files to DB: {e}")
        finally:
            db.close()

state_manager = StateManager()
