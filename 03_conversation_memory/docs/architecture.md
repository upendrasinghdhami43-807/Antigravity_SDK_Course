# Architecture

## Component Overview

- **`main.py`**: Entry point.
- **`chat.py`**: Manages the CLI loop and routing commands.
- **`agent.py`**: Wraps the Gemini SDK. Responsible for generating responses, extracting facts, and summarizing.
- **`context.py`**: Builds the final prompt combining system instructions, history, memory, and the new query.
- **`history.py`**: Manages the raw log of messages (`history.json`).
- **`memory.py`**: Manages the extracted facts dictionary (`memory.json`).
- **`session.py`**: Tracks metadata for the current interaction (`session.json`).

## Data Flow

User Input -> ChatManager -> Check Commands
If not command -> ContextBuilder -> Agent -> Response -> Screen
Then -> Update History -> Agent Extracts Facts -> Update Memory
