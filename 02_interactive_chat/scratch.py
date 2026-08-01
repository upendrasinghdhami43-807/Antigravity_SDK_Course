import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=API_KEY)
for m in client.models.list():
    if "gemini" in m.name and "vision" not in m.name:
        print(m.name)
