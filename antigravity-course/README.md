# Google Antigravity SDK — Beginner-to-Working Course

This is a hands-on companion to the curriculum you pasted in. Before writing any code I
checked the real SDK docs, PyPI page, and GitHub repo, because this SDK launched in
**May 2026** — after most model training data — and a few details in your original outline
don't match what actually ships. Corrections first, then the guide.

## What was wrong in your original plan

| Your doc said | Reality |
|---|---|
| `pip install antigravity google` | The real package is **`pip install google-antigravity`** |
| Generic "SDK" with `LocalAgentConfig`, `agent.chat()` etc. | These class names are *actually correct* — good sign the doc was based on real docs at some point, just with a broken install line |
| Works on any OS | Pre-built wheels only exist for **Linux and macOS** (you're on Xubuntu, so you're fine) |
| — | Needs **Python 3.10+**, not just "Python 3" |
| — | It ships a compiled Go binary ("localharness") inside the wheel — you cannot `git clone` the repo and run it, it must come from `pip` |
| — | It's a **Research Preview / Alpha**. APIs can change between versions. |

Status: this is a real, working Google product (`google.antigravity`), built on top of
Gemini, and it's the same agent engine that powers the Antigravity IDE and CLI. Good
choice to learn, just needs the corrected instructions below.

---

## Part 0 — From an empty folder to a working agent

Everything below assumes an **empty folder** and only basic Python knowledge (loops,
functions, `if`, and that you've built something like a calculator before — we'll reuse
that idea in Module 4).

### Step 1 — Make the folder and enter it

```bash
mkdir antigravity-course
cd antigravity-course
```

### Step 2 — Create and activate a virtual environment

A virtual environment is just an isolated copy of Python + its packages, so this
project's libraries don't clash with any other project on your machine.

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Your terminal prompt should now show `(.venv)` at the start of the line. From now on,
every `pip install` only affects this project.

### Step 3 — Install the SDK

```bash
pip install --upgrade pip
pip install google-antigravity python-dotenv pydantic
```

- `google-antigravity` — the SDK itself (includes the compiled agent runtime)
- `python-dotenv` — lets us load the API key from a `.env` file instead of hardcoding it
- `pydantic` — used later for structured output (Module 6)

### Step 4 — Get a Gemini API key

1. Go to Google AI Studio and create a free API key.
2. Copy `.env.example` in this folder to `.env`:
   ```bash
   cp .env.example .env
   ```
3. Open `.env` and paste your key in place of the placeholder.

Never commit `.env` to Git — `.gitignore` already excludes it.

### Step 5 — Verify the install

```bash
python -c "from google.antigravity import Agent, LocalAgentConfig; print('SDK OK')"
```

If that prints `SDK OK`, you're ready.

---

## Part 1 — Project structure

```
antigravity-course/
├── .venv/                      # virtual environment (never edit by hand)
├── .env                        # your real API key (never commit this)
├── .env.example                # template teammates can copy
├── requirements.txt            # exact package list
├── 01_hello_agent.py           # Module 1: one-shot request/response
├── 02_interactive_chat.py      # Module 2: terminal chat loop, with memory
├── 03_streaming_chat.py        # Module 3: tokens appear as they're generated
├── 04_custom_tools.py          # Module 4: agent calls your own Python functions
├── 05_stateful_tool_memory.py  # Module 5: a tool that remembers data across turns
├── 06_structured_output.py     # Module 6: force the agent to return typed JSON
└── 07_builtin_tools_and_safety.py  # Module 7: filesystem/shell tools + safety policy
```

Run every file the same way, from inside the activated venv:

```bash
python 01_hello_agent.py
```

---

## Part 2 — The core concept you need before anything else

Every script follows the same shape:

```python
import asyncio
from google.antigravity import Agent, LocalAgentConfig

async def main():
    config = LocalAgentConfig(...)     # 1. describe the agent
    async with Agent(config) as agent: # 2. open a session (starts the runtime)
        response = await agent.chat("...")   # 3. send a message
        print(await response.text())         # 4. read the reply

asyncio.run(main())
```

