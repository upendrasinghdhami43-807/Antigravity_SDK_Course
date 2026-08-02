import sys
from rich.console import Console
from core.engine.engine import Engine

class TerminalUI:
    """Interactive terminal loop, prompt, display."""
    def __init__(self, engine: Engine):
        self.engine = engine
        self.console = Console()

    def show_startup_screen(self):
        self.console.print("====================================================", style="bold blue")
        self.console.print("AI AGENT FRAMEWORK", style="bold white")
        self.console.print("Module 05 · Architecture Framework", style="bold white")
        self.console.print("====================================================", style="bold blue")
        self.console.print(f"Model      {self.engine.config.default_model}")
        self.console.print("Provider   Google GenAI SDK")
        self.console.print("Memory     Enabled")
        self.console.print("History    Enabled")
        self.console.print("Logger     Enabled")
        self.console.print("Session    Running")
        self.console.print("Type /help for commands")
        self.console.print("====================================================", style="bold blue")

    def run(self):
        self.show_startup_screen()
        while True:
            try:
                user_input = self.console.input("\n[bold green]You >[/bold green] ")
                if not user_input.strip():
                    continue

                if self.engine.command_router.route(user_input):
                    continue

                self.console.print("\n[dim]Agent is thinking...[/dim]")
                response = self.engine.controller.process_request(user_input)
                self.console.print(f"\n[bold blue]Agent >[/bold blue] {response}")

            except KeyboardInterrupt:
                self.console.print("\nExiting...")
                self.engine.shutdown()
                sys.exit(0)
            except Exception as e:
                self.console.print(f"[bold red]Error: {e}[/bold red]")
