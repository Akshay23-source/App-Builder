import os
import sys
import uuid
from datetime import datetime

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from backend.db.session import SyncSessionLocal, sync_engine
from backend.db.models import Base, User, Project, Task, AgentLog, ProjectFile
from backend.shared.schemas import ProjectStatus, TaskStatus, AgentRole

def seed():
    print("Initializing database tables...")
    Base.metadata.create_all(bind=sync_engine)
    
    db = SyncSessionLocal()
    try:
        print("Seeding demo project data into database...")
        user = db.query(User).filter(User.firebase_uid == "demo_user_1").first()
        if not user:
            user = User(
                id=str(uuid.uuid4()),
                firebase_uid="demo_user_1",
                email="demo@forgeai.dev",
                phone_number="+15550192834"
            )
            db.add(user)
            db.commit()
            db.refresh(user)

        project = Project(
            id="demo-proj-1",
            user_id=user.id,
            name="AI SaaS Video Platform",
            prompt="A SaaS landing page for an AI video editor with pricing tables and dark glassmorphic hero",
            status=ProjectStatus.COMPLETED,
            preview_url="/dashboard/demo-proj-1/preview"
        )
        db.merge(project)

        # Seed sample files
        sample_file = ProjectFile(
            project_id=project.id,
            path="src/app/page.tsx",
            content="export default function Page() { return <h1>AI Video Editor</h1>; }"
        )
        db.add(sample_file)

        db.commit()
        print("Successfully seeded demo project!")
    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed()
