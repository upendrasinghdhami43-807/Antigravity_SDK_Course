"""
Module 3 — Streaming
----------------------
Instead of waiting for the whole reply and printing it in one go, we print each
token the moment it arrives — the "typing" effect you see in chat apps.

`response` (the object returned by agent.chat()) is itself an async iterator:
looping over it with `async for` yields text tokens as strings.

Run:
    python 03_streaming_chat.py
"""

import asyncio

from dotenv import load_dotenv
from google.antigravity import Agent, LocalAgentConfig

load_dotenv()


async def main() -> None:
    config = LocalAgentConfig(
        system_instructions="You are a concise assistant that explains things clearly."
    )

    async with Agent(config) as agent:
        response = await agent.chat(
            "Explain what a Python virtual environment is, in exactly 4 sentences."
        )

        print("Agent: ", end="", flush=True)
        async for token in response:
            print(token, end="", flush=True)
        print()  # final newline

        # Bonus: after the stream finishes, usage_metadata tells you how many
        # tokens the turn cost — useful once you start caring about API usage.
        print("\n[tokens used this turn]:", response.usage_metadata)


if __name__ == "__main__":
    asyncio.run(main())
