import os

class TemplateLoader:
    """Loads Markdown templates from the prompts directory."""
    def __init__(self, prompts_dir: str = "prompts"):
        self.prompts_dir = prompts_dir

    def load_template(self, template_name: str) -> str:
        """Loads a template by name (e.g., 'system' -> 'prompts/system.md')."""
        if not template_name.endswith('.md'):
            template_name += '.md'
            
        file_path = os.path.join(self.prompts_dir, template_name)
        if not os.path.exists(file_path):
            # Fallback or empty string
            return ""
            
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
