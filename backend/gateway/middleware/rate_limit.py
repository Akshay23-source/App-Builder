import time
import redis
from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from backend.shared.config import settings
from backend.shared.logging_config import logger

class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, max_requests: int = 120, window_seconds: int = 60):
        super().__init__(app)
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.redis_client = None
        self._redis_failed = False

        try:
            client = redis.Redis.from_url(
                settings.REDIS_URL,
                decode_responses=True,
                socket_connect_timeout=0.2,
                socket_timeout=0.2
            )
            client.ping()
            self.redis_client = client
        except Exception:
            self._redis_failed = True
            logger.info("Redis rate limiter disabled. Operating in fast local non-blocking mode.")

    async def dispatch(self, request: Request, call_next):
        # Skip health check & static endpoints
        if request.url.path in ["/health", "/docs", "/openapi.json", "/redoc"] or request.url.path.startswith("/ws/"):
            return await call_next(request)

        client_ip = request.client.host if request.client else "127.0.0.1"
        key = f"rate_limit:{client_ip}"

        if self.redis_client and not self._redis_failed:
            try:
                current = self.redis_client.get(key)
                if current and int(current) >= self.max_requests:
                    raise HTTPException(
                        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                        detail="Rate limit exceeded. Please try again shortly."
                    )
                pipeline = self.redis_client.pipeline()
                pipeline.incr(key)
                pipeline.expire(key, self.window_seconds)
                pipeline.execute()
            except HTTPException as he:
                raise he
            except Exception:
                self._redis_failed = True

        response = await call_next(request)
        return response
