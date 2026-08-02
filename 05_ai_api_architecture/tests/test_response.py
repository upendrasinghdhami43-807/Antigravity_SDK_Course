import pytest
from core.schemas.response import BaseResponse, BaseStatistics
from core.structured_output.manager import StructuredOutputManager
from core.schemas.chat import ChatResponse
from core.exceptions.framework_exceptions import StructuredOutputError

def test_base_response():
    resp = BaseStatistics(prompt_tokens=10, completion_tokens=20, response_time_ms=1.5)
    assert resp.prompt_tokens == 10

def test_structured_output_manager(monkeypatch):
    manager = StructuredOutputManager()
    
    # Valid
    res = manager.process('{"message": "hi", "role": "assistant", "timestamp": "now"}', ChatResponse)
    assert isinstance(res, ChatResponse)
    assert res.message == "hi"
    
    # Invalid -> throws Error since we don't have an active provider passed to it to repair (for simple tests)
    with pytest.raises(StructuredOutputError):
        manager.process('invalid', ChatResponse)
