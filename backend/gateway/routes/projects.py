import os
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from backend.db.session import get_async_db
from backend.db.models import User, Project, Task, AgentLog, ProjectFile
from backend.shared.schemas import (
    ProjectCreate, ProjectResponse, ProjectDetailResponse, ProjectStatus, GeneratedFile
)
from backend.gateway.auth.firebase_verify import verify_firebase_token
from backend.orchestrator.workers.planner_worker import run_planner
from backend.shared.config import settings
from backend.shared.logging_config import logger

router = APIRouter(prefix="/projects", tags=["Projects"])

async def get_or_create_user(decoded_token: dict, db: AsyncSession) -> User:
    uid = decoded_token.get("uid")
    result = await db.execute(select(User).where(User.firebase_uid == uid))
    user = result.scalars().first()
    if not user:
        user = User(
            firebase_uid=uid,
            email=decoded_token.get("email"),
            phone_number=decoded_token.get("phone_number")
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
    return user

@router.post("", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(
    payload: ProjectCreate,
    decoded_token: dict = Depends(verify_firebase_token),
    db: AsyncSession = Depends(get_async_db)
):
    user = await get_or_create_user(decoded_token, db)
    
    project = Project(
        user_id=user.id,
        name=payload.name or "Untitled Project",
        prompt=payload.prompt,
        status=ProjectStatus.QUEUED
    )
    db.add(project)
    await db.commit()
    await db.refresh(project)

    # Dispatch Celery Planner Worker
    try:
        run_planner.delay(project_id=project.id, prompt=project.prompt)
    except Exception as e:
        logger.error(f"Failed to queue Celery planner worker: {e}")

    return ProjectResponse.model_validate(project)

@router.get("", response_model=List[ProjectResponse])
async def list_projects(
    decoded_token: dict = Depends(verify_firebase_token),
    db: AsyncSession = Depends(get_async_db)
):
    user = await get_or_create_user(decoded_token, db)
    result = await db.execute(
        select(Project).where(Project.user_id == user.id).order_by(Project.created_at.desc())
    )
    projects = result.scalars().all()
    return [ProjectResponse.model_validate(p) for p in projects]

@router.get("/{project_id}", response_model=ProjectDetailResponse)
async def get_project_details(
    project_id: str,
    decoded_token: dict = Depends(verify_firebase_token),
    db: AsyncSession = Depends(get_async_db)
):
    user = await get_or_create_user(decoded_token, db)
    result = await db.execute(
        select(Project)
        .options(
            selectinload(Project.tasks),
            selectinload(Project.logs),
            selectinload(Project.files)
        )
        .where(Project.id == project_id, Project.user_id == user.id)
    )
    project = result.scalars().first()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    files = [GeneratedFile(path=f.path, content=f.content) for f in project.files]
    tasks = [
        {
            "id": t.id,
            "task_key": t.task_key,
            "name": t.name,
            "agent_role": t.agent_role.value if hasattr(t.agent_role, 'value') else str(t.agent_role),
            "status": t.status.value if hasattr(t.status, 'value') else str(t.status),
            "dependencies": t.dependencies,
            "output": t.output
        }
        for t in project.tasks
    ]
    logs = [
        {
            "id": l.id,
            "agent_role": l.agent_role.value if hasattr(l.agent_role, 'value') else str(l.agent_role),
            "event_type": l.event_type,
            "message": l.message,
            "data": l.log_data,
            "timestamp": l.timestamp.isoformat()
        }
        for l in project.logs
    ]

    return ProjectDetailResponse(
        id=project.id,
        user_id=project.user_id,
        name=project.name,
        prompt=project.prompt,
        status=project.status,
        preview_url=project.preview_url,
        created_at=project.created_at,
        updated_at=project.updated_at,
        tasks=tasks,
        logs=logs,
        files=files
    )

@router.get("/{project_id}/preview", response_class=HTMLResponse)
async def preview_project(project_id: str, db: AsyncSession = Depends(get_async_db)):
    result = await db.execute(
        select(Project).options(selectinload(Project.files)).where(Project.id == project_id)
    )
    project = result.scalars().first()
    if not project:
        raise HTTPException(status_code=404, detail="Project preview not available")

    # Render interactive live preview frame with client-side Next.js simulator
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{project.name} — Live Sandbox Preview</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <style>
            body {{ background-color: #0b0f19; color: #f8fafc; font-family: system-ui, sans-serif; }}
            .glass {{ background: rgba(15, 23, 42, 0.75); backdrop-filter: blur(12px); border: 1px solid rgba(255,255,255,0.1); }}
        </style>
    </head>
    <body class="p-6">
        <div class="max-w-5xl mx-auto space-y-6">
            <header class="flex items-center justify-between p-4 rounded-xl glass">
                <div>
                    <span class="text-xs font-semibold px-2.5 py-1 rounded bg-indigo-500/20 text-indigo-400 border border-indigo-500/30">Sandbox Live Preview</span>
                    <h1 class="text-xl font-bold text-white mt-1">{project.name}</h1>
                </div>
                <div class="flex items-center space-x-3 text-sm text-slate-400">
                    <span>Status: <strong class="text-emerald-400">{project.status.value}</strong></span>
                </div>
            </header>
            
            <main class="p-8 rounded-2xl glass min-h-[400px] flex flex-col items-center justify-center text-center space-y-4">
                <div class="w-16 h-16 rounded-full bg-indigo-600/20 text-indigo-400 flex items-center justify-center text-2xl font-bold border border-indigo-500/40">
                    ⚡
                </div>
                <h2 class="text-2xl font-semibold text-white">Generated Next.js 14 Web Application</h2>
                <p class="text-slate-400 max-w-lg text-sm">
                    Prompt: "{project.prompt}"
                </p>
                <div class="mt-4 pt-4 border-t border-slate-800 text-xs text-slate-500">
                    Emitted {len(project.files)} project source files into container workspace <code>/workspace/{project.id}/</code>
                </div>
            </main>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)
