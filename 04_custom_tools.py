"""
Module 4 — Custom Tools
--------------------------
This is where an agent stops being "just a chatbot" and starts being able to DO
things. You write plain Python functions -- the same style you'd use for a
basic calculator -- and hand them to the agent via LocalAgentConfig(tools=[...]).

Two things matter a lot here:
1. Type hints (e.g. `a: float`) tell the agent what kind of arguments to pass.
2. The docstring tells the agent WHEN to use the function. Write it like you're
   explaining the function to a teammate, not just to Python.

The agent decides on its own when a tool is needed and what arguments to call
it with -- you never call these functions directly yourself.

Run:
    python 04_custom_tools.py
"""

import asyncio

from dotenv import load_dotenv
from google.antigravity import Agent, LocalAgentConfig

load_dotenv()


def add(a: float, b: float) -> float:
    """Add two numbers together and return the sum."""
    return a + b


def multiply(a: float, b: float) -> float:
    """Multiply two numbers together and return the product."""
    return a * b


def divide(a: float, b: float) -> float:
    """Divide a by b and return the result. Raises an error if b is zero."""
    if b == 0:
        raise ValueError("Cannot divide by zero.")
    return a / b


async def main() -> None:
    config = LocalAgentConfig(
        system_instructions=(
            "You are a calculator assistant. Always use the provided tools for "
            "any arithmetic instead of computing it yourself, and show your work."
        ),
        tools=[add, multiply, divide],
    )

    async with Agent(config) as agent:
        response = await agent.chat(
            "What is (23 * 4) + 17? Also, what happens if I try to divide 100 by 0?"
        )
        print("Agent:", await response.text())


if __name__ == "__main__":
    asyncio.run(main())
