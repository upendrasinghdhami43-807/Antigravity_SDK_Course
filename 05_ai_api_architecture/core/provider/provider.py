from abc import ABC, abstractmethod
from typing import Generator, Union, Any

class Provider(ABC):
    """Abstract interface for all model providers."""
    
    @abstractmethod
    def generate_content(self, prompt: str) -> str:
        """Generate full content synchronously."""
        pass
        
    @abstractmethod
    def generate_content_stream(self, prompt: str) -> Generator[str, None, None]:
        """Generate content as a stream of chunks."""
        pass
