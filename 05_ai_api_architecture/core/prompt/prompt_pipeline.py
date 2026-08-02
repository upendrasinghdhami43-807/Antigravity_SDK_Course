from core.context.context_builder import Context
from core.prompt.manager import PromptManager
from core.prompt.builder import PromptBuilder
from core.prompt.validator import PromptValidator
from core.prompt.formatter import PromptFormatter
from core.logger.logger import get_logger

logger = get_logger()

class PromptPipeline:
    """End-to-end orchestration of the prompt layer."""
    def __init__(self, prompt_manager: PromptManager):
        self.manager = prompt_manager
        self.builder = PromptBuilder()
        self.validator = PromptValidator()
        self.formatter = PromptFormatter()

    def run_pipeline(self, context: Context, output_instructions: str = "") -> str:
        logger.debug("[PIPELINE] Running Prompt Pipeline")
        
        # 1. Load System/Developer/Persona
        context.system_prompt = self.manager.get_system_prompt()
        context.developer_prompt = self.manager.get_developer_prompt()
        context.persona = self.manager.get_active_persona_prompt()
        
        # 2. Build
        raw_prompt = self.builder.build(context, output_instructions)
        
        # 3. Validate
        self.validator.validate(raw_prompt)
        
        # 4. Format
        final_prompt = self.formatter.format(raw_prompt)
        
        return final_prompt
