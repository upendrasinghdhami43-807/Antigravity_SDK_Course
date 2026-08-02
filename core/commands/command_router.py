import logging
from typing import Callable, Dict
from core.logger.logger import get_logger

logger = get_logger()

class CommandRouter:
    """
    Routes anything starting with '/' to its registered handler.
    Chat logic and command logic never mix.
    """
    def __init__(self):
        self.handlers: Dict[str, Callable] = {}

    def register(self, command: str, handler: Callable):
        self.handlers[command.lower()] = handler

    def is_command(self, user_input: str) -> bool:
        return user_input.strip().startswith("/")

    def route(self, user_input: str) -> bool:
        """
        Executes the command if found. Returns True if handled, False otherwise.
        """
        if not self.is_command(user_input):
            return False

        parts = user_input.strip().split(" ", 1)
        command = parts[0].lower()
        args = parts[1] if len(parts) > 1 else ""

        if command in self.handlers:
            try:
                self.handlers[command](args)
                return True
            except Exception as e:
                logger.error(f"Error executing command {command}: {e}")
                return True
        else:
            print(f"Unknown command: {command}. Type /help for a list of commands.")
            return True
