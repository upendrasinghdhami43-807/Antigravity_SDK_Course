from app.config import SUMMARY_FILE
from app.utils import load_json, save_json
from app.logger import get_logger

logger = get_logger("SummaryManager")

class SummaryManager:
    def __init__(self):
        self.summary: str = ""
        self.load_summary()

    def load_summary(self):
        data = load_json(SUMMARY_FILE, default={"summary": ""})
        self.summary = data.get("summary", "")
        if self.summary:
            logger.debug("Loaded existing summary.")

    def save_summary(self):
        save_json(SUMMARY_FILE, {"summary": self.summary})
        logger.debug("Saved summary to file.")

    def get_summary(self) -> str:
        return self.summary if self.summary else "No summary available."

    def update_summary(self, new_summary: str):
        self.summary = new_summary
        self.save_summary()
        logger.info("Summary updated.")
