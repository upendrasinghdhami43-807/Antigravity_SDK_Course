"""
Module 7 — Built-in Tools & Safety Policies
-----------------------------------------------
LocalAgentConfig() enables a set of BUILT-IN tools automatically -- you don't
register these yourself the way you did in Module 4:

  Read-only (safe by default):  list_directory, view_file, find_file, grep_search
  Write / system-changing:      run_command, edit_file, create_file, ...

Read-only tools work immediately with zero extra setup -- see Part A below.

Write tools are BLOCKED by default ("deny by default"). If you try to give the
agent write access without an explicit policy, the SDK raises a ValueError on
startup rather than silently letting an LLM run arbitrary shell commands on
your machine. Part B shows the minimum policy needed to unblock one specific
tool, with a human-in-the-loop confirmation for anything riskier.

Run:
    python 07_builtin_tools_and_safety.py
"""

import asyncio

from dotenv import load_dotenv
from google.antigravity import Agent, LocalAgentConfig
from google.antigravity.hooks.policy import allow, ask_user, deny

load_dotenv()


async def part_a_read_only() -> None:
    """No policy needed -- read-only built-in tools are safe by default."""
    config = LocalAgentConfig(
        system_instructions="You can inspect the current project folder."
    )
    async with Agent(config) as agent:
        response = await agent.chat("What files are in the current directory?")
        print("Agent:", await response.text())


async def part_b_write_with_policy() -> None:
    """Write tools require an explicit, declarative safety policy."""

    def confirm_with_terminal(tool_name: str, arguments: dict) -> bool:
        answer = input(f"Allow agent to run '{tool_name}' with {arguments}? [y/N]: ")
        return answer.strip().lower() == "y"

    policies = [
        deny("*"),  # block everything by default
        allow("list_directory"),  # reading is always fine
        allow("view_file"),
        ask_user("run_command", handler=confirm_with_terminal),  # ask a human first
    ]

    config = LocalAgentConfig(
        system_instructions="You are a careful coding assistant.",
        policies=policies,
    )

    async with Agent(config) as agent:
        response = await agent.chat("Run `python --version` and tell me the result.")
        print("Agent:", await response.text())


async def main() -> None:
    print("--- Part A: read-only built-in tools ---")
    await part_a_read_only()

    print("\n--- Part B: write tool gated behind a policy ---")
    await part_b_write_with_policy()


if __name__ == "__main__":
    asyncio.run(main())
