import json
import os

class JSONExporter:
    def export(self, data: dict, filename: str = "export.json") -> str:
        os.makedirs("exports", exist_ok=True)
        filepath = os.path.join("exports", filename)
        with open(filepath, "w") as f:
            json.dump(data, f, indent=4)
        return filepath
