import threading
from backend.shared.logging_config import logger

def dispatch_task(task_func, *args, **kwargs):
    """
    Dispatches orchestrator tasks.
    Tries Celery first (if active). If Celery/Redis is unavailable,
    executes task in a non-blocking background thread.
    """
    celery_dispatched = False
    if hasattr(task_func, "delay"):
        try:
            task_func.delay(*args, **kwargs)
            celery_dispatched = True
            logger.info(f"Dispatched task '{getattr(task_func, '__name__', 'worker')}' via Celery.")
        except Exception as e:
            logger.info(f"Celery unavailable ({e}). Falling back to local background thread execution.")

    if not celery_dispatched:
        target_fn = getattr(task_func, "run", task_func)
        t = threading.Thread(target=target_fn, args=args, kwargs=kwargs, daemon=True)
        t.start()
        logger.info(f"Dispatched task '{getattr(target_fn, '__name__', 'worker')}' in background thread.")
