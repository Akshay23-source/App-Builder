import asyncio
import concurrent.futures
from typing import TypeVar

T = TypeVar("T")

def run_async(coro) -> T:
    """
    Safely executes an async coroutine from either sync or async context
    without throwing 'asyncio.run() cannot be called from a running event loop'.
    """
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = None

    if loop and loop.is_running():
        with concurrent.futures.ThreadPoolExecutor() as pool:
            return pool.submit(asyncio.run, coro).result()
    else:
        return asyncio.run(coro)
