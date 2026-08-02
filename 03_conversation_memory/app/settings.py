from typing import Dict, Any
import os
from app.utils import load_json, save_json
from app.config import DATA_DIR
from app.logger import get_logger

logger = get_logger("SettingsManager")
SETTINGS_FILE = os.path.join(DATA_DIR, "settings.json")

class SettingsManager:
    def __init__(self):
        self.settings: Dict[str, Any] = {
            "theme": "Dark",
            "current_model": "gemini-2.0-flash",
            "streaming": "Enabled",
            "auto_save": "Enabled",
            "summary_limit": 50,
            "context_limit": 100
        }
        self.load_settings()

    def load_settings(self):
        data = load_json(SETTINGS_FILE, default={})
        if data:
            self.settings.update(data)
            logger.debug("Settings loaded.")

    def save_settings(self):
        save_json(SETTINGS_FILE, self.settings)
        logger.debug("Settings saved.")

    def get(self, key: str, default: Any = None) -> Any:
        return self.settings.get(key, default)

    def set(self, key: str, value: Any):
        self.settings[key] = value
        self.save_settings()
        logger.info(f"Setting '{key}' updated to '{value}'.")
