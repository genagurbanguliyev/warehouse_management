from datetime import datetime
from typing import List, Any

from pydantic import BaseModel, Field

from app.util.schema import optional


@optional()
class MessageResponseBase(BaseModel):
    status: int
    message: str
    timestamp: str | datetime


@optional()
class FindBaseSchema(BaseModel):
    ordering: str | None = Field("-id")
    query: str | None = Field(None)
    limit: int | str
    page: int


class FindResultSchema(BaseModel):
    data: List[Any]
    total: int
