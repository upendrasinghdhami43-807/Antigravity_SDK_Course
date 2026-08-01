from app.chat import ChatManager
from app.logger import get_logger

logger = get_logger("Main")

def main():
    logger.info("Starting Application...")
    
    try:
        chat_manager = ChatManager()
        chat_manager.chat_loop()
    except Exception as e:
        logger.critical(f"Application failed to start: {e}")

if __name__ == "__main__":
    main()
