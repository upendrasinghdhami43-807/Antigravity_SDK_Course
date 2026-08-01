from app.menu import print_header, print_section, print_key_value, print_help
from app.exporter import Exporter
import sys

class CommandRouter:
    def __init__(self, chat_engine):
        self.chat_engine = chat_engine

    def handle_command(self, cmd_input: str) -> bool:
        """Returns True if the application should exit, False otherwise."""
        cmd_parts = cmd_input.lower().strip().split()
        cmd = cmd_parts[0]
        
        # Strip leading slash if present to make /command and command identical
        if cmd.startswith("/"):
            cmd = cmd[1:]

        if cmd in ["exit", "quit"]:
            print("\nSaving session and exiting. Goodbye!")
            return True
            
        elif cmd == "help":
            print_help()
            
        elif cmd == "clear":
            print('\033[2J\033[H', end='') # ANSI escape to clear screen
            
        elif cmd == "models":
            print_header("Available Gemini Models")
            categories, indexed = self.chat_engine.model_mgr.get_categorized_models()
            for cat_name, models in categories.items():
                print(f"\n--- {cat_name} ---")
                for m in models:
                    # Find index for display
                    idx = next((k for k, v in indexed.items() if v == m), "?")
                    print(f"{idx}. {m}")
                    
            print("\nCurrent Model:\n" + self.chat_engine.model_mgr.get_current_model() + "\n")
            print("Tip: Type '/model <number>' to quickly switch!\n")
            
        elif cmd == "model":
            if len(cmd_parts) > 1:
                new_model = cmd_parts[1]
                old_model = self.chat_engine.model_mgr.get_current_model()
                if self.chat_engine.model_mgr.switch_model(new_model):
                    print(f"\nCurrent model changed.\n\nOld\n{old_model}\n\n↓\n\nNew\n{self.chat_engine.model_mgr.get_current_model()}\n")
                else:
                    print(f"\nModel '{new_model}' not found in available models.\n")
            else:
                print("\nUsage: /model <model_name>\n")
                
        elif cmd == "token":
            stats = self.chat_engine.stats_mgr.get_all()
            context_limit_setting = self.chat_engine.settings_mgr.get("context_limit", 100)
            
            # Note: Context limit in tokens is configured in env usually, 
            # but settings "context_limit" is just messages.
            # We'll use a fixed arbitrary limit like 1M to match the design doc if needed,
            # or pull from config.
            from app.config import MAX_HISTORY_TOKENS
            limit = MAX_HISTORY_TOKENS
            
            session_total = stats['prompt_tokens'] + stats['response_tokens']
            percent_used = (session_total / limit) * 100 if limit > 0 else 0
            
            print_header("Token Statistics")
            print_key_value("Prompt Tokens", str(stats['prompt_tokens']))
            print_key_value("Response Tokens", str(stats['response_tokens']))
            print_key_value("Session Total", str(session_total))
            print_key_value("Configured Context Limit", f"{limit:,}")
            print_key_value("Used", f"{percent_used:.2f}%")
            
        elif cmd == "stats":
            stats = self.chat_engine.stats_mgr.get_all()
            print_header("Session Statistics")
            print_key_value("Messages", str(stats['messages']))
            print_key_value("Questions", str(stats['questions']))
            print_key_value("Responses", str(stats['responses']))
            
            duration_str = f"{stats['session_duration'] // 60} minutes" if stats['session_duration'] > 60 else f"{stats['session_duration']} seconds"
            print_key_value("Session Duration", duration_str)
            print_key_value("Average Response Time", f"{stats['average_response_time']} sec")
            print_key_value("Model", self.chat_engine.model_mgr.get_current_model())
            
            history_size_bytes = sys.getsizeof(str(self.chat_engine.history_mgr.get_messages()))
            print_key_value("History Size", f"{history_size_bytes / 1024:.1f} KB")

        elif cmd == "memory":
            print_section("Stored User Facts")
            facts = self.chat_engine.memory_mgr.facts
            if not facts:
                print("No facts known yet.\n")
            for k, v in facts.items():
                print(f"{k.capitalize()}\n{v}\n")
                
        elif cmd == "history":
            print_section("Conversation History")
            messages = self.chat_engine.history_mgr.get_recent_messages(10)
            if not messages:
                print("No history found.\n")
            for msg in messages:
                print(f"{msg.role.capitalize()}\n{msg.text}\n")
                
        elif cmd == "summary":
            print_section("Conversation Summary")
            print(f"{self.chat_engine.summary_mgr.get_summary()}\n")
            
        elif cmd == "export":
            print("Export Conversation\n1 Markdown\n2 TXT\n3 JSON")
            choice = input("Choice: ").strip()
            messages = self.chat_engine.history_mgr.get_messages()
            if choice == "1":
                path = Exporter.export_markdown(messages)
                print(f"Exported to {path}\n")
            elif choice == "2":
                path = Exporter.export_txt(messages)
                print(f"Exported to {path}\n")
            elif choice == "3":
                path = Exporter.export_json(messages)
                print(f"Exported to {path}\n")
            else:
                print("Invalid choice.\n")

        elif cmd == "settings":
            print_section("Settings")
            settings = self.chat_engine.settings_mgr.settings
            for k, v in settings.items():
                title = k.replace("_", " ").title()
                print(f"{title}\n{v}\n")
                
        elif cmd == "reset":
            confirm = input("Delete History?\nY/N\n")
            if confirm.lower() == 'y':
                self.chat_engine.history_mgr.clear_history()
                self.chat_engine.memory_mgr.clear_memory()
                self.chat_engine.summary_mgr.update_summary("")
                # Also reset stats
                self.chat_engine.stats_mgr.stats = {
                    "messages": 0, "questions": 0, "responses": 0,
                    "session_duration": 0, "prompt_tokens": 0, "response_tokens": 0,
                    "average_response_time": 0.0, "_total_response_time": 0.0
                }
                self.chat_engine.stats_mgr.save_stats()
                print("\nDeleted.\n")
        else:
            return False # Not a command
            
        return False # Handled command, don't exit
