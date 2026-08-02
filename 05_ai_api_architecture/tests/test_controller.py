import pytest
import json
from core.controller.agent_controller import AgentController
from core.planner.planner import Planner
from core.reasoning.reasoning import ReasoningEngine
from core.context.context_builder import ContextBuilder
from core.prompt.prompt_pipeline import PromptPipeline
from core.prompt.manager import PromptManager
from core.structured_output.manager import StructuredOutputManager
from core.memory.memory_manager import MemoryManager
from core.history.history_manager import HistoryManager
from core.statistics.statistics import StatisticsManager
from core.events.event_manager import EventManager
from core.provider.provider import Provider

class MockProvider(Provider):
    def generate_content(self, prompt: str) -> str:
        return json.dumps({"message": "Mock response", "role": "assistant", "timestamp": "2024-01-01T00:00:00"})
    
    def generate_content_stream(self, prompt: str):
        yield ""

def test_controller_end_to_end(tmp_path):
    events = EventManager()
    events_log = []
    events.subscribe("ProviderStarted", lambda x: events_log.append("provider"))
    
    prompt_manager = PromptManager()
    prompt_manager.variable_manager.set_variable("SESSION_ID", "123")
    
    controller = AgentController(
        planner=Planner(),
        reasoning=ReasoningEngine(),
        context_builder=ContextBuilder(),
        prompt_pipeline=PromptPipeline(prompt_manager),
        provider=MockProvider(),
        output_manager=StructuredOutputManager(),
        memory=MemoryManager(str(tmp_path / "mem.json")),
        history=HistoryManager(str(tmp_path / "hist.json")),
        statistics=StatisticsManager(str(tmp_path / "stats.json")),
        events=events
    )
    
    response = controller.process_request("hello")
    assert response == "Mock response"
    assert "provider" in events_log
