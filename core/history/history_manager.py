import json
import os
from typing import List, Dict, Any
from core.models.message import Message
from core.exceptions.framework_exceptions import HistoryError

class HistoryManager:
    """Manages full conversation history."""
    def __init__(self, data_file: str = "data/history.json"):
        self.data_file = data_file
        self.history: List[Message] = []
        self._load()

    def _load(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                    self.history = [Message.from_dict(m) for m in data]
            except json.JSONDecodeError:
                self.history = []
        else:
            self.history = []
            self._save()

    def _save(self):
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        with open(self.data_file, 'w') as f:
            json.dump([m.to_dict() for m in self.history], f, indent=2)

    def add_message(self, message: Message):
        self.history.append(message)
        self._save()

    def get_history(self, limit: int = None) -> List[Message]:
        if limit and limit > 0:
            return self.history[-limit:]
        return self.history

    def clear(self):
        self.history = []
        self._save()
