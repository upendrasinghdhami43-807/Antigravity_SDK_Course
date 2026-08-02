# Architecture

The application is structured into modular components:

- **main.py**: Entry point. Starts the `ChatSession`.
- **chat.py**: Manages the UI, console interaction, and the main `while` loop.
- **agent.py**: Manages the Gemini API connection and conversation context.
- **history.py**: Responsible for logging chat messages to `data/history.json`.
- **logger.py**: Configures application-level file logging.
- **utils.py**: Helper functions like clearing the terminal.
