import sys
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
        
        # Start Session
        self.session_mgr.start_session()
        
        # Deferred import to avoid circular dependency if router needs ChatEngine
        from app.command_router import CommandRouter
        self.command_router = CommandRouter(self)

    def run(self):
        print("\n" + "="*40)
        print("🚀 Welcome to Antigravity AI Assistant! 🚀")
        print("="*40)
        print("Type '/help' for commands, '/exit' to quit.")
        
        while True:
            try:
                user_input = input("\nYou: ").strip()
                if not user_input:
                    continue

                if user_input.startswith("/") or user_input.lower() in ["exit", "quit", "help", "clear", "history", "summary", "memory", "stats", "token", "models", "model", "export", "settings", "reset"]:
                    should_exit = self.command_router.handle_command(user_input)
                    if should_exit:
                        self.shutdown()
                        break
                    continue

                self.process_chat(user_input)
                
            except (KeyboardInterrupt, EOFError):
                print("\nSaving session and exiting. Goodbye!")
                self.shutdown()
                break
            except Exception as e:
                logger.error(f"Unexpected error: {e}")
                print(f"\nAn error occurred: {e}")

    def process_chat(self, user_input: str):
        # 1. Update stats
        self.stats_mgr.increment_questions()
        
        # 2. Build Context
        context_prompt = self.context_builder.build_context(user_input)
        
        # 3. Generate Response
        assistant_response, elapsed_time = self.agent.generate_response(context_prompt)
        print(f"Assistant: {assistant_response}")
        
        # 4. Update stats for response
        self.stats_mgr.increment_responses()
        self.stats_mgr.add_response_time(elapsed_time)
        
        # 5. Token Calculation
        prompt_tokens = TokenManager.count_tokens(context_prompt)
        response_tokens = TokenManager.count_tokens(assistant_response)
        self.stats_mgr.add_tokens(prompt_tokens, response_tokens)
        
        # 6. Save History
        self.history_mgr.append_message("user", user_input)
        self.history_mgr.append_message("assistant", assistant_response)
        
        # 7. Extract Memory (Facts)
        new_facts = self.agent.extract_facts(user_input, assistant_response)
        if new_facts:
            self.memory_mgr.update_facts(new_facts)
            
        # 8. Check if Summarization is needed based on settings
        limit = int(self.settings_mgr.get("summary_limit", 50))
        if len(self.history_mgr.get_messages()) >= limit:
            history_text = self.history_mgr.get_formatted_history()
            new_summary = self.agent.summarize_history(history_text)
            self.summary_mgr.update_summary(new_summary)
            # Leave recent messages but trim history to save context
            self.history_mgr.messages = self.history_mgr.messages[-10:]
            self.history_mgr.save_history()
            
    def shutdown(self):
        self.session_mgr.save_session()
        duration = getattr(self.session_mgr.current_session, "duration_seconds", 0) if self.session_mgr.current_session else 0
        self.stats_mgr.add_duration(duration)
        self.stats_mgr.save_stats()
        # History, memory, etc. are saved continuously as they update
        sys.exit(0)
