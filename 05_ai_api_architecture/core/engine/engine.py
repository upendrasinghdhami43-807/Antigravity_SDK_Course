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
        self.command_router.register("/help", lambda args: print("Commands: /help, /architecture, /pipeline, /planner, /reasoning, /context, /memory, /history, /session, /provider, /stats, /config, /logs, /events, /performance, /reset, /exit, /persona, /system, /developer, /showprompt, /prompts, /template, /variables, /examples, /reloadprompts, /schema, /json, /validate, /parser, /format, /object, /response, /pretty, /exportjson, /exportmd, /models"))
        self.command_router.register("/architecture", lambda args: print("Phase 2 Architecture loaded."))
        self.command_router.register("/pipeline", lambda args: print("Pipeline: Planner -> Reasoning -> Context -> Prompt -> Provider -> Parser -> Output"))
        self.command_router.register("/planner", lambda args: print("Planner details pending request..."))
        self.command_router.register("/reasoning", lambda args: print("Reasoning details pending request..."))
        self.command_router.register("/context", lambda args: print("Context details pending request..."))
        self.command_router.register("/memory", lambda args: print(self.memory.get_memory()))
        self.command_router.register("/history", lambda args: print(self.history.get_history()))
        self.command_router.register("/session", lambda args: print(self.session.get_state()))
        self.command_router.register("/provider", lambda args: print(f"Provider: {self.config.default_model}"))
        self.command_router.register("/models", self._handle_models_command)
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

    def _handle_models_command(self, args):
        menu = """
============================
Available Gemini Models
============================

--- General / Fast (Free Tier Friendly) ---
1. gemini-2.5-flash
2. gemini-2.0-flash
3. gemini-2.0-flash-001
4. gemini-2.0-flash-lite-001
5. gemini-2.0-flash-lite
6. gemini-flash-latest
7. gemini-flash-lite-latest
8. gemini-2.5-flash-lite

--- Complex Reasoning (Pro) ---
9. gemini-2.5-pro
10. gemini-pro-latest

--- Image & Vision ---
11. gemini-2.5-flash-image
12. gemini-3-pro-image-preview
13. gemini-3-pro-image
14. gemini-3.1-flash-image-preview
15. gemini-3.1-flash-image
16. gemini-3.1-flash-lite-image

--- Audio & Voice ---
17. gemini-2.5-flash-preview-tts
18. gemini-2.5-pro-preview-tts
19. gemini-3.1-flash-tts-preview
20. gemini-2.5-flash-native-audio-latest
21. gemini-2.5-flash-native-audio-preview-09-2025
22. gemini-2.5-flash-native-audio-preview-12-2025

--- Embeddings & Search ---
23. gemini-embedding-001
24. gemini-embedding-2-preview
25. gemini-embedding-2

--- Preview & Experimental (May be Paid) ---
26. gemini-3-pro-preview
27. gemini-3-flash-preview
28. gemini-3.1-pro-preview
29. gemini-3.1-pro-preview-customtools
30. gemini-3.1-flash-lite-preview
31. gemini-3.1-flash-lite
32. gemini-3.5-flash
33. gemini-3.5-flash-lite
34. gemini-omni-flash-preview
35. gemini-3.6-flash
36. gemini-robotics-er-1.5-preview
37. gemini-robotics-er-1.6-preview
38. gemini-robotics-er-2-preview
39. gemini-2.5-computer-use-preview-10-2025
40. gemini-3.1-flash-live-preview
41. gemini-robotics-er-2-streaming-preview
42. gemini-3.5-live-translate-preview
"""
        print(menu)
        
        try:
            choice = input(f"Current Model: {self.config.default_model}\nSelect a model number: ").strip()
            models = {
                "1": "gemini-2.5-flash", "2": "gemini-2.0-flash", "3": "gemini-2.0-flash-001", "4": "gemini-2.0-flash-lite-001",
                "5": "gemini-2.0-flash-lite", "6": "gemini-flash-latest", "7": "gemini-flash-lite-latest", "8": "gemini-2.5-flash-lite",
                "9": "gemini-2.5-pro", "10": "gemini-pro-latest", "11": "gemini-2.5-flash-image", "12": "gemini-3-pro-image-preview",
                "13": "gemini-3-pro-image", "14": "gemini-3.1-flash-image-preview", "15": "gemini-3.1-flash-image", "16": "gemini-3.1-flash-lite-image",
                "17": "gemini-2.5-flash-preview-tts", "18": "gemini-2.5-pro-preview-tts", "19": "gemini-3.1-flash-tts-preview", "20": "gemini-2.5-flash-native-audio-latest",
                "21": "gemini-2.5-flash-native-audio-preview-09-2025", "22": "gemini-2.5-flash-native-audio-preview-12-2025", "23": "gemini-embedding-001",
                "24": "gemini-embedding-2-preview", "25": "gemini-embedding-2", "26": "gemini-3-pro-preview", "27": "gemini-3-flash-preview",
                "28": "gemini-3.1-pro-preview", "29": "gemini-3.1-pro-preview-customtools", "30": "gemini-3.1-flash-lite-preview",
                "31": "gemini-3.1-flash-lite", "32": "gemini-3.5-flash", "33": "gemini-3.5-flash-lite", "34": "gemini-omni-flash-preview",
                "35": "gemini-3.6-flash", "36": "gemini-robotics-er-1.5-preview", "37": "gemini-robotics-er-1.6-preview",
                "38": "gemini-robotics-er-2-preview", "39": "gemini-2.5-computer-use-preview-10-2025", "40": "gemini-3.1-flash-live-preview",
                "41": "gemini-robotics-er-2-streaming-preview", "42": "gemini-3.5-live-translate-preview"
            }
            if choice in models:
                self.config.default_model = models[choice]
                print(f"Model changed to {self.config.default_model}")
                # Update the variable in VariableManager so prompt templates reflect the correct model
                if hasattr(self, 'prompt_manager') and hasattr(self.prompt_manager, 'variable_manager'):
                    self.prompt_manager.variable_manager.set_variable("CURRENT_MODEL", self.config.default_model)
            else:
                print("Invalid selection. Model not changed.")
        except Exception as e:
            print(f"Error selecting model: {e}")
