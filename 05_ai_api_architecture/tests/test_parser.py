import pytest
from core.structured_output.parser import Parser
from core.exceptions.framework_exceptions import StructuredOutputError

def test_parser_success():
    parser = Parser()
    res = parser.parse('{"key": "value"}')
    assert res["key"] == "value"
    
def test_parser_markdown_stripping():
    parser = Parser()
    res = parser.parse('```json\n{"key": "value"}\n```')
    assert res["key"] == "value"
    
def test_parser_failure():
    parser = Parser()
    with pytest.raises(StructuredOutputError):
        parser.parse('not a json object')
