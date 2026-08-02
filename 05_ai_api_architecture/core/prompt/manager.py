from core.prompt.template_loader import TemplateLoader
from core.prompt.variable_manager import VariableManager
from core.prompt.persona_manager import PersonaManager
from core.prompt.renderer import PromptRenderer

class PromptManager:
    """Coordinates the prompt components (loading, switching persona)."""
    def __init__(self):
        self.template_loader = TemplateLoader()
        self.variable_manager = VariableManager()
        self.persona_manager = PersonaManager()
        self.renderer = PromptRenderer(self.variable_manager)

    def load_and_render(self, template_name: str) -> str:
        template = self.template_loader.load_template(template_name)
        return self.renderer.render(template)

    def get_system_prompt(self) -> str:
        return self.load_and_render("system")

    def get_developer_prompt(self) -> str:
        return self.load_and_render("developer")

    def get_active_persona_prompt(self) -> str:
        persona = self.persona_manager.get_persona()
        if not persona:
            return ""
        return self.load_and_render(persona)
