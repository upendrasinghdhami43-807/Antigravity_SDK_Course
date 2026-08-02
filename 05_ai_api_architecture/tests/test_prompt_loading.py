import pytest
from core.prompt.template_loader import TemplateLoader
from core.prompt.variable_manager import VariableManager
from core.prompt.renderer import PromptRenderer

def test_template_loader_success(tmp_path):
    prompts_dir = tmp_path / "prompts"
    prompts_dir.mkdir()
    (prompts_dir / "test.md").write_text("Hello {{USER_NAME}}")
    
    loader = TemplateLoader(str(prompts_dir))
    content = loader.load_template("test")
    assert content == "Hello {{USER_NAME}}"
    
def test_template_loader_missing(tmp_path):
    loader = TemplateLoader(str(tmp_path))
    assert loader.load_template("missing") == ""

def test_variable_injection():
    var_manager = VariableManager()
    var_manager.set_variable("USER_NAME", "Alice")
    renderer = PromptRenderer(var_manager)
    
    rendered = renderer.render("Hello {{USER_NAME}}, today is {{CURRENT_DATE}}")
    assert "Alice" in rendered
    assert "{{CURRENT_DATE}}" not in rendered # Should be replaced by actual date
