"""
Module 1 — Hello Agent
-----------------------
The smallest possible Antigravity SDK program: send one message, print one reply.

Run:
    python 01_hello_agent.py
"""

import asyncio

from dotenv import load_dotenv
from google.antigravity import Agent, LocalAgentConfig

load_dotenv()  # reads GEMINI_API_KEY from your .env file


async def main() -> None:
    # LocalAgentConfig describes HOW the agent should behave.
    # system_instructions is like giving the agent a job description.
    config = LocalAgentConfig(
        system_instructions=(
            "You are a friendly, concise tutor helping a computer engineering "
            "student in Nepal who is new to AI agent development."
        )
    )

    # `async with` opens the agent session and guarantees it's cleanly shut
    # down afterwards, even if something goes wrong inside the block.
    async with Agent(config) as agent:
        response = await agent.chat("Hello! Introduce yourself in two short lines.")
        print("Agent:", await response.text())


if __name__ == "__main__":
    asyncio.run(main())
