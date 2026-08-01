import time
from rich import print
from rich.console import Console
from app.agent import Agent
from app.history import History
from app.logger import logger
from app.utils import clear_terminal

console = Console()

class ChatSession:
    def __init__(self):
        self.history = History()
        try:
            self.agent = Agent()
        except ValueError as e:
            console.print(f"[red]Error: {str(e)}[/red]")
            logger.error(f"Initialization error: {str(e)}")
            exit(1)
        self.message_count = 0
        self.start_time = time.time()

    def display_welcome(self):
        clear_terminal()
        console.print("[cyan]===================================[/cyan]")
        console.print("[bold green]Interactive AI Chat[/bold green]")
        console.print("Type [bold yellow]/exit[/bold yellow], [bold yellow]/quit[/bold yellow], or [bold yellow]/bye[/bold yellow] anytime.")
        console.print("Type [bold yellow]/clear[/bold yellow] to clear terminal.")
        console.print("Type [bold yellow]/reset[/bold yellow] to clear chat history.")
        console.print("Type [bold yellow]/model[/bold yellow] to list and change the model.")
        console.print("Type [bold yellow]/help[/bold yellow] for commands.")
        console.print("[cyan]===================================[/cyan]\n")
        logger.info("Application Started")

    def show_help(self):
        console.print("\n[bold cyan]Available Commands:[/bold cyan]")
        console.print("  [yellow]/exit, /quit, /bye[/yellow] - Stop the chat")
        console.print("  [yellow]/clear[/yellow]             - Clear the terminal screen")
        console.print("  [yellow]/reset[/yellow]             - Erase chat history and start fresh")
        console.print("  [yellow]/model[/yellow]             - Switch AI model")
        console.print("  [yellow]/help[/yellow]              - Show this help message\n")

    def run(self):
        self.display_welcome()
        
        while True:
            try:
                user_input = input("You : ").strip()
            except (KeyboardInterrupt, EOFError):
                break

            if not user_input:
                console.print("[red]Please enter a message.[/red]")
                continue

            lower_input = user_input.lower()
            if lower_input in ['exit', 'quit', 'bye', '/exit', '/quit', '/bye']:
                break
            
            if lower_input in ['clear', '/clear']:
                clear_terminal()
                continue
                
            if lower_input in ['reset', '/reset']:
                self.history.clear()
                self.agent.reset()
                console.print("[green]Chat history cleared! Starting a fresh session.[/green]")
                continue
                
            if lower_input in ['help', '/help']:
                self.show_help()
                continue
                
            if lower_input == '/model':
                categorized_models = self.agent.get_categorized_models()
                all_models = []
                idx = 1
                
                console.print("\n[bold cyan]Available Models:[/bold cyan]")
                for category, models in categorized_models.items():
                    if models:
                        console.print(f"\n[bold magenta]{category}:[/bold magenta]")
                        for m in models:
                            console.print(f"  [yellow]{idx}.[/yellow] {m}")
                            all_models.append(m)
                            idx += 1
                            
                if not all_models:
                    console.print("[red]No models found.[/red]")
                    continue
                
                try:
                    selection = input("\nSelect a model number: ").strip()
                    if not selection:
                        console.print("[yellow]Model selection cancelled.[/yellow]")
                        continue
                    selected_idx = int(selection) - 1
                    if 0 <= selected_idx < len(all_models):
                        selected_model = all_models[selected_idx]
                        self.agent.change_model(selected_model)
                        console.print(f"[green]Successfully switched to model: {selected_model}[/green]")
                    else:
                        console.print("[red]Invalid selection.[/red]")
                except ValueError:
                    console.print("[red]Invalid input. Please enter a number.[/red]")
                except (KeyboardInterrupt, EOFError):
                    console.print("\n[yellow]Model selection cancelled.[/yellow]")
                continue

            self.message_count += 1
            logger.info(f"Question: {user_input}")
            self.history.add_message("User", user_input)

            response = self.agent.ask(user_input)
            
            logger.info(f"Response: {response}")
            self.history.add_message("Agent", response)

            print()
            console.print("[cyan]Agent :[/cyan]")
            console.print(response)
            print()

        self.shutdown()

    def shutdown(self):
        duration = int(time.time() - self.start_time)
        console.print(f"\n[green]Goodbye! Chat ended.[/green]")
        console.print(f"[dim]Session stats: {self.message_count} messages sent in {duration} seconds.[/dim]")
        logger.info("Application Exit")
