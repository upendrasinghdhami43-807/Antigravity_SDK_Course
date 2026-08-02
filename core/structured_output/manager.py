from typing import Type
from pydantic import BaseModel
from core.structured_output.parser import Parser
from core.structured_output.validator import OutputValidator
from core.structured_output.formatter import Formatter
from core.logger.logger import get_logger

logger = get_logger()

class StructuredOutputManager:
    """Coordinates parse -> validate -> format -> convert"""
    def __init__(self):
        self.parser = Parser()
        self.validator = OutputValidator()
        self.formatter = Formatter()

    def process(self, raw_text: str, schema: Type[BaseModel]) -> BaseModel:
        logger.debug("[STRUCTURED_OUTPUT] Parsing raw text to JSON")
        data = self.parser.parse(raw_text)
        
        logger.debug("[STRUCTURED_OUTPUT] Validating against schema")
        parsed_object = self.validator.validate(data, schema)
        
        return parsed_object
