import unittest
import os
import json
from app.memory import MemoryManager
from app.config import MEMORY_FILE

class TestMemoryManager(unittest.TestCase):
    def setUp(self):
        # Clear memory before tests
        if os.path.exists(MEMORY_FILE):
            os.remove(MEMORY_FILE)
        self.memory = MemoryManager()

    def tearDown(self):
        if os.path.exists(MEMORY_FILE):
            os.remove(MEMORY_FILE)

    def test_update_facts(self):
        new_facts = {"name": "Alice", "role": "Developer"}
        self.memory.update_facts(new_facts)
        self.assertEqual(self.memory.facts["name"], "Alice")
        
        # Load fresh to verify saving
        fresh_memory = MemoryManager()
        self.assertEqual(fresh_memory.facts["role"], "Developer")

    def test_get_memory_string(self):
        self.memory.update_facts({"language": "Python"})
        mem_str = self.memory.get_memory_string()
        self.assertIn("language: Python", mem_str)

if __name__ == '__main__':
    unittest.main()
