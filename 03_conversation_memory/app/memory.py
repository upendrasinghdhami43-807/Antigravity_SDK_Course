from typing import Dict, Any
from app.config import MEMORY_FILE
from app.utils import load_json, save_json
from app.logger import get_logger

logger = get_logger("MemoryManager")

class MemoryManager:
    def __init__(self):
        self.facts: Dict[str, Any] = {}
        self.load_memory()

    def load_memory(self):
        self.facts = load_json(MEMORY_FILE, default={})
        logger.debug(f"Loaded {len(self.facts)} memory facts.")

    def save_memory(self):
        save_json(MEMORY_FILE, self.facts)
        logger.debug("Saved memory to file.")

    def update_facts(self, new_facts: Dict[str, Any]):
        if new_facts:
            self.facts.update(new_facts)
            self.save_memory()
            logger.info(f"Updated memory with new facts: {list(new_facts.keys())}")

    def get_memory_string(self) -> str:
        if not self.facts:
            return "No specific facts known yet."
        return "\n".join([f"- {k}: {v}" for k, v in self.facts.items()])

    def clear_memory(self):
        self.facts = {}
        self.save_memory()
        logger.info("Memory cleared.")
