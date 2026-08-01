from google import genai
from app.config import API_KEY, MODEL

client = genai.Client(api_key=API_KEY)

def ask(prompt):
    response = client.models.generate_content(
        model=MODEL,
        contents=prompt
    )
    return response.text
