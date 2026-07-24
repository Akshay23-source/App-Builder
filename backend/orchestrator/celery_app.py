from celery import Celery
from backend.shared.config import settings

celery_app = Celery(
    "forgeai_orchestrator",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=[
        "backend.orchestrator.workers.planner_worker",
        "backend.orchestrator.workers.research_worker",
        "backend.orchestrator.workers.codegen_worker",
        "backend.orchestrator.workers.debug_worker",
        "backend.orchestrator.workers.docs_worker",
    ]
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
)
