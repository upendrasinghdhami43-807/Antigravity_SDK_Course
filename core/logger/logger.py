import logging
import os
from rich.logging import RichHandler

class FrameworkLogger:
    """
    Central logger for the framework. Logs to console via Rich and to file.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(FrameworkLogger, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        self.logger = logging.getLogger("AIAgentFramework")
        self.logger.setLevel(logging.DEBUG)  # Base level, handlers filter

        # Create logs directory if it doesn't exist
        os.makedirs("logs", exist_ok=True)

        # File Handler
        file_handler = logging.FileHandler("logs/framework.log")
        file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(file_formatter)
        self.logger.addHandler(file_handler)

        # Console Handler (Rich)
        console_handler = RichHandler(rich_tracebacks=True, markup=True)
        console_formatter = logging.Formatter('%(message)s')
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)
        
        self.file_handler = file_handler
        self.console_handler = console_handler

    def set_level(self, level_str: str):
        level = getattr(logging, level_str.upper(), logging.INFO)
        self.console_handler.setLevel(level)
        self.file_handler.setLevel(level)

    def get_logger(self) -> logging.Logger:
        return self.logger

def get_logger() -> logging.Logger:
    return FrameworkLogger().get_logger()
