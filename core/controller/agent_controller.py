import time
from core.models.message import Message
from core.planner.planner import Planner
from core.reasoning.reasoning import ReasoningEngine
from core.context.context_builder import ContextBuilder
from core.prompt.prompt_pipeline import PromptPipeline
from core.provider.provider import Provider
from core.structured_output.manager import StructuredOutputManager
from core.memory.memory_manager import MemoryManager
from core.history.history_manager import HistoryManager
from core.statistics.statistics import StatisticsManager
from core.tokenizer.tokenizer import Tokenizer
from core.events.event_manager import EventManager
from core.logger.logger import get_logger
from core.schemas.chat import ChatResponse
from core.exceptions.framework_exceptions import StructuredOutputError

logger = get_logger()

class AgentController:
    """Orchestrates the entire request lifecycle (stages 1-29)."""
    def __init__(self, 
                 planner: Planner,
                 reasoning: ReasoningEngine,
                 context_builder: ContextBuilder,
                 prompt_pipeline: PromptPipeline,
                 provider: Provider,
                 output_manager: StructuredOutputManager,
                 memory: MemoryManager,
                 history: HistoryManager,
                 statistics: StatisticsManager,
                 events: EventManager):
        self.planner = planner
        self.reasoning = reasoning
        self.context_builder = context_builder
        self.prompt_pipeline = prompt_pipeline
        self.provider = provider
        self.output_manager = output_manager
        self.memory = memory
        self.history = history
        self.statistics = statistics
        self.events = events

    def process_request(self, user_input: str) -> str:
        start_time = time.time()
        self.events.publish("MessageReceived", user_input)
        
        # 1. Input Validation (basic)
        if not user_input.strip():
            return "Please provide an input."

        # 2. Planner
        plan = self.planner.create_plan(user_input)
        self.events.publish("PlannerFinished", plan)

        # 3. Reasoning
        reasoning_result = self.reasoning.analyze(user_input, plan)
        self.events.publish("ReasoningFinished", reasoning_result)

        # 4. Context Building
        mem_data = self.memory.get_memory() if reasoning_result.needs else {}
        hist_data = self.history.get_history(limit=5)
        context = self.context_builder.build_context(user_input, mem_data, hist_data)
        self.events.publish("ContextBuilt")

        # 5. Prompt Pipeline (Module 06)
        # We request JSON specifically
        output_instructions = "You MUST return a valid JSON object matching this schema:\n" \
                              "{'message': 'your reply', 'role': 'assistant', 'timestamp': 'ISO8601'}"
        final_prompt = self.prompt_pipeline.run_pipeline(context, output_instructions)
        self.events.publish("PromptBuilt")

        # 6. Provider Execution
        self.events.publish("ProviderStarted")
        try:
            raw_response = self.provider.generate_content(final_prompt)
            self.events.publish("ResponseReceived")
        except Exception as e:
            logger.error(f"Provider Error: {e}")
            self.statistics.record_request(0, 0, (time.time()-start_time)*1000, error=True)
            return f"Error: Provider failed - {e}"

        # 7. Structured Output Engine (Module 07)
        try:
            parsed_object = self.output_manager.process(raw_response, ChatResponse)
            response_text = parsed_object.message
            self.events.publish("OutputValidated", parsed_object)
        except StructuredOutputError as e:
            logger.warning(f"Failed to parse structured output: {e}. Falling back to raw response.")
            response_text = raw_response

        # 8. History Update
        self.history.add_message(Message(role="user", content=user_input))
        self.history.add_message(Message(role="assistant", content=response_text))
        self.events.publish("HistorySaved")

        # 9. Statistics Update
        end_time = time.time()
        p_tokens = Tokenizer.estimate_tokens(final_prompt)
        c_tokens = Tokenizer.estimate_tokens(raw_response)
        self.statistics.record_request(p_tokens, c_tokens, (end_time - start_time) * 1000)

        return response_text
