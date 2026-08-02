from pydantic import BaseModel
import json

class Formatter:
    """Formats structured data for output (e.g. JSON to pretty string)."""
    
    def format_pretty_json(self, data: dict) -> str:
        return json.dumps(data, indent=2)

    def format_object(self, obj: BaseModel) -> str:
        # In a real app, this could map schemas to markdown templates
        return self.format_pretty_json(obj.model_dump())
