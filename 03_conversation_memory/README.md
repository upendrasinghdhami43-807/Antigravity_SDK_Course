# Module 3 - Conversation Memory

## Overview
This project is Module 3 of the Antigravity SDK Course. It implements a persistent AI assistant that can remember previous conversations across sessions, manage conversation size, and extract important facts to store in long-term memory.

## Features
- **Persistent Memory**: Saves history to `data/history.json`.
- **User Fact Extraction**: Automatically extracts and saves facts about the user to `data/memory.json`.
- **Session Tracking**: Tracks start time, duration, and message counts in `data/session.json`.
- **Token Management**: Limits the size of history passed to the model.
- **Commands**: Supports commands like `help`, `clear`, `history`, `memory`, `summary`, `export`, and `reset`.

## Installation

1. Create and activate a virtual environment:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Add your Gemini API Key to the `.env` file:
```
GEMINI_API_KEY="your_actual_api_key"
```

## Usage

Start the AI Assistant by running:
```bash
python3 -m app.main
```

## Folder Structure

- `app/`: Application logic
- `data/`: Persistent JSON storage
- `docs/`: Documentation
- `tests/`: Unit tests
- `logs/`: Application logs
