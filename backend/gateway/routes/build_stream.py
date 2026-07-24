import asyncio
import json
import redis.asyncio as aioredis
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from backend.shared.config import settings
from backend.shared.logging_config import logger
from backend.orchestrator.state_manager import broadcaster

router = APIRouter(tags=["WebSocket Stream"])

@router.websocket("/ws/build/{project_id}")
async def websocket_build_stream(websocket: WebSocket, project_id: str):
    await websocket.accept()
    logger.info(f"WebSocket client connected for project build stream: {project_id}")
    
    channel_name = f"project:{project_id}:stream"
    in_mem_queue = broadcaster.subscribe(channel_name)

    redis_pubsub = None
    try:
        r = aioredis.from_url(settings.REDIS_URL, decode_responses=True)
        redis_pubsub = r.pubsub()
        await redis_pubsub.subscribe(channel_name)
        logger.info(f"Subscribed WebSocket to Redis channel [{channel_name}]")
    except Exception as e:
        logger.info(f"Redis pubsub connection bypassed ({e}). Using local in-memory stream for project {project_id}")

    try:
        while True:
            # 1. Drain in-memory events if any
            while not in_mem_queue.empty():
                payload = in_mem_queue.get_nowait()
                await websocket.send_text(payload)

            # 2. Check for Redis messages if pubsub active
            if redis_pubsub:
                try:
                    message = await redis_pubsub.get_message(ignore_subscribe_messages=True, timeout=0.1)
                    if message and message["type"] == "message":
                        await websocket.send_text(message["data"])
                except Exception:
                    pass

            await asyncio.sleep(0.1)

    except WebSocketDisconnect:
        logger.info(f"WebSocket client disconnected for project {project_id}")
    except Exception as e:
        logger.error(f"WebSocket streaming error for project {project_id}: {e}")
    finally:
        broadcaster.unsubscribe(channel_name, in_mem_queue)
        if redis_pubsub:
            try:
                await redis_pubsub.unsubscribe()
                await redis_pubsub.close()
            except Exception:
                pass
