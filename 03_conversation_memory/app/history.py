from typing import List, Dict
from app.config import HISTORY_FILE
from app.models import Message
from app.utils import load_json, save_json
from app.logger import get_logger

logger = get_logger("HistoryManager")

class HistoryManager:
    def __init__(self):
        self.messages: List[Message] = []
        self.load_history()

    def load_history(self):
        data = load_json(HISTORY_FILE, default=[])
        self.messages = [Message.from_dict(msg) for msg in data]
        logger.debug(f"Loaded {len(self.messages)} messages from history.")

    def save_history(self):
        data = [msg.to_dict() for msg in self.messages]
        save_json(HISTORY_FILE, data)
        logger.debug("Saved history to file.")

    def append_message(self, role: str, text: str):
        msg = Message(role=role, text=text)
        self.messages.append(msg)
        self.save_history()

    def get_messages(self) -> List[Message]:
        return self.messages

    def get_recent_messages(self, count: int) -> List[Message]:
        return self.messages[-count:]

    def clear_history(self):
        self.messages = []
        self.save_history()
        logger.info("History cleared.")

    def replace_history_with_summary(self, summary_msg: Message):
        self.messages = [summary_msg]
        self.save_history()
        logger.info("History replaced with summary.")
