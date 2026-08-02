from core.provider.provider import Provider
from core.provider.gemini_provider import GeminiProvider
from core.configuration.config import Config

class ProviderFactory:
    """Factory to return the correct provider based on configuration."""
    
    @staticmethod
    def get_provider(config: Config) -> Provider:
        # In the future, we could check config to return OpenAIProvider, etc.
        return GeminiProvider(config)
