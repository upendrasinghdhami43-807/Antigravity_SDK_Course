from typing import Dict, Any
from datetime import datetime
import re

class VariableManager:
    """Manages variables injected into prompt templates (e.g., {{USER_NAME}})."""
    def __init__(self):
        import uuid
        self.variables: Dict[str, Any] = {
            "CURRENT_DATE": datetime.now().strftime("%Y-%m-%d"),
            "CURRENT_TIME": datetime.now().strftime("%H:%M:%S"),
            "USER_NAME": "User", # Can be overridden by config/memory
            "CURRENT_MODEL": "gemini-flash-lite-latest", # Default
            "LANGUAGE": "English",
            "SESSION_ID": str(uuid.uuid4()), # Generate a random session ID
        }

    def set_variable(self, key: str, value: Any):
        self.variables[key] = value

    def get_variables(self) -> Dict[str, Any]:
        return self.variables

    def inject_variables(self, text: str) -> str:
        """Replaces {{KEY}} in text with value from variables."""
        if not text:
            return text
            
        def repl(match):
            key = match.group(1)
            return str(self.variables.get(key, f"{{{{{key}}}}}"))

        return re.sub(r'\{\{(.*?)\}\}', repl, text)
