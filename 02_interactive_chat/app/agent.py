from google import genai
from google.genai import errors
from app.config import API_KEY, MODEL
from app.prompts import SYSTEM_PROMPT

class Agent:
    def __init__(self):
        if not API_KEY:
            raise ValueError("API Key is missing. Please set GEMINI_API_KEY in .env")
        self.client = genai.Client(api_key=API_KEY)
        self.chat_session = self.client.chats.create(
            model=MODEL,
            config={"system_instruction": SYSTEM_PROMPT}
        )
        
    def ask(self, prompt: str) -> str:
        try:
            response = self.chat_session.send_message(prompt)
            return response.text
        except errors.APIError as e:
            return f"API Error: {str(e)}"
        except Exception as e:
            return f"An unexpected error occurred: {str(e)}"
