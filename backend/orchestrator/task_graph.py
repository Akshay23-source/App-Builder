from typing import List, Dict, Any
from backend.shared.schemas import TaskDAG, TaskStatus, AgentRole
from backend.shared.logging_config import logger
from backend.db.session import SyncSessionLocal
from backend.db.models import Task

class TaskGraphExecutor:
    """
    Evaluates dependencies in the project Task DAG and triggers ready tasks.
    """
    @staticmethod
    def get_ready_tasks(project_id: str) -> List[Task]:
        db = SyncSessionLocal()
        try:
            all_tasks = db.query(Task).filter(Task.project_id == project_id).all()
            completed_keys = {t.task_key for t in all_tasks if t.status == TaskStatus.SUCCESS}
            
            ready = []
            for t in all_tasks:
                if t.status == TaskStatus.PENDING:
                    deps = t.dependencies or []
                    if all(dep in completed_keys for dep in deps):
                        ready.append(t)
            return ready
        finally:
            db.close()

    @staticmethod
    def is_dag_completed(project_id: str) -> bool:
        db = SyncSessionLocal()
        try:
            all_tasks = db.query(Task).filter(Task.project_id == project_id).all()
            if not all_tasks:
                return False
            return all(t.status == TaskStatus.SUCCESS for t in all_tasks)
        finally:
            db.close()
