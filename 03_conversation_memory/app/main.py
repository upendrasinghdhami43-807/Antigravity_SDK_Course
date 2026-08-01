from app.logger import get_logger
from app.chat import ChatEngine
from app.config import GEMINI_API_KEY
from google import genai
import sys

def main():
    logger = get_logger("Main")
    
    if not GEMINI_API_KEY:
        print("CRITICAL: GEMINI_API_KEY is missing from .env file.", file=sys.stderr)
        sys.exit(1)

    try:
        # Initialize the single client instance to pass around
        client = genai.Client(api_key=GEMINI_API_KEY)
        
        chat_engine = ChatEngine(client)
        chat_engine.run()
    except Exception as e:
        logger.critical(f"Application failed to start: {e}")
        print(f"Failed to start: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
