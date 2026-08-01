import uuid
import time
from datetime import datetime
from app.config import SESSION_FILE
from app.models import Session
from app.utils import load_json, save_json
from app.logger import get_logger

logger = get_logger("SessionManager")

class SessionManager:
    def __init__(self):
        self.current_session: Session = None
        self.start_session()

    def start_session(self):
        session_id = str(uuid.uuid4())
        start_time = datetime.now().isoformat()
        self.current_session = Session(
            session_id=session_id,
            start_time=start_time,
            message_count=0,
            duration_seconds=0
        )
        self._start_timestamp = time.time()
        self.save_session()
        logger.info(f"Started new session: {session_id}")

    def save_session(self):
        if self.current_session:
            self.current_session.duration_seconds = int(time.time() - self._start_timestamp)
            save_json(SESSION_FILE, self.current_session.to_dict())

    def increment_message_count(self):
        if self.current_session:
            self.current_session.message_count += 1
            self.save_session()
