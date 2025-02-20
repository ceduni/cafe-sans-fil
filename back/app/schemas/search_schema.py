from typing import List, Optional

from pydantic import BaseModel, Field

from app.schemas.cafe_schema import CafeOut


class SearchCreate(BaseModel):
    query: str = Field(
        ..., description="The search query, e.g., a cafe name, menu item name, or tag."
    )


class SearchOut(BaseModel):
    cafes: Optional[List[CafeOut]] = Field(
        None, description="List of cafes matching the search query."
    )
