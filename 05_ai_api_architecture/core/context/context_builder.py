from dataclasses import dataclass
from typing import List, Dict, Any
from core.models.message import Message

@dataclass
class Context:
    """The merged context object holding everything needed to build a prompt."""
    system_prompt: str
    developer_prompt: str
    persona: str
    memory: Dict[str, Any]
    history: List[Message]
    question: str
    examples: List[Dict[str, str]]

class ContextBuilder:
    """
    Assembles system prompt + history + memory + current question into one Context object.
    Note: Prompts are resolved by Module 06 (Prompt Engine), but ContextBuilder
    provides the raw materials from Memory and History.
    """
    def build_context(self, question: str, memory_data: Dict[str, Any], history_data: List[Message]) -> Context:
        # In Phase 2, system, developer, persona, examples are loaded in Module 06.
        # This builder just structures the data passed from the controller.
        return Context(
            system_prompt="", # To be filled by Prompt Manager
            developer_prompt="", # To be filled by Prompt Manager
            persona="", # To be filled by Prompt Manager
            memory=memory_data,
            history=history_data,
            question=question,
            examples=[] # To be filled by Prompt Manager
        )
