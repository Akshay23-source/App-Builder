from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from backend.shared.config import settings

# Async Engine for FastAPI Gateway
async_engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False,
    future=True
)

AsyncSessionLocal = sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Sync Engine for Celery Workers
sync_engine = create_engine(
    settings.DATABASE_URL_SYNC,
    echo=False,
    pool_pre_ping=True
)

SyncSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=sync_engine
)

async def get_async_db():
    async with AsyncSessionLocal() as session:
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
