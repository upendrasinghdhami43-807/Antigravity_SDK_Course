from google import genai
from typing import Generator
from core.provider.provider import Provider
from core.configuration.config import Config
from core.exceptions.framework_exceptions import ProviderError
import time

class GeminiProvider(Provider):
    """Concrete implementation for Google Gen AI SDK."""
    def __init__(self, config: Config):
        self.config = config
        try:
            self.client = genai.Client(api_key=config.gemini_api_key)
        except Exception as e:
            raise ProviderError(f"Failed to initialize Gemini Client: {e}")

    def generate_content(self, prompt: str) -> str:
        try:
            response = self.client.models.generate_content(
                model=self.config.default_model,
                contents=prompt,
                config=genai.types.GenerateContentConfig(
                    temperature=self.config.temperature
                )
            )
            return response.text
        except Exception as e:
            raise ProviderError(f"Gemini generation failed: {e}")

    def generate_content_stream(self, prompt: str) -> Generator[str, None, None]:
        try:
            response = self.client.models.generate_content_stream(
                model=self.config.default_model,
                contents=prompt,
                config=genai.types.GenerateContentConfig(
                    temperature=self.config.temperature
                )
            )
            for chunk in response:
                yield chunk.text
        except Exception as e:
            raise ProviderError(f"Gemini stream failed: {e}")
