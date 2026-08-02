from core.configuration.config import load_config
from core.logger.logger import get_logger, FrameworkLogger
from core.session.session_manager import SessionManager
from core.statistics.statistics import StatisticsManager
from core.memory.memory_manager import MemoryManager
from core.history.history_manager import HistoryManager
from core.provider.provider_factory import ProviderFactory
from core.prompt.manager import PromptManager
from core.prompt.prompt_pipeline import PromptPipeline
from core.structured_output.manager import StructuredOutputManager
from core.planner.planner import Planner
from core.reasoning.reasoning import ReasoningEngine
from core.context.context_builder import ContextBuilder
from core.controller.agent_controller import AgentController
from core.commands.command_router import CommandRouter
from core.events.event_manager import EventManager

logger = get_logger()

class Engine:
    """The central core that coordinates and wires all modules together."""
    def __init__(self):
        self.config = load_config()
        if self.config.debug:
            FrameworkLogger().set_level("DEBUG")
            
        self.events = EventManager()
        self.events.publish("ApplicationStarted")
        
        self.session = SessionManager()
        self.events.publish("SessionStarted", self.session.session_id)
        
        self.statistics = StatisticsManager()
        self.memory = MemoryManager()
        self.history = HistoryManager()
        
        self.provider = ProviderFactory.get_provider(self.config)
        self.prompt_manager = PromptManager()
        self.prompt_pipeline = PromptPipeline(self.prompt_manager)
        
        self.output_manager = StructuredOutputManager()
        
        self.planner = Planner()
        self.reasoning = ReasoningEngine()
        self.context_builder = ContextBuilder()
        
        self.controller = AgentController(
            planner=self.planner,
            reasoning=self.reasoning,
            context_builder=self.context_builder,
            prompt_pipeline=self.prompt_pipeline,
            provider=self.provider,
            output_manager=self.output_manager,
            memory=self.memory,
            history=self.history,
            statistics=self.statistics,
            events=self.events
        )
        
        self.command_router = CommandRouter()
        self._register_commands()

    def _register_commands(self):
        self.command_router.register("/help", lambda args: print("Commands: /help, /architecture, /pipeline, /stats, /config, /exit"))
        self.command_router.register("/stats", lambda args: print(self.statistics.get_statistics()))
        self.command_router.register("/config", lambda args: print(self.config.as_dict()))
        self.command_router.register("/exit", lambda args: exit(0))
        # Additional debug commands can be added here...

    def shutdown(self):
        self.session.end_session()
        self.events.publish("ApplicationClosed")
