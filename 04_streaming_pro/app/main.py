import asyncio
import os
from dotenv import load_dotenv
from google import genai
from app.logger import get_logger
from app.chat import ChatEngine

logger = get_logger("Main")

async def main():
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY not found in .env")
        return

    # For streaming, we use the async client interface
    client = genai.Client(api_key=api_key)
    
    chat_engine = ChatEngine(client)
    await chat_engine.run()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        # Catch unexpected forceful exits
        print("\nApplication terminated.")
