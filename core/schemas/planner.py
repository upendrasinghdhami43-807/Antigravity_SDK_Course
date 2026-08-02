from pydantic import BaseModel

class PlannerResponse(BaseModel):
    goal: str
    intent: str
    priority: str
    need_tools: bool
    need_memory: bool
    need_search: bool
    complexity: str
