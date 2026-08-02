from core.structured_output.formatter import Formatter
from core.schemas.chat import ChatResponse

def test_formatter():
    fmt = Formatter()
    data = {"key": "value"}
    res = fmt.format_pretty_json(data)
    assert '"key": "value"' in res
    
    obj = ChatResponse(message="msg", role="bot", timestamp="time")
    res_obj = fmt.format_object(obj)
    assert '"message": "msg"' in res_obj
