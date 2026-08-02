from core.validators.json_validator import JSONValidator

def test_json_validator():
    validator = JSONValidator()
    
    # Valid
    is_valid, data = validator.validate_and_repair('{"a": 1}')
    assert is_valid is True
    assert data["a"] == 1
    
    # Repairable
    is_valid, data = validator.validate_and_repair('```json\n{"b": 2}\n```')
    assert is_valid is True
    assert data["b"] == 2
    
    # Invalid
    is_valid, data = validator.validate_and_repair('not json')
    assert is_valid is False
    assert data is None
