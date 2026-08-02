import os

class MarkdownExporter:
    def export(self, content: str, filename: str = "export.md") -> str:
        os.makedirs("exports", exist_ok=True)
        filepath = os.path.join("exports", filename)
        with open(filepath, "w") as f:
            f.write(content)
        return filepath
