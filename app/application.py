from core.engine.engine import Engine
from app.terminal import TerminalUI

class Application:
    """Constructs every framework component."""
    def __init__(self):
        self.engine = Engine()
        self.terminal = TerminalUI(self.engine)

    def run(self):
        self.terminal.run()
