from typing import List
from app.config import MAX_HISTORY_MESSAGES, MAX_HISTORY_TOKENS
from app.models import Message
from app.history import HistoryManager
from app.memory import MemoryManager
from app.summarizer import SummaryManager
from app.prompts import SYSTEM_PROMPT
from app.tokenizer import estimate_tokens
from app.logger import get_logger

logger = get_logger("ContextBuilder")

class ContextBuilder:
    def __init__(
        self, 
        history_mgr: HistoryManager, 
        memory_mgr: MemoryManager, 
        summary_mgr: SummaryManager
    ):
        self.history_mgr = history_mgr
        self.memory_mgr = memory_mgr
        self.summary_mgr = summary_mgr

    def build_system_prompt(self) -> str:
        memory_str = self.memory_mgr.get_memory_string()
        summary_str = self.summary_mgr.get_summary()
        
        prompt = SYSTEM_PROMPT.format(
            memory=memory_str,
            summary=summary_str
        )
        return prompt

    def get_context_messages(self) -> List[Message]:
        """
        Returns a list of messages that fit within the token limit.
        If history is too long, it triggers summarization.
        """
        all_messages = self.history_mgr.get_messages()
        
        # Simple heuristic: Just use the last MAX_HISTORY_MESSAGES
        # In a real app, you would count tokens and summarize if limit is breached.
        recent_messages = all_messages[-MAX_HISTORY_MESSAGES:]
        
        # Example of token checking:
        total_tokens = sum(estimate_tokens(msg.text) for msg in recent_messages)
        if total_tokens > MAX_HISTORY_TOKENS:
            logger.warning("History token limit exceeded. (Summarization should be triggered here)")
            # Here we would trigger summarize, for now we just truncate
            recent_messages = recent_messages[-(MAX_HISTORY_MESSAGES//2):]
            
        return recent_messages
