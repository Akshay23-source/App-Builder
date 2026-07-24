import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime, Enum, ForeignKey, JSON
from sqlalchemy.orm import declarative_base, relationship
from backend.shared.schemas import ProjectStatus, TaskStatus, AgentRole

Base = declarative_base()

def generate_uuid():
    return str(uuid.uuid4())

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=generate_uuid)
    firebase_uid = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, nullable=True)
    phone_number = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    projects = relationship("Project", back_populates="user", cascade="all, delete-orphan")

class Project(Base):
    __tablename__ = "projects"

    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    name = Column(String, default="Untitled Project")
    prompt = Column(Text, nullable=False)
    status = Column(Enum(ProjectStatus), default=ProjectStatus.QUEUED)
    preview_url = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="projects")
    tasks = relationship("Task", back_populates="project", cascade="all, delete-orphan")
    logs = relationship("AgentLog", back_populates="project", cascade="all, delete-orphan")
    files = relationship("ProjectFile", back_populates="project", cascade="all, delete-orphan")

class Task(Base):
    __tablename__ = "tasks"

    id = Column(String, primary_key=True, default=generate_uuid)
    project_id = Column(String, ForeignKey("projects.id"), nullable=False)
    task_key = Column(String, nullable=False)  # e.g. "research_design", "generate_code"
    name = Column(String, nullable=False)
    agent_role = Column(Enum(AgentRole), nullable=False)
    status = Column(Enum(TaskStatus), default=TaskStatus.PENDING)
    dependencies = Column(JSON, default=list)  # list of task_keys
    task_metadata = Column(JSON, default=dict)
    output = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    project = relationship("Project", back_populates="tasks")

class AgentLog(Base):
    __tablename__ = "agent_logs"

    id = Column(String, primary_key=True, default=generate_uuid)
    project_id = Column(String, ForeignKey("projects.id"), nullable=False)
    agent_role = Column(Enum(AgentRole), nullable=False)
    event_type = Column(String, nullable=False)  # "status", "thought", "error", "file"
    message = Column(Text, nullable=False)
    log_data = Column(JSON, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)

    project = relationship("Project", back_populates="logs")

class ProjectFile(Base):
    __tablename__ = "project_files"

    id = Column(String, primary_key=True, default=generate_uuid)
    project_id = Column(String, ForeignKey("projects.id"), nullable=False)
    path = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    project = relationship("Project", back_populates="files")
