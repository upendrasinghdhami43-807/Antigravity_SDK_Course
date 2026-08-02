def print_header(title: str):
    print(f"\n{'=' * 28}")
    print(f"{title}")
    print(f"{'=' * 28}\n")

def print_section(title: str):
    print(f"\n{title}")
    print(f"{'-' * len(title)}\n")
    
def print_key_value(key: str, value: str):
    print(f"{key}\n{value}\n")

def print_help():
    print_section("Available Commands")
    commands = [
        "/help     - Show this message",
        "/models   - List available models",
        "/model    - Change current model",
        "/stream   - Toggle streaming ON/OFF (e.g. /stream off)",
        "/history  - Display recent message history",
        "/memory   - Display extracted user facts",
        "/summary  - Show the current conversation summary",
        "/token    - Display session token usage",
        "/stats    - Display conversation statistics",
        "/export   - Export conversation history",
        "/settings - Display and modify settings",
        "/clear    - Clear the current screen",
        "/reset    - Reset history and memory",
        "/exit     - Exit the application"
    ]
    for cmd in commands:
        print(cmd)
    print()
