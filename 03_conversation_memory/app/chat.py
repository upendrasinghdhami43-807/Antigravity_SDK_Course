import sys
from app.agent import Agent
from app.history import HistoryManager
from app.memory import MemoryManager
from app.session import SessionManager
from app.summarizer import SummaryManager
from app.context import ContextBuilder
from app.logger import get_logger

logger = get_logger("Chat")

class ChatManager:
    def __init__(self):
        self.history_mgr = HistoryManager()
        self.memory_mgr = MemoryManager()
        self.session_mgr = SessionManager()
        self.summary_mgr = SummaryManager()
        
        self.context_builder = ContextBuilder(
            self.history_mgr,
            self.memory_mgr,
            self.summary_mgr
        )
        
        self.agent = Agent()

    def process_command(self, user_input: str) -> bool:
        cmd = user_input.lower().strip()
        
        if cmd == "exit" or cmd == "quit":
            print("\nSaving session and exiting. Goodbye!")
            return True
            
        elif cmd == "help":
            print("\nAvailable commands:")
            print("  help    - Show this message")
            print("  clear   - Clear the current screen")
            print("  history - Display recent message history")
            print("  summary - Show the current conversation summary")
            print("  memory  - Display extracted user facts")
            print("  reset   - Reset history and memory")
            print("  export  - Export history to markdown")
            print("  exit    - Exit the application")
            
        elif cmd == "clear":
            print('\033[2J\033[H', end='') # ANSI escape to clear screen
            
        elif cmd == "history":
            messages = self.history_mgr.get_recent_messages(10)
            print("\n--- Recent History ---")
            if not messages:
                print("No history found.")
            for msg in messages:
                print(f"{msg.role.capitalize()}: {msg.text}")
            print("----------------------")
            
        elif cmd == "summary":
            print("\n--- Current Summary ---")
            print(self.summary_mgr.get_summary())
            print("-----------------------")
            
        elif cmd == "memory":
            print("\n--- User Memory ---")
            print(self.memory_mgr.get_memory_string())
            print("-------------------")
            
        elif cmd == "reset":
            confirm = input("Are you sure you want to delete all history and memory? (y/n): ")
            if confirm.lower() == 'y':
                self.history_mgr.clear_history()
                self.memory_mgr.clear_memory()
                self.summary_mgr.update_summary("")
                print("History and memory reset.")
                
        elif cmd == "export":
            messages = self.history_mgr.get_messages()
            try:
                with open("conversation_export.md", "w") as f:
                    f.write("# Conversation Export\n\n")
                    for msg in messages:
                        f.write(f"**{msg.role.capitalize()}**:\n{msg.text}\n\n")
                print("Exported to conversation_export.md")
            except Exception as e:
                print(f"Failed to export: {e}")
                
        else:
            return False # Not a command
            
        return False # Handled command, don't exit

    def build_prompt(self, user_input: str) -> str:
        sys_prompt = self.context_builder.build_system_prompt()
        context_msgs = self.context_builder.get_context_messages()
        
        # We need to construct a single string prompt for Gemini
        # Alternatively we could use Gemini's ChatSession, but the roadmap 
        # specifically asks for a ContextBuilder that combines everything into "One Prompt"
        
        prompt_parts = [sys_prompt, "\n--- Recent Conversation ---"]
        for msg in context_msgs:
            prompt_parts.append(f"{msg.role.capitalize()}: {msg.text}")
            
        prompt_parts.append(f"\nUser: {user_input}")
        prompt_parts.append("Assistant:")
        
        return "\n".join(prompt_parts)

    def chat_loop(self):
        print("AI Assistant started. Type 'help' for commands, 'exit' to quit.")
        
        while True:
            try:
                user_input = input("\nYou: ")
                if not user_input.strip():
                    continue
                
                # Check for commands
                if self.process_command(user_input):
                    break
                    
                # Build context and prompt
                full_prompt = self.build_prompt(user_input)
                
                # Get response
                print("Assistant: ", end="", flush=True)
                response_text = self.agent.generate_response(full_prompt)
                print(response_text)
                
                # Update Session
                self.session_mgr.increment_message_count()
                
                # Update History
                self.history_mgr.append_message("user", user_input)
                self.history_mgr.append_message("assistant", response_text)
                
                # Extract Memory Facts in the background (or synchronously here)
                new_facts = self.agent.extract_facts(user_input, response_text)
                if new_facts:
                    self.memory_mgr.update_facts(new_facts)
                    
                # (Optional) Token summarization logic would go here if threshold is met
                
            except KeyboardInterrupt:
                print("\nExiting...")
                break
            except Exception as e:
                logger.error(f"Unexpected error in chat loop: {e}")
                print(f"\nAn error occurred: {e}")
