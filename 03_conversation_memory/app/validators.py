def is_valid_model(model_name: str, available_models: list) -> bool:
    """Validates if the provided model name is in the available models list."""
    if model_name in available_models:
        return True
    
    # Check if they forgot 'models/' prefix but the list has it
    if f"models/{model_name}" in available_models:
        return True
    
    return False

def validate_setting_value(key: str, value: str) -> bool:
    """Validates a setting value based on the key."""
    if key in ["theme", "streaming", "auto_save"]:
        return value.lower() in ["enabled", "disabled", "dark", "light"]
    
    if key in ["summary_limit", "context_limit"]:
        return value.isdigit()
        
    return True
