import pytest
from core.structured_output.validator import OutputValidator
from core.schemas.chat import ChatResponse
from core.exceptions.framework_exceptions import StructuredOutputError

def test_output_validator_success():
    validator = OutputValidator()
    data = {"message": "Hello", "role": "assistant", "timestamp": "now"}
    obj = validator.validate(data, ChatResponse)
    assert isinstance(obj, ChatResponse)
    
def test_output_validator_failure():
    validator = OutputValidator()
    with pytest.raises(StructuredOutputError):
        validator.validate({"message": "missing fields"}, ChatResponse)
