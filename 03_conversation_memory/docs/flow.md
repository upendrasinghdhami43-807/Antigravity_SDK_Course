# Application Flow

## Startup
1. `main.py` initializes `ChatManager`.
2. `ChatManager` instantiates Memory, History, Session, and Summary managers.
3. These managers read their respective `.json` files from disk.

## Conversation Loop
1. User types input.
2. `chat.py` checks if it is a command (e.g. `history`).
3. If not, it requests `ContextBuilder` to build the prompt.
4. `ContextBuilder` combines System Prompt + Memory String + Summary + Recent History.
5. The Prompt is sent to the Gemini SDK in `agent.py`.
6. `agent.py` returns the text response.
7. Both messages are saved to `history.json`.
8. `agent.py` runs `extract_facts()`. If new facts are found, they are appended to `memory.json`.

## Shutdown
1. User types `exit`.
2. Session manager calculates total duration and saves.
3. Program ends.
