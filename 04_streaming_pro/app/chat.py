import sys
import asyncio
from app.agent import Agent
from app.context import ContextBuilder
from app.history import HistoryManager
from app.memory import MemoryManager
from app.summarizer import SummaryManager
from app.session import SessionManager
from app.settings import SettingsManager
from app.statistics import StatisticsManager
from app.model_manager import ModelManager
from app.tokenizer import TokenManager
from app.stream_manager import StreamManager
from app.logger import get_logger

logger = get_logger("ChatEngine")

class ChatEngine:
    def __init__(self, client):
        logger.info("Initializing Chat Engine")
        
        # Initialize Managers
        self.settings_mgr = SettingsManager()
        self.stats_mgr = StatisticsManager()
        self.model_mgr = ModelManager(client, self.settings_mgr)
        self.history_mgr = HistoryManager()
        self.memory_mgr = MemoryManager()
        self.summary_mgr = SummaryManager()
        self.session_mgr = SessionManager()
        
        # Initialize Core Components
        self.agent = Agent(client, self.model_mgr)
        self.context_builder = ContextBuilder(
            history_mgr=self.history_mgr,
            memory_mgr=self.memory_mgr,
            summary_mgr=self.summary_mgr
        )
        self.stream_mgr = StreamManager(self.agent, self.stats_mgr)
        
        # Ensure default setting for streaming
        if self.settings_mgr.get("streaming") is None:
            self.settings_mgr.set("streaming", "ON")
            
        # Start Session
        self.session_mgr.start_session()
        
        # Deferred import to avoid circular dependency
        from app.command_router import CommandRouter
        self.command_router = CommandRouter(self)

    async def run(self):
        print("\n" + "="*40)
        print("🚀 Welcome to Antigravity AI Assistant! 🚀")
        print("Model :", self.model_mgr.get_current_model())
        print("Streaming :", self.settings_mgr.get("streaming", "ON"))
        print("="*40)
        print("Type '/help' for commands, '/exit' to quit.")
        
        while True:
            try:
                # Use standard input for terminal blocking, since we are idle here
                user_input = input("\nYou: ").strip()
                if not user_input:
                    continue

                if user_input.startswith("/") or user_input.lower() in ["exit", "quit", "help", "clear", "history", "summary", "memory", "stats", "token", "models", "model", "export", "settings", "reset", "stream"]:
                    should_exit = self.command_router.handle_command(user_input)
                    if should_exit:
                        self.shutdown()
                        break
                    continue

                await self.process_chat(user_input)
                
            except KeyboardInterrupt:
                if self.stream_mgr.is_streaming:
                    # Cancel the stream if it's currently running
                    print("\n[Stream Interrupted by User]")
                    self.stream_mgr.cancel_stream()
                else:
                    print("\nSaving session and exiting. Goodbye!")
                    self.shutdown()
                    break
            except EOFError:
                print("\nSaving session and exiting. Goodbye!")
                self.shutdown()
                break
            except Exception as e:
                logger.error(f"Unexpected error: {e}")
                print(f"\nAn error occurred: {e}")

    async def process_chat(self, user_input: str):
        # 1. Update stats
        self.stats_mgr.increment_questions()
        
        # 2. Build Context
        context_prompt = self.context_builder.build_context(user_input)
        
        # 3. Generate Response via Stream Manager
        stream_val = self.settings_mgr.get("streaming", "ON").upper()
        use_streaming = stream_val in ["ON", "ENABLED", "TRUE", "1"]
        
        assistant_response = await self.stream_mgr.run_stream(context_prompt, use_streaming=use_streaming)
        
        # 4. Update stats for response
        self.stats_mgr.increment_responses()
        
        # 5. Token Calculation
        prompt_tokens = TokenManager.count_tokens(context_prompt)
        response_tokens = TokenManager.count_tokens(assistant_response)
        self.stats_mgr.add_tokens(prompt_tokens, response_tokens)
        
        # 6. Save History
        self.history_mgr.append_message("user", user_input)
        self.history_mgr.append_message("assistant", assistant_response)
        
        # 7. Extract Memory (Facts) - Done asynchronously or in the background in a real app, but we await here
        new_facts = self.agent.extract_facts(user_input, assistant_response)
        if new_facts:
            self.memory_mgr.update_facts(new_facts)
            
        # 8. Check if Summarization is needed based on settings
        limit = int(self.settings_mgr.get("summary_limit", 50))
        if len(self.history_mgr.get_messages()) >= limit:
            history_text = self.history_mgr.get_formatted_history()
            new_summary = self.agent.summarize_history(history_text)
            self.summary_mgr.update_summary(new_summary)
            self.history_mgr.messages = self.history_mgr.messages[-10:]
            self.history_mgr.save_history()
            
    def shutdown(self):
        self.session_mgr.save_session()
        duration = getattr(self.session_mgr.current_session, "duration_seconds", 0) if self.session_mgr.current_session else 0
        self.stats_mgr.add_duration(duration)
        self.stats_mgr.save_stats()
        sys.exit(0)
