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
        # Module 05 Commands
        self.command_router.register("/help", lambda args: print("Commands: /help, /architecture, /pipeline, /planner, /reasoning, /context, /memory, /history, /session, /provider, /stats, /config, /logs, /events, /performance, /reset, /exit, /persona, /system, /developer, /showprompt, /prompts, /template, /variables, /examples, /reloadprompts, /schema, /json, /validate, /parser, /format, /object, /response, /pretty, /exportjson, /exportmd"))
        self.command_router.register("/architecture", lambda args: print("Phase 2 Architecture loaded."))
        self.command_router.register("/pipeline", lambda args: print("Pipeline: Planner -> Reasoning -> Context -> Prompt -> Provider -> Parser -> Output"))
        self.command_router.register("/planner", lambda args: print("Planner details pending request..."))
        self.command_router.register("/reasoning", lambda args: print("Reasoning details pending request..."))
        self.command_router.register("/context", lambda args: print("Context details pending request..."))
        self.command_router.register("/memory", lambda args: print(self.memory.get_memory()))
        self.command_router.register("/history", lambda args: print(self.history.get_history()))
        self.command_router.register("/session", lambda args: print(self.session.get_state()))
        self.command_router.register("/provider", lambda args: print(f"Provider: {self.config.default_model}"))
        self.command_router.register("/stats", lambda args: print(self.statistics.get_statistics()))
        self.command_router.register("/config", lambda args: print(self.config.as_dict()))
        self.command_router.register("/logs", lambda args: print("Tail logs via logs/framework.log"))
        self.command_router.register("/events", lambda args: print("Events dispatched..."))
        self.command_router.register("/performance", lambda args: print("Performance metrics pending..."))
        self.command_router.register("/reset", lambda args: self.history.clear())
        self.command_router.register("/exit", lambda args: self.shutdown())
        
        # Module 06 Commands
        self.command_router.register("/persona", lambda args: self.prompt_manager.persona_manager.set_persona(args[0]) if args else print(self.prompt_manager.persona_manager.get_persona()))
        self.command_router.register("/system", lambda args: print("System rules..."))
        self.command_router.register("/developer", lambda args: print("Developer rules..."))
        self.command_router.register("/showprompt", lambda args: print("Last generated prompt..."))
        self.command_router.register("/prompts", lambda args: print("Available templates..."))
        self.command_router.register("/template", lambda args: print(f"Template {args[0]} content..." if args else "Need template name"))
        self.command_router.register("/variables", lambda args: print(self.prompt_manager.variable_manager.variables))
        self.command_router.register("/examples", lambda args: print("Examples loaded..."))
        self.command_router.register("/reloadprompts", lambda args: print("Prompts reloaded."))
        
        # Module 07 Commands
        self.command_router.register("/schema", lambda args: print("Active Schema..."))
        self.command_router.register("/json", lambda args: print("Raw JSON from model..."))
        self.command_router.register("/validate", lambda args: print("Validation logic executed..."))
        self.command_router.register("/parser", lambda args: print("Parser info..."))
        self.command_router.register("/format", lambda args: print("Format logic..."))
        self.command_router.register("/object", lambda args: print("Pydantic object representation..."))
        self.command_router.register("/response", lambda args: print("Last response object..."))
        self.command_router.register("/pretty", lambda args: print("Pretty formatted output..."))
        self.command_router.register("/exportjson", lambda args: print("Exported to JSON."))
        self.command_router.register("/exportmd", lambda args: print("Exported to Markdown."))

    def shutdown(self):
        self.session.end_session()
        self.events.publish("ApplicationClosed")
