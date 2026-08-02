import json
import os
from typing import Dict, Any

class MemoryManager:
    """Manages long-term facts/preferences about the user."""
    def __init__(self, data_file: str = "data/memory.json"):
        self.data_file = data_file
        self.memory: Dict[str, Any] = {}
        self._load()

    def _load(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    self.memory = json.load(f)
            except json.JSONDecodeError:
                self.memory = {}
        else:
            self.memory = {}
            self._save()

    def _save(self):
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        with open(self.data_file, 'w') as f:
            json.dump(self.memory, f, indent=2)

    def get_memory(self) -> Dict[str, Any]:
        return self.memory

    def update_memory(self, new_facts: Dict[str, Any]):
        """Merge new facts into existing memory."""
        # Simple merge for Phase 2
        for key, value in new_facts.items():
            if isinstance(value, list) and key in self.memory and isinstance(self.memory[key], list):
                self.memory[key].extend(value)
                self.memory[key] = list(set(self.memory[key])) # Deduplicate
            elif isinstance(value, dict) and key in self.memory and isinstance(self.memory[key], dict):
                self.memory[key].update(value)
            else:
                self.memory[key] = value
        self._save()
        
    def clear(self):
        self.memory = {}
        self._save()
