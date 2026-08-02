"""
Exception hierarchy for the AI Agent Framework.
"""

class FrameworkError(Exception):
    """Base exception for all framework errors."""
    pass

class ConfigurationError(FrameworkError):
    """Raised when there are missing or invalid configuration values (e.g. .env)."""
    pass

class ProviderError(FrameworkError):
    """Raised when the Model Provider SDK, network, or auth fails."""
    pass

class PromptValidationError(FrameworkError):
    """Raised when Module 06 (Prompt Engine) validation fails."""
    pass

class StructuredOutputError(FrameworkError):
    """Raised when Module 07 fails to parse/validate the output after retries."""
    pass

class MemoryError(FrameworkError):
    """Raised when memory read/write operations fail."""
    pass

class HistoryError(FrameworkError):
    """Raised when history read/write operations fail."""
    pass

class ToolExecutionError(FrameworkError):
    """Raised when a tool execution fails."""
    pass
