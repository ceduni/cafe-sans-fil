from typing import List, Optional

from pydantic import BaseModel, Field

from app.cafe.schemas import CafeOut


class SearchCreate(BaseModel):
    query: str


class SearchOut(BaseModel):
    cafes: Optional[List[CafeOut]] = None
