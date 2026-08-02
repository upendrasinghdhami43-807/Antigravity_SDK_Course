from pydantic import BaseModel
from typing import Type
from core.validators.schema_validator import SchemaValidator
from core.exceptions.framework_exceptions import StructuredOutputError

class OutputValidator:
    """Validates the parsed JSON data against a Pydantic schema."""
    def __init__(self):
        self.schema_validator = SchemaValidator()
        
    def validate(self, data: dict, schema: Type[BaseModel]) -> BaseModel:
        is_valid, parsed_object, error_msg = self.schema_validator.validate(data, schema)
        if not is_valid or parsed_object is None:
            raise StructuredOutputError(f"Schema validation failed: {error_msg}")
        return parsed_object
