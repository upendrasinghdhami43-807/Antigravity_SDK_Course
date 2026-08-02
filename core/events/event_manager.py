from typing import Callable, Any, Dict, List
import logging
from core.logger.logger import get_logger

logger = get_logger()

class EventManager:
    """
    Pub/Sub event bus for lifecycle events.
    """
    def __init__(self):
        self.subscribers: Dict[str, List[Callable]] = {}
        self.event_history: List[Dict[str, Any]] = []

    def subscribe(self, event_type: str, callback: Callable):
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []
        self.subscribers[event_type].append(callback)

    def unsubscribe(self, event_type: str, callback: Callable):
        if event_type in self.subscribers:
            if callback in self.subscribers[event_type]:
                self.subscribers[event_type].remove(callback)

    def publish(self, event_type: str, data: Any = None):
        event = {"type": event_type, "data": data}
        self.event_history.append(event)
        logger.debug(f"[EVENT] {event_type}")
        
        if event_type in self.subscribers:
            for callback in self.subscribers[event_type]:
                try:
                    callback(data)
                except Exception as e:
                    logger.error(f"Error in event subscriber for {event_type}: {e}")

    def get_history(self) -> List[Dict[str, Any]]:
        return self.event_history
