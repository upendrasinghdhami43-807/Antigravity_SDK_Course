from typing import Optional

class PersonaManager:
    """Manages the active persona (e.g., Python Teacher, Code Reviewer)."""
    def __init__(self):
        self.active_persona: Optional[str] = None
        
    def set_persona(self, persona_name: str):
        self.active_persona = persona_name

    def get_persona(self) -> Optional[str]:
        return self.active_persona
