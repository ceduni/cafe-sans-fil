from pydantic import BaseModel, Field
from uuid import UUID
from app.models.cafe_model import CafeOut

class searchCreate(BaseModel):
     query: str = Field(..., description="The search query, e.g., a cafe name, menu item name, or tag.")

class SearchOut(BaseModel):
    cafes: Optional[List[CafeOut]] = Field(None, description="List of cafes matching the search query.")
   