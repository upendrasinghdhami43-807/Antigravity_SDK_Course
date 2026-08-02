from core.validators.json_validator import JSONValidator
from core.exceptions.framework_exceptions import StructuredOutputError

class Parser:
    """Raw text -> JSON parser."""
    def __init__(self):
        self.json_validator = JSONValidator()
        
    def parse(self, raw_text: str) -> dict:
        is_valid, data = self.json_validator.validate_and_repair(raw_text)
        if not is_valid or data is None:
            raise StructuredOutputError("Failed to parse raw text into valid JSON.")
        return data
