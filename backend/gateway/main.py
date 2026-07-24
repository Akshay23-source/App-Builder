from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.shared.config import settings
from backend.shared.logging_config import logger
from backend.db.session import sync_engine
from backend.db.models import Base
from backend.gateway.middleware.rate_limit import RateLimitMiddleware
from backend.gateway.routes import users, projects, build_stream

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Initializing database tables...")
    try:
        Base.metadata.create_all(bind=sync_engine)
        logger.info("Database tables initialized successfully.")
    except Exception as e:
        logger.error(f"Error creating database tables: {e}")
    yield

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Multi-Agent AI Website Builder Gateway API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# CORS Setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rate Limiter Setup
app.add_middleware(RateLimitMiddleware, max_requests=120, window_seconds=60)

# Mount Routers
app.include_router(users.router, prefix=settings.API_V1_STR)
app.include_router(projects.router, prefix=settings.API_V1_STR)
app.include_router(build_stream.router)

@app.get("/health")
async def health_check():
    return {
        "status": "online",
        "service": "ForgeAI API Gateway",
        "version": "1.0.0"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.gateway.main:app", host="0.0.0.0", port=8000, reload=True)
