import time
from backend.shared.logging_config import logger
from backend.db.session import sync_engine
from backend.db.models import Base

def main():
    logger.info("Initializing Orchestrator database tables...")
    try:
        Base.metadata.create_all(bind=sync_engine)
        logger.info("Database tables initialized successfully.")
    except Exception as e:
        logger.error(f"Error initializing DB tables: {e}")

    logger.info("ForgeAI Orchestrator Service is active and monitoring tasks.")
    while True:
        time.sleep(10)

if __name__ == "__main__":
    main()
