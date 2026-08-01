"""
Module 6 — Structured Output
--------------------------------
Free-form text is fine for a chat window, but useless if you want to save the
agent's answer into a database or feed it into another part of your app.

response_schema lets you describe the EXACT shape you want back -- as a
Pydantic model -- and the agent returns data matching that shape instead of a
paragraph. `await response.structured_output()` gives you back a parsed,
validated result instead of raw text.

Run:
    python 06_structured_output.py
"""

import asyncio

from dotenv import load_dotenv
from pydantic import BaseModel
from google.antigravity import Agent, LocalAgentConfig

load_dotenv()


class TaskItem(BaseModel):
    title: str
    priority: str  # "low" | "medium" | "high"
    estimated_hours: float


class TaskList(BaseModel):
    tasks: list[TaskItem]


async def main() -> None:
    config = LocalAgentConfig(
        system_instructions=(
            "You turn a student's messy, informal task list into clean, "
            "structured data. Estimate hours realistically."
        ),
        response_schema=TaskList,
    )

    async with Agent(config) as agent:
        response = await agent.chat(
            "I need to finish the Laravel API for my EpayNepal capstone, "
            "revise my DBMS notes before the exam, and fix a crash in my "
            "Flutter calculator app."
        )
        result = await response.structured_output()

        # `result` is a TaskList instance (or dict, depending on SDK version) --
        # this is now real structured data you could save to a database.
        for task in result.tasks:
            print(f"- [{task.priority.upper()}] {task.title} (~{task.estimated_hours}h)")


if __name__ == "__main__":
    asyncio.run(main())
