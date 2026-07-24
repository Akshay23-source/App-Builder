from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime
from enum import Enum

class ProjectStatus(str, Enum):
    QUEUED = "QUEUED"
    PLANNING = "PLANNING"
    RESEARCHING = "RESEARCHING"
    CODING = "CODING"
    DEBUGGING = "DEBUGGING"
    DOCUMENTING = "DOCUMENTING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class TaskStatus(str, Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"

class AgentRole(str, Enum):
    PLANNER = "planner"
    RESEARCH = "research"
    CODEGEN = "codegen"
    DEBUG = "debug"
    DOCS = "docs"

# CodeGen File Spec
class GeneratedFile(BaseModel):
    path: str
    content: str

class CodeGenOutput(BaseModel):
    files: List[GeneratedFile]

# Task Graph Models
class TaskNode(BaseModel):
    id: str
    name: str
    agent_role: AgentRole
    dependencies: List[str] = []
    metadata: Dict[str, Any] = {}
    status: TaskStatus = TaskStatus.PENDING

class TaskDAG(BaseModel):
    project_id: str
    nodes: List[TaskNode]

# User Schemas
class UserBase(BaseModel):
    email: Optional[str] = None
    phone_number: Optional[str] = None
    firebase_uid: str

class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    id: str
    created_at: datetime
    class Config:
        from_attributes = True

# Project Schemas
class ProjectCreate(BaseModel):
    name: Optional[str] = "Untitled Project"
    prompt: str = Field(..., min_length=5, description="Idea description for website build")

class ProjectResponse(BaseModel):
    id: str
    user_id: str
    name: str
    prompt: str
    status: ProjectStatus
    preview_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    class Config:
        from_attributes = True

class ProjectDetailResponse(ProjectResponse):
    tasks: List[Dict[str, Any]] = []
    logs: List[Dict[str, Any]] = []
    files: List[GeneratedFile] = []

# WebSocket Stream Event
class BuildEvent(BaseModel):
    project_id: str
    agent_role: AgentRole
    task_id: Optional[str] = None
    event_type: str  # "status_update", "log", "task_completed", "error", "file_created"
    message: str
    data: Optional[Dict[str, Any]] = None
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())

# Auth Token Response
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
