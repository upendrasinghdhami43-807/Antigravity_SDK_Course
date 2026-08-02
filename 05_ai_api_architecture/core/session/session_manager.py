import uuid
from datetime import datetime
from typing import Dict, Any

class SessionManager:
    """Manages session state: id, start/end time, token counters."""
    def __init__(self):
        self.session_id = str(uuid.uuid4())
        self.start_time = datetime.now().isoformat()
        self.end_time = None
        self.current_model = None
        self.message_count = 0
        self.total_prompt_tokens = 0
        self.total_completion_tokens = 0
        
    def add_tokens(self, prompt_tokens: int, completion_tokens: int):
        self.total_prompt_tokens += prompt_tokens
        self.total_completion_tokens += completion_tokens
        self.message_count += 1
        
    def end_session(self):
        self.end_time = datetime.now().isoformat()
        
    def to_dict(self) -> Dict[str, Any]:
        return {
            "session_id": self.session_id,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "current_model": self.current_model,
            "message_count": self.message_count,
            "total_prompt_tokens": self.total_prompt_tokens,
            "total_completion_tokens": self.total_completion_tokens
        }
