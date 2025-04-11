import pymongo
from pydantic import BaseModel, Field
from typing import Optional
from app.models import CafeId, CustomDocument, Id
from pymongo import IndexModel


class StockBase(BaseModel, Id):
    name: str = Field(..., min_length=1, max_length=50, description="Name of the item")
    description: Optional[str] = Field(None, min_length=1, max_length=255)
    quantity: int = Field(..., description="Quantity in stock")

class Stock(CustomDocument, StockBase, CafeId):

    class Settings:
        name = "stocks" 
        indexes = [
            IndexModel([("cafe_id", pymongo.ASCENDING)]),
            IndexModel([("category_ids", pymongo.ASCENDING)]),
            IndexModel([("name", pymongo.ASCENDING)]),
            IndexModel([("description", pymongo.ASCENDING)]),
            IndexModel([("_id", pymongo.ASCENDING), ("cafe_id", pymongo.ASCENDING)]),
            IndexModel([("cafe_id", pymongo.ASCENDING), ("name", pymongo.ASCENDING)], unique=True,),
        ]



class StockCreate(StockBase):
    """Model for creating stock items."""

    pass

class StockUpdate(StockBase):
    """Model for creating stock items."""

    pass
