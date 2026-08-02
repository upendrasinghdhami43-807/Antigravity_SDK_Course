class PromptFormatter:
    """Final formatting pass for the prompt before sending to the model."""
    
    def format(self, prompt: str) -> str:
        # Strip trailing whitespaces, ensure proper newlines
        lines = [line.rstrip() for line in prompt.split('\n')]
        return '\n'.join(lines).strip()
