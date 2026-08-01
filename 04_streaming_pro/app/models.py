from dataclasses import dataclass
from typing import List, Dict, Any

@dataclass
class Message:
    role: str
    text: str

    def to_dict(self) -> Dict[str, str]:
        return {"role": self.role, "text": self.text}
    
    @classmethod
    def from_dict(cls, data: Dict[str, str]) -> 'Message':
        return cls(role=data.get("role", ""), text=data.get("text", ""))

@dataclass
class Session:
    session_id: str
    start_time: str
    message_count: int
    duration_seconds: int

    def to_dict(self) -> Dict[str, Any]:
        return {
            "session_id": self.session_id,
            "start_time": self.start_time,
            "message_count": self.message_count,
            "duration_seconds": self.duration_seconds
        }
