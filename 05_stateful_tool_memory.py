"""
Module 5 — Stateful Tools with ToolContext
---------------------------------------------
Module 4's tools were "pure" -- no memory between calls. Real applications
often need a tool that remembers data across the conversation: a running
total, a cache, a to-do list.

ToolContext gives a tool exactly that: a small per-conversation key-value
store. Add a parameter typed as `ToolContext` to any tool function and the
SDK injects it automatically -- the model never sees this parameter, so it
never tries to fill it in itself.

Example here: a tiny expense tracker (the same underlying idea you'd want
inside something like EpayNepal, just simplified to plain Python state).

Run:
    python 05_stateful_tool_memory.py

Note: this SDK is a Research Preview and ToolContext's exact method
signatures can shift between releases -- if get_state/set_state behaves
differently on your installed version, check the SDK's own docstrings with
`help(ToolContext)`.
"""

import asyncio

from dotenv import load_dotenv
from google.antigravity import Agent, LocalAgentConfig
from google.antigravity.tools.tool_context import ToolContext

load_dotenv()


def add_expense(item: str, amount: float, context: ToolContext) -> str:
    """Record a new expense with an item name and an amount in NPR."""
    expenses = context.get_state("expenses") or []
    expenses.append({"item": item, "amount": amount})
    context.set_state("expenses", expenses)
    return f"Recorded: {item} — Rs. {amount}"


def get_total(context: ToolContext) -> str:
    """Return the running total of every expense recorded so far this session."""
    expenses = context.get_state("expenses") or []
    total = sum(e["amount"] for e in expenses)
    return f"Total spent so far: Rs. {total} across {len(expenses)} item(s)."


async def main() -> None:
    config = LocalAgentConfig(
        system_instructions="You are a personal expense tracker for a student.",
        tools=[add_expense, get_total],
    )

    async with Agent(config) as agent:
        r1 = await agent.chat("I spent 150 on tea and 400 on a bus ticket today.")
        print("Agent:", await r1.text())

        r2 = await agent.chat("How much have I spent in total so far?")
        print("Agent:", await r2.text())


if __name__ == "__main__":
    asyncio.run(main())
