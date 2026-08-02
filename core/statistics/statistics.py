import json
import os
from typing import Dict, Any

class StatisticsManager:
    """Tracks aggregated usage statistics across sessions."""
    def __init__(self, data_file: str = "data/statistics.json"):
        self.data_file = data_file
        self.stats: Dict[str, Any] = {
            "total_requests": 0,
            "total_errors": 0,
            "total_prompt_tokens": 0,
            "total_completion_tokens": 0,
            "total_response_time_ms": 0.0,
            "average_response_time_ms": 0.0
        }
        self._load()

    def _load(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    self.stats.update(json.load(f))
            except json.JSONDecodeError:
                pass
        else:
            self._save()

    def _save(self):
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        with open(self.data_file, 'w') as f:
            json.dump(self.stats, f, indent=2)

    def record_request(self, prompt_tokens: int, completion_tokens: int, response_time_ms: float, error: bool = False):
        self.stats["total_requests"] += 1
        if error:
            self.stats["total_errors"] += 1
        
        self.stats["total_prompt_tokens"] += prompt_tokens
        self.stats["total_completion_tokens"] += completion_tokens
        self.stats["total_response_time_ms"] += response_time_ms
        
        if self.stats["total_requests"] > 0:
            self.stats["average_response_time_ms"] = (
                self.stats["total_response_time_ms"] / self.stats["total_requests"]
            )
        
        self._save()

    def get_statistics(self) -> Dict[str, Any]:
        return self.stats
