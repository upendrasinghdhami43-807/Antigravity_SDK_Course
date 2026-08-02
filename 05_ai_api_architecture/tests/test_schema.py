import pytest
from core.schemas.chat import ChatResponse
from core.schemas.planner import PlannerResponse

def test_chat_schema_valid():
    data = {"message": "Hello", "role": "assistant", "timestamp": "2024-01-01T00:00:00"}
    obj = ChatResponse.model_validate(data)
    assert obj.message == "Hello"
    
def test_chat_schema_invalid():
    data = {"message": "Hello"} # Missing required fields
    with pytest.raises(Exception):
        ChatResponse.model_validate(data)

def test_planner_schema_valid():
    data = {
        "goal": "Test", 
        "intent": "Question",
        "priority": "High",
        "need_tools": False,
        "need_memory": True,
        "need_search": False,
        "complexity": "Low"
    }
    obj = PlannerResponse.model_validate(data)
    assert obj.goal == "Test"