Why `async`/`await`? The agent talks to a background process over a local connection,
and `await` just means "pause here until that reply comes back, without freezing the
whole program." You don't need to master `asyncio` — just always wrap your code in an
`async def main()` and call `asyncio.run(main())` at the bottom, exactly like every file
here does.

The important part: **one `async with Agent(config) as agent:` block = one conversation
session.** Every `agent.chat()` call inside that same block remembers everything said
before it. That's it — that's "conversation memory," no extra code needed (see Module 2).

---

## Module 1 — Hello Agent (`01_hello_agent.py`)

The absolute minimum: send one message, print one reply. This is your "Hello, World."

## Module 2 — Interactive Chat (`02_interactive_chat.py`)

A `while True` loop reading from `input()`, same idea as a basic terminal chatbot.
Because the loop stays inside one `async with Agent(...) as agent:` block, the agent
remembers earlier turns automatically — ask it your name, tell it your name, then ask
again a few turns later.

## Module 3 — Streaming (`03_streaming_chat.py`)

Instead of waiting for the full answer, you print each token as it arrives — the
"typing" effect you see in ChatGPT-style apps. `response` itself is an async iterator.

## Module 4 — Custom Tools (`04_custom_tools.py`)

This is where it stops being "just a chatbot." You write plain Python functions —
literally the same style as the calculator you already built — and hand them to the
agent. The agent decides when to call them and with what arguments; your function's
docstring is what tells it what the function does.

## Module 5 — Stateful Tools (`05_stateful_tool_memory.py`)

A step up from Module 4: tools that remember data across multiple turns using
`ToolContext` (a per-conversation key-value store). Example used here: a small expense
tracker, similar in spirit to features you'd want in something like EpayNepal.

## Module 6 — Structured Output (`06_structured_output.py`)

Instead of getting back a paragraph of text, you define a Pydantic model describing the
exact shape of data you want (fields, types), and the agent returns validated JSON that
matches it. Useful any time an agent's output needs to plug into another system — a
database, an API, a UI.

## Module 7 — Built-in Tools & Safety Policies (`07_builtin_tools_and_safety.py`)

The SDK ships built-in tools for reading files, listing directories, and running shell
commands — no registration needed. Read-only tools work immediately. Anything that can
*change* your system (`run_command`, `edit_file`, `create_file`) is blocked by default
until you explicitly configure a safety policy. This module shows both the read-only
case and how the policy system works.

---

## Troubleshooting

- **`ImportError: cannot import name 'Agent'`** → you're not inside the venv, or the
  install failed. Run `source .venv/bin/activate` again, then reinstall.
- **Auth errors** → confirm `.env` has `GEMINI_API_KEY=...` with no quotes, and that you
  actually ran `pip install python-dotenv` and call `load_dotenv()` (already done at the
  top of every script here).
- **`ValueError` on startup mentioning policies** → you gave the agent a "write" tool
  (or an MCP server) without a safety policy. See Module 7.
- **Nothing happens / hangs** → check your internet connection; the SDK talks to Gemini
  over the network even though the harness itself runs locally.

## Where to go next (Phase 2+ from your original roadmap)

Once modules 1–7 feel comfortable, the same patterns extend to:
- **MCP servers** — connect the agent to Slack, GitHub, Postgres, etc. via
  `LocalAgentConfig(mcp_servers=[...])`
- **Lifecycle hooks** — intercept every tool call for logging/auditing
- **Sub-agents** — one agent delegating tasks to other agents (your "multi-agent team"
  idea from Phase 6)
- **Remote/cloud deployment** — the same code can target Google Cloud instead of your
  laptop

The official examples directory (`google-antigravity/antigravity-sdk-python` on GitHub,
under `examples/`) has runnable, single-file demos for every one of these — that's the
best next stop once you've built modules 1–7 yourself.
