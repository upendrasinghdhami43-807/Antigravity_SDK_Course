# Module 4: Streaming API Pro

This project is **Module 4** of the Antigravity SDK Course. It transforms a standard block-and-wait AI application into a fully asynchronous, real-time streaming application. 

By leveraging Python's `asyncio` framework and the Gemini API's streaming endpoints, this module replicates the exact "live typing" effect seen in professional AI tools like ChatGPT or Claude.

## 🚀 Key Features

- **Asynchronous Architecture**: Built entirely on an `asyncio` event loop for non-blocking I/O.
- **Real-Time Streaming**: Renders chunks of text token-by-token character-by-character the millisecond they arrive over the network.
- **Interruption Handling**: Press `Ctrl+C` mid-stream to instantly cancel the network request, save the generated portion, and return to the prompt without crashing.
- **Streaming Metrics**: Tracks advanced metrics including:
  - Time to First Byte (First-Token Latency)
  - Tokens per second
  - Characters per second
- **Toggle Streaming**: Switch between real-time streaming and synchronous generation using the `/stream` command.

## 📦 File Structure

The application's core logic is heavily decoupled to handle the complex streaming lifecycle:
- `app/stream_manager.py`: Orchestrates the stream lifecycle, tracking latency and managing cancellations.
- `app/stream_renderer.py`: Injects a microscopic delay between characters to ensure a smooth typewriter effect, bypassing chunky network packets.
- `app/stream_buffer.py`: Silently collects chunks in the background to save the final complete string to your persistent history.

## 🛠 Installation & Setup

1. Ensure you are in the `04_streaming_pro` directory.
2. Create and activate a Python virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Configure your API key by creating a `.env` file:
   ```env
   GEMINI_API_KEY=your_api_key_here
   LOG_LEVEL="INFO"
   MAX_HISTORY_TOKENS=4000
   ```

## 🎮 Usage

Start the AI Assistant by running the main module:
```bash
python3 -m app.main
```

### Available Commands
- `/help` - Show all commands
- `/stream on|off` - Toggle the real-time typing effect
- `/stats` - View your streaming metrics (latency and speed)
- `/models` - List and switch between Gemini models
- `/history` - View recent message history
- `/memory` - Display extracted facts about you
- `/export` - Export conversation to Markdown, TXT, or JSON
- `/clear` - Clear the terminal screen
- `/reset` - Delete all history and memory
- `/exit` - Safely exit the application

Available Commands
------------------

/help     - Show this message
/models   - List available models
/model    - Change current model
/stream   - Toggle streaming ON/OFF (e.g. /stream off)
/history  - Display recent message history
/memory   - Display extracted user facts
/summary  - Show the current conversation summary
/token    - Display session token usage
/stats    - Display conversation statistics
/export   - Export conversation history
/settings - Display and modify settings
/clear    - Clear the current screen
/reset    - Reset history and memory
/exit     - Exit the application

#stop response
ctrl+c
