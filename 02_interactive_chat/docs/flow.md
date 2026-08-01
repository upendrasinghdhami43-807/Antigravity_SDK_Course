# Execution Flow

1. **Start**: User runs `python app/main.py`.
2. **Init**: `main.py` instantiates `ChatSession`.
3. **Setup**: `ChatSession` initializes `History` and `Agent`.
4. **Agent Init**: `Agent` loads `API_KEY` and initializes Gemini client.
5. **Welcome**: `ChatSession` clears terminal and displays welcome screen.
6. **Loop**:
    a. Wait for user input.
    b. If `exit/quit/bye`, break loop.
    c. Send input to `Agent.ask()`.
    d. `Agent` calls Gemini API.
    e. Print response.
    f. Save to `History`.
    g. Repeat.
7. **Shutdown**: Print session stats and exit.
