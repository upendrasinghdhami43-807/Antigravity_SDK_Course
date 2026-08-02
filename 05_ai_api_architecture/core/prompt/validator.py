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
            raise PromptValidationError(f"Prompt contains unresolved variables: {unreplaced}")

        # Security: Prevent Prompt Injection
        lower_prompt = prompt.lower()
        forbidden_phrases = [
            "ignore previous instructions",
            "disregard previous instructions",
            "forget previous instructions"
        ]
        for phrase in forbidden_phrases:
            if phrase in lower_prompt:
                raise PromptValidationError("Security Violation: Attempted prompt injection detected.")

