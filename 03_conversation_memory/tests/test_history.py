import unittest
import os
from app.history import HistoryManager
from app.config import HISTORY_FILE

class TestHistoryManager(unittest.TestCase):
    def setUp(self):
        if os.path.exists(HISTORY_FILE):
            os.remove(HISTORY_FILE)
        self.history = HistoryManager()

    def tearDown(self):
        if os.path.exists(HISTORY_FILE):
            os.remove(HISTORY_FILE)

    def test_append_message(self):
        self.history.append_message("user", "Hello")
        self.assertEqual(len(self.history.messages), 1)
        self.assertEqual(self.history.messages[0].role, "user")
        self.assertEqual(self.history.messages[0].text, "Hello")

    def test_get_recent_messages(self):
        for i in range(5):
            self.history.append_message("user", f"Message {i}")
        recent = self.history.get_recent_messages(2)
        self.assertEqual(len(recent), 2)
        self.assertEqual(recent[0].text, "Message 3")
        self.assertEqual(recent[1].text, "Message 4")

if __name__ == '__main__':
    unittest.main()
