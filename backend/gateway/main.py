from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.shared.config import settings
from backend.shared.logging_config import logger
from backend.gateway.middleware.rate_limit import RateLimitMiddleware
from backend.gateway.routes import users, projects, build_stream

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Multi-Agent AI Website Builder Gateway API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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
