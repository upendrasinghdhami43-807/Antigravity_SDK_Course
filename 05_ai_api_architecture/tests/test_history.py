import pytest
from core.history.history_manager import HistoryManager
from core.models.message import Message

def test_history_lifecycle(tmp_path):
    test_file = tmp_path / "history.json"
    manager = HistoryManager(str(test_file))
    
    assert len(manager.get_history()) == 0
    
    msg = Message(role="user", content="hello")
    manager.add_message(msg)
    
    history = manager.get_history()
    assert len(history) == 1
    assert history[0].content == "hello"
    
    manager2 = HistoryManager(str(test_file))
    assert len(manager2.get_history()) == 1
    
    manager2.clear()
    assert len(manager2.get_history()) == 0

def test_history_limit(tmp_path):
    manager = HistoryManager(str(tmp_path / "history.json"))
    for i in range(10):
        manager.add_message(Message(role="user", content=str(i)))
    
    limited = manager.get_history(limit=5)
    assert len(limited) == 5
    assert limited[-1].content == "9"
