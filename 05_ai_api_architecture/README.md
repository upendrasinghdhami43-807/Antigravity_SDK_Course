# AI API Architecture (Phase 2)

An advanced, modular, and event-driven foundation for building autonomous AI agents.

## Features
- **Provider Agnostic:** Modular provider layer.
- **Robust Pipeline:** Planner -> Reasoning -> Context Builder -> Prompt Engine -> Provider -> Parser.
- **Structured Output Engine:** Parses raw LLM text into strictly typed Pydantic models.
- **Prompt Engineering:** Dynamic template and persona injection.
- **State Management:** Session tracking, Token counting, Statistics, Persistent Long-term Memory.

## Installation
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Running
```bash
cp .env.example .env
# Set GEMINI_API_KEY
python -m app.main
```
