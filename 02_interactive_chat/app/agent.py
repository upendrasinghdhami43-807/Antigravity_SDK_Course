from google import genai
from google.genai import errors
from app.config import API_KEY, MODEL
from app.prompts import SYSTEM_PROMPT

class Agent:
    def __init__(self):
        if not API_KEY:
            raise ValueError("API Key is missing. Please set GEMINI_API_KEY in .env")
        self.client = genai.Client(api_key=API_KEY)
        self.current_model = MODEL
        self.reset()
        
    def reset(self):
        self.chat_session = self.client.chats.create(
            model=self.current_model,
            config={"system_instruction": SYSTEM_PROMPT}
        )
        
    def get_categorized_models(self):
        categories = {
            "Chat Models": [],
            "Image Models": [],
            "Other Models": []
        }
        for m in self.client.models.list():
            name = m.name.replace("models/", "")
            if "gemini" not in name:
                continue
            
            if "image" in name or "vision" in name:
                categories["Image Models"].append(name)
            elif any(x in name for x in ["tts", "audio", "embedding", "robotics", "computer-use", "translate", "live"]):
                categories["Other Models"].append(name)
            else:
                categories["Chat Models"].append(name)
                
        return categories
        
    def change_model(self, new_model: str):
        self.current_model = new_model
        self.reset()
        
    def ask(self, prompt: str) -> str:
        try:
            response = self.chat_session.send_message(prompt)
            return response.text
        except errors.APIError as e:
            return f"API Error: {str(e)}"
        except Exception as e:
            return f"An unexpected error occurred: {str(e)}"
