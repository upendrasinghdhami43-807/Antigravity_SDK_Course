from pydantic import BaseModel, ValidationError
from typing import Type, Any, Tuple, Optional

class SchemaValidator:
    """Validates a dictionary against a Pydantic schema."""
    
    def validate(self, data: dict, schema: Type[BaseModel]) -> Tuple[bool, Optional[BaseModel], str]:
        """
        Returns (is_valid, parsed_object, error_message)
        """
        try:
            parsed = schema.model_validate(data)
            return True, parsed, ""
        except ValidationError as e:
            return False, None, str(e)
