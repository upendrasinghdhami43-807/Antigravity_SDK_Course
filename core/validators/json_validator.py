import json
from typing import Tuple, Optional

class JSONValidator:
    """Validates raw text as JSON, attempts to fix common errors."""
    
    def validate_and_repair(self, text: str) -> Tuple[bool, Optional[dict]]:
        if not text:
            return False, None
            
        # Try to parse directly
        try:
            return True, json.loads(text)
        except json.JSONDecodeError:
            pass
            
        # Try to repair (e.g. strip markdown fences)
        cleaned = text.strip()
        if cleaned.startswith("```json"):
            cleaned = cleaned[7:]
        elif cleaned.startswith("```"):
            cleaned = cleaned[3:]
            
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3]
            
        cleaned = cleaned.strip()
        
        try:
            return True, json.loads(cleaned)
        except json.JSONDecodeError:
            return False, None
