import pytest
from core.prompt.manager import PromptManager
from core.prompt.prompt_pipeline import PromptPipeline
from core.context.context_builder import Context
from core.exceptions.framework_exceptions import PromptValidationError

def test_prompt_pipeline_success():
    manager = PromptManager()
    manager.variable_manager.set_variable("SESSION_ID", "123")
    pipeline = PromptPipeline(manager)
    
    context = Context(
        system_prompt="System",
        developer_prompt="Dev",
        persona="Persona",
        memory={},
        history=[],
        question="Hello",
        examples=[]
    )
    
    final_prompt = pipeline.run_pipeline(context, "Return JSON")
    assert "USER INPUT" in final_prompt
    assert "Hello" in final_prompt
    assert "Return JSON" in final_prompt

def test_prompt_pipeline_validation_error():
    manager = PromptManager()
    pipeline = PromptPipeline(manager)
    
    context = Context("", "", "", {}, [], "", [])
    
    with pytest.raises(PromptValidationError):
        pipeline.run_pipeline(context) # Empty prompt should fail
