from pydantic import BaseModel
from typing import Optional

class BaseResponse(BaseModel):
    """Base schema for structured responses."""
    pass

class BaseStatistics(BaseModel):
    """Statistics schema to append to structured responses if needed."""
    prompt_tokens: int = 0
    completion_tokens: int = 0
    response_time_ms: float = 0.0
