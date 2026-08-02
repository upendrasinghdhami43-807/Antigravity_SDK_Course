"""
Module 2 — Interactive Chat (with automatic memory)
----------------------------------------------------
A terminal chat loop. Because every agent.chat() call below happens INSIDE the
same `async with Agent(...) as agent:` block, the agent automatically remembers
everything said earlier in the session — try telling it your name, then a few
messages later ask "what's my name?".

Run:
    python 02_interactive_chat.py

Type 'exit' or 'quit' to stop.
"""

import asyncio

from dotenv import load_dotenv
from google.antigravity import Agent, LocalAgentConfig

load_dotenv()


async def main() -> None:
    config = LocalAgentConfig(
        system_instructions="You are a helpful terminal assistant. Keep answers short."
    )

    print("Antigravity Chat — type 'exit' or 'quit' to stop.\n")

    async with Agent(config) as agent:
        while True:
            user_input = input("You: ").strip()

            if user_input.lower() in ("exit", "quit"):
                print("Agent: Goodbye!")
                break

            if not user_input:
                continue

            response = await agent.chat(user_input)
            print("Agent:", await response.text())


if __name__ == "__main__":
    asyncio.run(main())
