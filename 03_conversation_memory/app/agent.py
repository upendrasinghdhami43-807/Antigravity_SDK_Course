import json
import google.generativeai as genai
from typing import Dict, Any

from app.config import GEMINI_API_KEY
from app.prompts import SUMMARIZATION_PROMPT, FACT_EXTRACTION_PROMPT
from app.logger import get_logger

logger = get_logger("Agent")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

class Agent:
    def __init__(self):
        # Initialize Gemini Model
        if GEMINI_API_KEY:
            self.model = genai.GenerativeModel('gemini-1.5-pro')
            self.fast_model = genai.GenerativeModel('gemini-1.5-flash')
        else:
            logger.warning("No API key provided. Agent will not work properly.")
            self.model = None
            self.fast_model = None

    def generate_response(self, prompt: str) -> str:
        if not self.model:
            return "Error: Gemini API key is not configured."
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return f"Error: {e}"

    def extract_facts(self, user_input: str, assistant_response: str) -> Dict[str, Any]:
        """Uses a faster model to extract facts from the conversation turn."""
        if not self.fast_model:
            return {}
        
        prompt = FACT_EXTRACTION_PROMPT.format(
            user_input=user_input,
            assistant_response=assistant_response
        )
        try:
            response = self.fast_model.generate_content(prompt)
            result_text = response.text.strip()
            
            if result_text == "NONE" or result_text.startswith("NONE"):
                return {}
            
            # Clean up potential markdown formatting in JSON response
            if "```json" in result_text:
                result_text = result_text.split("```json")[1].split("```")[0].strip()
            elif "```" in result_text:
                result_text = result_text.split("```")[1].split("```")[0].strip()
                
            return json.loads(result_text)
        except json.JSONDecodeError:
            logger.warning(f"Failed to parse extracted facts JSON: {result_text}")
            return {}
        except Exception as e:
            logger.error(f"Error extracting facts: {e}")
            return {}

    def summarize_history(self, history_text: str) -> str:
        """Uses the model to summarize conversation history."""
        if not self.fast_model:
            return ""
        
        prompt = SUMMARIZATION_PROMPT.format(history=history_text)
        try:
            response = self.fast_model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            logger.error(f"Error summarizing history: {e}")
            return ""
