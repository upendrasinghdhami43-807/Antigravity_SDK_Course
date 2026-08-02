import pytest
from core.provider.provider import Provider
from core.provider.provider_factory import ProviderFactory
from core.configuration.config import Config
from core.exceptions.framework_exceptions import ProviderError
from typing import Generator

class FakeProvider(Provider):
    def generate_content(self, prompt: str) -> str:
        if "fail" in prompt:
            raise ProviderError("Simulated failure")
        return "fake response"
        
    def generate_content_stream(self, prompt: str) -> Generator[str, None, None]:
        yield "fake stream"

def test_provider_factory(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "test_key")
    config = Config()
    provider = ProviderFactory.get_provider(config)
    assert provider is not None
    
def test_fake_provider_success():
    provider = FakeProvider()
    assert provider.generate_content("hello") == "fake response"
    
def test_fake_provider_error():
    provider = FakeProvider()
    with pytest.raises(ProviderError):
        provider.generate_content("fail")
