from core.prompt.persona_manager import PersonaManager

def test_persona_manager():
    manager = PersonaManager()
    assert manager.get_persona() is None
    
    manager.set_persona("python_teacher")
    assert manager.get_persona() == "python_teacher"
