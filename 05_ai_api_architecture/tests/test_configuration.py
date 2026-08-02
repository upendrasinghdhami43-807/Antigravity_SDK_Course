import os
import pytest
from core.configuration.config import Config, load_config
from core.exceptions.framework_exceptions import ConfigurationError

def test_load_configuration_success(monkeypatch):
    monkeypatch.setattr("core.configuration.config.load_dotenv", lambda *args, **kwargs: None)
    monkeypatch.setenv("GEMINI_API_KEY", "test_key")
    monkeypatch.setenv("DEFAULT_MODEL", "test-model")
    monkeypatch.setenv("TEMPERATURE", "0.5")
    
    config = Config()
    assert config.gemini_api_key == "test_key"
    assert config.default_model == "test-model"
    assert config.temperature == 0.5
    
def test_load_configuration_missing_key(monkeypatch):
    monkeypatch.setattr("core.configuration.config.load_dotenv", lambda *args, **kwargs: None)
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    with pytest.raises(ConfigurationError, match="GEMINI_API_KEY is required"):
        Config()
