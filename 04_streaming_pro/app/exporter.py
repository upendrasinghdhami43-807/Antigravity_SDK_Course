import os
import json
from datetime import datetime
from typing import List
from app.models import Message
from app.logger import get_logger

logger = get_logger("Exporter")
EXPORT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "exports")

class Exporter:
    @staticmethod
    def _get_timestamp():
        return datetime.now().strftime("%Y%m%d_%H%M%S")

    @staticmethod
    def export_markdown(messages: List[Message]) -> str:
        filepath = os.path.join(EXPORT_DIR, "markdown", f"export_{Exporter._get_timestamp()}.md")
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write("# Conversation Export\n\n")
                for msg in messages:
                    f.write(f"**{msg.role.capitalize()}**:\n{msg.text}\n\n")
            logger.info(f"Exported to {filepath}")
            return filepath
        except Exception as e:
            logger.error(f"Failed to export markdown: {e}")
            return ""

    @staticmethod
    def export_txt(messages: List[Message]) -> str:
        filepath = os.path.join(EXPORT_DIR, "txt", f"export_{Exporter._get_timestamp()}.txt")
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write("Conversation Export\n===================\n\n")
                for msg in messages:
                    f.write(f"{msg.role.capitalize()}:\n{msg.text}\n\n")
            logger.info(f"Exported to {filepath}")
            return filepath
        except Exception as e:
            logger.error(f"Failed to export txt: {e}")
            return ""

    @staticmethod
    def export_json(messages: List[Message]) -> str:
        filepath = os.path.join(EXPORT_DIR, "json", f"export_{Exporter._get_timestamp()}.json")
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        try:
            data = [msg.to_dict() for msg in messages]
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
            logger.info(f"Exported to {filepath}")
            return filepath
        except Exception as e:
            logger.error(f"Failed to export json: {e}")
            return ""
