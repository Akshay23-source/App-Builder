import asyncio
import json
import redis.asyncio as aioredis
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from backend.shared.config import settings
from backend.shared.logging_config import logger

router = APIRouter(tags=["WebSocket Stream"])

@router.websocket("/ws/build/{project_id}")
async def websocket_build_stream(websocket: WebSocket, project_id: str):
    await websocket.accept()
    logger.info(f"WebSocket client connected for project build stream: {project_id}")
    
    redis_pubsub = None
    try:
        r = aioredis.from_url(settings.REDIS_URL, decode_responses=True)
        redis_pubsub = r.pubsub()
        channel_name = f"project:{project_id}:stream"
        await redis_pubsub.subscribe(channel_name)
        logger.info(f"Subscribed WebSocket to Redis channel [{channel_name}]")

        while True:
            # Check for Redis messages non-blocking
            message = await redis_pubsub.get_message(ignore_subscribe_messages=True, timeout=1.0)
            if message and message["type"] == "message":
                data = message["data"]
                await websocket.send_text(data)

            # Heartbeat ping to keep socket alive
            await asyncio.sleep(0.1)

    except WebSocketDisconnect:
        logger.info(f"WebSocket client disconnected for project {project_id}")
    except Exception as e:
        logger.error(f"WebSocket streaming error for project {project_id}: {e}")
    finally:
        if redis_pubsub:
            await redis_pubsub.unsubscribe()
            await redis_pubsub.close()
