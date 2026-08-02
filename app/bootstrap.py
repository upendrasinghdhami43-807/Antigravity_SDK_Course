from app.application import Application
from core.logger.logger import get_logger

logger = get_logger()

def start():
    """Loads config, builds Application, starts it."""
    try:
        app = Application()
        app.run()
    except Exception as e:
        logger.error(f"Failed to bootstrap application: {e}")
        import traceback
        traceback.print_exc()
