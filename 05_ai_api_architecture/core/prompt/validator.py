from core.exceptions.framework_exceptions import PromptValidationError
import re

class PromptValidator:
    """Validates the assembled prompt."""
    
    def validate(self, prompt: str, max_length: int = 100000):
        if not prompt or not prompt.strip():
            raise PromptValidationError("Prompt is empty.")
            
        if len(prompt) > max_length:
            raise PromptValidationError(f"Prompt length ({len(prompt)}) exceeds max length ({max_length}).")
            
        # Check for unreplaced variables
        unreplaced = re.findall(r'\{\{(.*?)\}\}', prompt)
        if unreplaced:
            # Maybe just warn instead of fail, but for now we'll allow it or just log.
            # In a strict environment, this could raise an error.
            pass
