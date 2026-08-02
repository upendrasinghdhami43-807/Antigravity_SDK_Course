from core.prompt.variable_manager import VariableManager

class PromptRenderer:
    """Renders templates by injecting variables."""
    def __init__(self, variable_manager: VariableManager):
        self.variable_manager = variable_manager

    def render(self, template: str) -> str:
        if not template:
            return ""
        return self.variable_manager.inject_variables(template)
