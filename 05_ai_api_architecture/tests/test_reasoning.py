from core.planner.planner import PlanResult
from core.reasoning.reasoning import ReasoningEngine

def test_reasoning():
    engine = ReasoningEngine()
    plan = PlanResult("goal", False, False, True, True, "Normal")
    
    res1 = engine.analyze("Hello there", plan)
    assert res1.intent == "General Inquiry"
    
    res2 = engine.analyze("What is Python?", plan)
    assert res2.intent == "Question"
