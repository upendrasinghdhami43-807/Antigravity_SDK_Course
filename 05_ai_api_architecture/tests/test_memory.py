import pytest
import os
from core.memory.memory_manager import MemoryManager

def test_memory_lifecycle(tmp_path):
    test_file = tmp_path / "memory.json"
    manager = MemoryManager(str(test_file))
    
    assert manager.get_memory() == {}
    
    manager.update_memory({"language": "Python"})
    assert manager.get_memory() == {"language": "Python"}
    
    # Reload should persist
    manager2 = MemoryManager(str(test_file))
    assert manager2.get_memory() == {"language": "Python"}
    
    manager2.clear()
    assert manager2.get_memory() == {}
