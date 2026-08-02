import os
from typing import Optional
from dotenv import load_dotenv
from core.exceptions.framework_exceptions import ConfigurationError

class Config:
    """
    Configuration manager for the AI Agent Framework.
    Loads and validates environment variables.
    """
    def __init__(self, env_file: Optional[str] = None):
        if env_file and os.path.exists(env_file):
            load_dotenv(env_file)
        else:
            load_dotenv()

        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        if not self.gemini_api_key:
            raise ConfigurationError("GEMINI_API_KEY is required but not set in the environment.")
        
        self.default_model = os.getenv("DEFAULT_MODEL", "gemini-2.5-flash")
        
        try:
            self.temperature = float(os.getenv("TEMPERATURE", "0.7"))
        except ValueError:
            self.temperature = 0.7
            
        self.streaming = os.getenv("STREAMING", "true").lower() == "true"
        self.debug = os.getenv("DEBUG", "false").lower() == "true"
        
        try:
            self.max_history = int(os.getenv("MAX_HISTORY", "50"))
        except ValueError:
            self.max_history = 50
            
        self.log_level = os.getenv("LOG_LEVEL", "INFO").upper()

    def as_dict(self) -> dict:
        """Return the configuration as a dictionary, masking sensitive information."""
        return {
            "gemini_api_key": "***MASKED***",
            "default_model": self.default_model,
            "temperature": self.temperature,
            "streaming": self.streaming,
            "debug": self.debug,
            "max_history": self.max_history,
            "log_level": self.log_level
        }

def load_config() -> Config:
    """Helper to load config based on APP_ENV profile if set."""
    app_env = os.getenv("APP_ENV")
    if app_env:
        env_path = os.path.join(os.getcwd(), "config", f"{app_env}.env")
        if os.path.exists(env_path):
            return Config(env_file=env_path)
    return Config()
