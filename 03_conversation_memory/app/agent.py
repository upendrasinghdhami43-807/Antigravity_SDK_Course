import json
import ast
from google import genai
from typing import Dict, Any

from app.config import GEMINI_API_KEY
from app.prompts import SUMMARIZATION_PROMPT, FACT_EXTRACTION_PROMPT
from app.logger import get_logger

logger = get_logger("Agent")

def _clean_error(e: Exception) -> str:
    err_str = str(e)
    msg = err_str
    try:
        if "{" in err_str:
            start_idx = err_str.index("{")
            dict_str = err_str[start_idx:]
            err_dict = ast.literal_eval(dict_str)
            if 'error' in err_dict and 'message' in err_dict['error']:
                msg = err_dict['error']['message']
    except Exception:
        pass
        
    # Analyze the message for specific friendly output
    if "403" in err_str or "Permission Denied" in msg or "not enabled" in msg.lower():
        return "❌ Access Denied: This might be a paid model, or your API key doesn't have permission for it."
    elif "429" in err_str or "Quota Exceeded" in msg or "RESOURCE_EXHAUSTED" in err_str:
        return "⏳ Quota Exceeded: You have reached your rate limit. Please wait a bit and try again."
    elif "404" in err_str or "Not Found" in msg:
        return "⚠️ Model Not Found: This model doesn't exist or is no longer available to new users."
    elif "ConnectionError" in err_str or "Timeout" in err_str:
        return "🌐 Network Error: Please check your internet connection."
    elif "API_KEY_INVALID" in err_str:
        return "🔑 API Configuration Error: Your API key is invalid."
        
    return msg

import time

class Agent:
    def __init__(self, client, model_mgr):
        self.client = client
        self.model_mgr = model_mgr
        self.fast_model_name = 'gemini-2.0-flash-lite'

    def generate_response(self, prompt: str) -> tuple[str, float]:
        if not self.client:
            return "Error: Gemini API key is not configured.", 0.0
        try:
            start_time = time.time()
            response = self.client.models.generate_content(
                model=self.model_mgr.get_current_model(),
                contents=prompt
            )
            elapsed = time.time() - start_time
            return response.text.strip(), round(elapsed, 2)
        except Exception as e:
            clean_msg = _clean_error(e)
            logger.error(f"Error generating response: {clean_msg}")
            return f"Error: {clean_msg}", 0.0



    def extract_facts(self, user_input: str, assistant_response: str) -> Dict[str, Any]:
        """Uses a faster model to extract facts from the conversation turn."""
        if not self.client:
            return {}
        
        prompt = FACT_EXTRACTION_PROMPT.format(
            user_input=user_input,
            assistant_response=assistant_response
        )
        try:
            response = self.client.models.generate_content(
                model=self.model_mgr.get_current_model(),
                contents=prompt
            )
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
            clean_msg = _clean_error(e)
            logger.error(f"Error extracting facts: {clean_msg}")
            return {}

    def summarize_history(self, history_text: str) -> str:
        """Uses the model to summarize conversation history."""
        if not self.client:
            return ""
        
        prompt = SUMMARIZATION_PROMPT.format(history=history_text)
        try:
            response = self.client.models.generate_content(
                model=self.model_mgr.get_current_model(),
                contents=prompt
            )
            return response.text.strip()
        except Exception as e:
            clean_msg = _clean_error(e)
            logger.error(f"Error summarizing history: {clean_msg}")
            return ""
