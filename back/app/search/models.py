from typing import List, Optional

from pydantic import BaseModel, Field

from app.cafe.models import CafeViewOut


class SearchCreate(BaseModel):
    query: str


class SearchOut(BaseModel):
    cafes: Optional[List[CafeViewOut]] = None
