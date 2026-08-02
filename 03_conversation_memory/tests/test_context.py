import unittest
from unittest.mock import Mock
from app.context import ContextBuilder
from app.history import HistoryManager
from app.memory import MemoryManager
from app.summarizer import SummaryManager

class TestContextBuilder(unittest.TestCase):
    def setUp(self):
        self.history_mock = Mock(spec=HistoryManager)
        self.memory_mock = Mock(spec=MemoryManager)
        self.summary_mock = Mock(spec=SummaryManager)
        
        self.context_builder = ContextBuilder(
            self.history_mock, 
            self.memory_mock, 
            self.summary_mock
        )

    def test_build_system_prompt(self):
        self.memory_mock.get_memory_string.return_value = "- name: Bob"
        self.summary_mock.get_summary.return_value = "Past summary here"
        
        prompt = self.context_builder.build_system_prompt()
        self.assertIn("name: Bob", prompt)
        self.assertIn("Past summary here", prompt)

if __name__ == '__main__':
    unittest.main()
