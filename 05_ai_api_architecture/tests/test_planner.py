from core.planner.planner import Planner

def test_planner():
    planner = Planner()
    plan = planner.create_plan("hello")
    
    assert plan.goal is not None
    assert plan.need_tools is False
    assert plan.priority == "Normal"
