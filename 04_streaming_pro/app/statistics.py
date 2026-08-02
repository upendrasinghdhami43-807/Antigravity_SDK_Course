from typing import Dict, Any
import os
from app.utils import load_json, save_json
from app.config import DATA_DIR
from app.logger import get_logger

logger = get_logger("StatisticsManager")
STATISTICS_FILE = os.path.join(DATA_DIR, "statistics.json")

class StatisticsManager:
    def __init__(self):
        self.stats: Dict[str, Any] = {
            "messages": 0,
            "questions": 0,
            "responses": 0,
            "session_duration": 0,
            "prompt_tokens": 0,
            "response_tokens": 0,
            "average_response_time": 0.0,
            "_total_response_time": 0.0,
            "average_latency": 0.0,
            "_total_latency": 0.0,
            "_total_characters": 0,
            "characters_per_second": 0.0,
            "tokens_per_second": 0.0
        }
        self.load_stats()

    def load_stats(self):
        data = load_json(STATISTICS_FILE, default={})
        if data:
            self.stats.update(data)
            # Ensure new streaming metrics exist for older stats files
            if "average_latency" not in self.stats:
                self.stats.update({
                    "average_latency": 0.0,
                    "_total_latency": 0.0,
                    "_total_characters": 0,
                    "characters_per_second": 0.0,
                    "tokens_per_second": 0.0
                })
            logger.debug("Statistics loaded.")

    def save_stats(self):
        save_json(STATISTICS_FILE, self.stats)
        logger.debug("Statistics saved.")

    def increment_messages(self, count: int = 1):
        self.stats["messages"] += count

    def increment_questions(self, count: int = 1):
        self.stats["questions"] += count
        self.increment_messages(count)
        self.save_stats()

    def increment_responses(self, count: int = 1):
        self.stats["responses"] += count
        self.increment_messages(count)
        self.save_stats()

    def add_duration(self, seconds: int):
        self.stats["session_duration"] += seconds
        self.save_stats()

    def add_tokens(self, prompt: int, response: int):
        self.stats["prompt_tokens"] += prompt
        self.stats["response_tokens"] += response
        self.stats["_total_characters"] += (response * 4)
        self.save_stats()

    def add_response_time(self, seconds: float):
        self.stats["_total_response_time"] += seconds
        if self.stats["responses"] > 0:
            self.stats["average_response_time"] = round(self.stats["_total_response_time"] / self.stats["responses"], 2)
            
            if self.stats["_total_response_time"] > 0:
                tps = self.stats["response_tokens"] / self.stats["_total_response_time"]
                cps = self.stats["_total_characters"] / self.stats["_total_response_time"]
                self.stats["tokens_per_second"] = round(tps, 2)
                self.stats["characters_per_second"] = round(cps, 2)
        self.save_stats()

    def add_latency(self, seconds: float):
        self.stats["_total_latency"] += seconds
        if self.stats["responses"] > 0:
            self.stats["average_latency"] = round(self.stats["_total_latency"] / self.stats["responses"], 2)
        self.save_stats()
        
    def get_all(self) -> Dict[str, Any]:
        return self.stats
