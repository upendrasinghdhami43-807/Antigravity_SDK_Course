from dataclasses import dataclass

@dataclass
class PlanResult:
    goal: str
    need_tools: bool
    need_search: bool
    need_memory: bool
    need_history: bool
    priority: str

class Planner:
    """
    Decides what should happen (Phase 2 stub: answer directly).
    """
    def create_plan(self, user_input: str) -> PlanResult:
        # For Phase 2, we just return a static plan that asks to answer directly.
        # Future phases will use LLM here to decide.
        return PlanResult(
            goal="Provide a helpful and structured response.",
            need_tools=False,
            need_search=False,
            need_memory=True,
            need_history=True,
            priority="Normal"
        )
