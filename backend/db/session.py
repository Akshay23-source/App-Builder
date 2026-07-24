from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.shared.config import settings
from backend.shared.logging_config import logger

db_url_sync = settings.DATABASE_URL_SYNC

if db_url_sync.startswith("sqlite"):
    sync_engine = create_engine(
        db_url_sync,
        echo=False,
        connect_args={"check_same_thread": False}
    )
else:
    sync_engine = create_engine(
        db_url_sync,
        echo=False,
        pool_pre_ping=True
    )

SyncSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=sync_engine
)

class DirectAsyncSession:
    """
    Lightweight async wrapper around SQLAlchemy sync session.
    Prevents greenlet DLL compilation issues on Python 3.14 Windows environment.
    """
    def __init__(self, sync_session):
        self.sync_session = sync_session

    async def execute(self, statement, params=None):
        return self.sync_session.execute(statement, params)

    def add(self, instance):
        self.sync_session.add(instance)

    def delete(self, instance):
        self.sync_session.delete(instance)

    async def commit(self):
        self.sync_session.commit()

    async def refresh(self, instance):
        self.sync_session.refresh(instance)

    async def close(self):
        self.sync_session.close()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.sync_session.rollback()
        self.sync_session.close()

def AsyncSessionLocal():
    return DirectAsyncSession(SyncSessionLocal())

async def get_async_db():
    session = DirectAsyncSession(SyncSessionLocal())
    try:
        yield session
    finally:
        await session.close()

def get_sync_db():
    db = SyncSessionLocal()
    try:
        yield db
    finally:
        db.close()
