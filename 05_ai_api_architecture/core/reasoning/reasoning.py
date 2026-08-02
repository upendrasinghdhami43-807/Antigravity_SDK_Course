from dataclasses import dataclass
from core.planner.planner import PlanResult

@dataclass
class ReasoningResult:
    intent: str
    complexity: str
    priority: str
    needs: list[str]

class ReasoningEngine:
    """
    Analyzes intent, complexity, priority, and needs (Phase 2 stub).
    """
    def analyze(self, user_input: str, plan: PlanResult) -> ReasoningResult:
        # Static reasoning for Phase 2
        intent = "General Inquiry"
        if "?" in user_input:
            intent = "Question"
            
        return ReasoningResult(
            intent=intent,
            complexity="Low",
            priority=plan.priority,
            needs=["knowledge"]
        )
