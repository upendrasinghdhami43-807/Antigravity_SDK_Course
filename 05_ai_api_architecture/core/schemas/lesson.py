from pydantic import BaseModel
from typing import List, Optional
from core.schemas.response import BaseResponse

class LessonResponse(BaseResponse):
    title: str
    difficulty: str
    objectives: List[str]
    topics: List[str]
    summary: str
    examples: List[str] = []
    exercises: List[str] = []
