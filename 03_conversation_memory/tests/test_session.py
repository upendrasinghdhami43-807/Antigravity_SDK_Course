import unittest
import os
from app.session import SessionManager
from app.config import SESSION_FILE

class TestSessionManager(unittest.TestCase):
    def setUp(self):
        if os.path.exists(SESSION_FILE):
            os.remove(SESSION_FILE)
        self.session = SessionManager()

    def tearDown(self):
        if os.path.exists(SESSION_FILE):
            os.remove(SESSION_FILE)

    def test_start_session(self):
        self.assertIsNotNone(self.session.current_session.session_id)
        self.assertEqual(self.session.current_session.message_count, 0)

    def test_increment_message_count(self):
        self.session.increment_message_count()
        self.assertEqual(self.session.current_session.message_count, 1)

if __name__ == '__main__':
    unittest.main()
